import inspect
from flask import Blueprint, request, jsonify, current_app, url_for, redirect, g
import jwt
from datetime import datetime, timedelta
from .db import Database
from .models import User, Role, ApiToken
from .exceptions import AuthError
import uuid
import requests
import bcrypt
import logging
import os
import re
from functools import wraps
from isodate import parse_duration
import threading
import time
import msal
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AuthManager:
    def __init__(self, app=None, db_dsn=None, jwt_secret=None, oauth_config=None, id_type='integer', environment_prefix=None, api_tokens=None, cache_ttl=10, allow_oauth_auto_create=None, email_username=None, email_password=None, email_address=None, email_reply_to=None, email_server=None, email_port=None, role_implications=None):
        self.user_override = None
        self._user_cache = {}
        self._cache_ttl = cache_ttl or 10  # 10 seconds
        self._last_used_updates = {}  # Track pending updates
        self._update_lock = threading.Lock()
        self._update_thread = None
        self._shutdown_event = threading.Event()
        self._token_resolvers = {}  # Registered functions for token resolution
        self.role_implications = role_implications or {}

        # Determine prefix: empty if environment_prefix is None/empty, otherwise use it with '_' delimiter
        prefix = (environment_prefix.upper() + '_') if environment_prefix else ''
        
        # Arguments have priority over environment variables
        db_dsn = db_dsn or os.getenv(f'{prefix}DATABASE_URL')
        jwt_secret = jwt_secret or os.getenv(f'{prefix}JWT_SECRET')
        
        # OAuth config: use argument if provided, otherwise build from env vars
        if oauth_config is None:
            google_client_id = os.getenv(f'{prefix}GOOGLE_CLIENT_ID')
            google_client_secret = os.getenv(f'{prefix}GOOGLE_CLIENT_SECRET')
            oauth_config = {}
            if google_client_id and google_client_secret:
                oauth_config['google'] = {
                    'client_id': google_client_id,
                    'client_secret': google_client_secret
                }
        
        # OAuth auto-create: use argument if provided, otherwise check env var (defaults to False)
        if allow_oauth_auto_create is not None:
            self.allow_oauth_auto_create = allow_oauth_auto_create
        else:
            auto_create_env = os.getenv(f'{prefix}OAUTH_ALLOW_AUTO_CREATE')
            if auto_create_env is not None:
                self.allow_oauth_auto_create = auto_create_env.lower() in ['1', 'true', 'yes']
            else:
                self.allow_oauth_auto_create = False
        
        # API tokens: use argument if provided, otherwise parse from env var
        if api_tokens is None:
            api_tokens_env = os.getenv(f'{prefix}API_TOKENS')
            if api_tokens_env:
                api_tokens = {}
                for entry in api_tokens_env.split(','):
                    if ':' in entry:
                        key, user = entry.split(':', 1)
                        api_tokens[key.strip()] = user.strip()
        
        # User override: use argument if provided, otherwise check env var
        user_override_env = os.getenv(f'{prefix}USER_OVERRIDE')
        if user_override_env:
            self.user_override = user_override_env
        
        # Email configuration: arguments have priority
        email_username = email_username or os.getenv(f'{prefix}EMAIL_USERNAME')
        email_password = email_password or os.getenv(f'{prefix}EMAIL_PASSWORD')
        email_address = email_address or os.getenv(f'{prefix}EMAIL_ADDRESS')
        email_reply_to = email_reply_to or os.getenv(f'{prefix}EMAIL_REPLY_TO')
        email_server = email_server or os.getenv(f'{prefix}EMAIL_SERVER')
        email_port = email_port or os.getenv(f'{prefix}EMAIL_PORT')
            
        self.expiry_time = parse_duration(os.getenv(f'{prefix}JWT_TOKEN_EXPIRY_TIME', 'PT1H'))
        if self.user_override and (api_tokens or db_dsn):
            raise ValueError('Cannot set user_override together with api_tokens or db_dsn')
        if api_tokens and db_dsn:
            raise ValueError('Cannot set both api_tokens and db_dsn')
        self.api_tokens = api_tokens or None
        self.db = Database(db_dsn, id_type=id_type) if db_dsn else None
        self.jwt_secret = jwt_secret
        self.oauth_config = oauth_config or {}
        
        # Email configuration
        self.email_username = email_username
        self.email_password = email_password
        self.email_address = email_address or email_username
        if email_reply_to:
            self.email_reply_to = email_reply_to
        elif email_username:
            domain = email_username.split('@')[1] if '@' in email_username else 'localhost'
            self.email_reply_to = f'noreply@{domain}'
        else:
            self.email_reply_to = None
        self.email_server = email_server
        self.email_port = int(email_port) if email_port else 587
        
        self.public_endpoints = {
            'auth.login',
            'auth.oauth_login',
            'auth.oauth_callback',
            'auth.refresh_token',
            'auth.register',
            'auth.get_roles',
            'auth.validate_registration',
            'auth.resend_validation'
        }
        self.bp = None
        if self.db:
            self._ensure_admin_role()
        
        if app:
            self.init_app(app)
        
        # Start the background update thread
        self._start_update_thread()

    def _ensure_admin_role(self):
        try:
            with self.db.get_cursor() as cur:
                cur.execute("SELECT COUNT(*) AS role_count FROM roles")
                result = cur.fetchone() or {}
                if result.get('role_count', 0):
                    return
                role = Role('administrator', 'Default administrator role', self.db.get_id_generator())
                columns = ['name', 'description', 'created_at']
                values = [role.name, role.description, role.created_at]
                placeholders = ['%s', '%s', '%s']
                if role.id is not None:
                    columns.insert(0, 'id')
                    values.insert(0, role.id)
                    placeholders.insert(0, '%s')
                cur.execute(
                    f"INSERT INTO roles ({', '.join(columns)}) VALUES ({', '.join(placeholders)})",
                    values
                )
                logger.info('Default admin role created')
        except Exception:
            logger.exception('Ensure admin role failed')

    def _ensure_admin_role(self):
        try:
            with self.db.get_cursor() as cur:
                cur.execute("SELECT COUNT(*) AS user_count FROM users")
                result = cur.fetchone() or {}
                if result.get('user_count', 0):
                    return
                # Generate a secure 12-character password
                alphabet = string.ascii_letters + string.digits + string.punctuation
                password = ''.join(secrets.choice(alphabet) for _ in range(12))
                logger.info(f"There were no users in the database. A temporary user `admin` has been created with password: {password}")
                role = Role('administrator', 'Default administrator role', self.db.get_id_generator())
                columns = ['name', 'description', 'created_at']
                values = [role.name, role.description, role.created_at]
                placeholders = ['%s', '%s', '%s']
                if role.id is not None:
                    columns.insert(0, 'id')
                    values.insert(0, role.id)
                    placeholders.insert(0, '%s')
                cur.execute(
                    f"INSERT INTO roles ({', '.join(columns)}) VALUES ({', '.join(placeholders)})",
                    values
                )
                logger.info('Default admin role created')
        except Exception:
            logger.exception('Ensure admin role failed')

    def _extract_token_from_header(self):
        #print('request.headers', request.headers, 'authorization', request.authorization, 'request', request)
        auth = request.authorization
        if not auth or not auth.token:
            raise AuthError('No authorization header or token', 401)

        if auth.type.lower() != 'bearer':
            raise AuthError('Invalid authorization scheme', 401)

        return auth.token

    def get_redirect_uri(self):
        redirect_uri = os.getenv('REDIRECT_URL') or url_for('auth.oauth_callback', _external=True).replace("http://", "https://")
        logger.info(f"REDIRECT URI..: {redirect_uri}")
        return redirect_uri

    def _validate_api_token(self, api_token):
        if self.api_tokens is not None:
            username = self.api_tokens.get(api_token)
            if not username:
                raise AuthError('Invalid API token')
            # Return a minimal user dict
            return {
                'id': username,
                'username': username,
                'email': '',
                'real_name': username,
                'roles': []
            }
        try:
            parsed = ApiToken.parse_token(api_token)
            
            # Check cache first
            cache_key = f"api_token_{parsed['id']}"
            current_time = datetime.utcnow()
            
            if cache_key in self._user_cache:
                cached_data, cache_time = self._user_cache[cache_key]
                if (current_time - cache_time).total_seconds() < self._cache_ttl:
                    logger.debug(f"Returning cached API token data for ID: {parsed['id']}")
                    return cached_data.copy()  # Return a copy to avoid modifying cache
            
            # Cache miss or expired, fetch from database
            with self.db.get_cursor() as cur:
                # First get the API token record
                cur.execute("""
                    SELECT t.*, u.*, r.name as role_name FROM api_tokens t
                    JOIN users u ON t.user_id = u.id
                    LEFT JOIN user_roles ur ON ur.user_id = u.id
                    LEFT JOIN roles r ON ur.role_id = r.id
                    WHERE t.id = %s
                """, (parsed['id'],))
                results = cur.fetchall()
                if not results:
                    raise AuthError('Invalid API token')

                # Get the first row for token/user data (all rows will have same token/user data)
                result = results[0]
                
                # Verify the nonce
                if not bcrypt.checkpw(parsed['nonce'].encode('utf-8'), result['token'].encode('utf-8')):
                    raise AuthError('Invalid API token')

                # Check if token is expired
                if result['expires_at'] and result['expires_at'] < datetime.utcnow():
                    raise AuthError('API token has expired')

                # Schedule last used timestamp update (asynchronous with 10s delay)
                self._schedule_last_used_update(parsed['id'])

                # Extract roles from results
                roles = [row['role_name'] for row in results if row['role_name'] is not None]

                # Construct user object
                user_data = {
                    'id': result['user_id'],
                    'username': result['username'],
                    'email': result['email'],
                    'real_name': result['real_name'],
                    'roles': roles
                }

            # Cache the result
            self._user_cache[cache_key] = (user_data.copy(), current_time)
            
            # Clean up expired cache entries
            self._cleanup_cache()
            
            return user_data
        except ValueError:
            raise AuthError('Invalid token format')

    def _authenticate_request(self):
        if hasattr(g, 'requesting_user'):
            return g.requesting_user
        g.requesting_user = self._authenticate_request_helper()
        return g.requesting_user

    def _authenticate_request_helper(self):
        if self.user_override:
            return {
                'id': self.user_override,
                'username': self.user_override,
                'email': '',
                'real_name': self.user_override,
                'roles': []
            }
        auth_header = request.headers.get('Authorization')
        api_token = request.headers.get('X-API-Token')

        if auth_header and auth_header.startswith('Bearer '):
            # JWT authentication
            token = self._extract_token_from_header()
            return self.validate_token(token)
        elif api_token:
            # API token authentication
            return self._validate_api_token(api_token)
        else:
            raise AuthError('No authentication provided', 401)

    def require_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = self._authenticate_request()
            sig = inspect.signature(f)
            if 'requesting_user' in sig.parameters:
                kwargs['requesting_user'] = user

            return f(*args, **kwargs)
        return decorated

    def add_public_endpoint(self, endpoint):
        """Mark an endpoint as public so it bypasses authentication."""
        self.public_endpoints.add(endpoint)

    def public_endpoint(self, f):
        """Decorator to mark a view function as public."""
        # Always register the bare function name so application level routes
        # are exempt from authentication checks.
        self.add_public_endpoint(f.__name__)

        # If a blueprint is active, also register the blueprint-prefixed name
        # used by Flask for endpoint identification.
        if self.bp:
            endpoint = f"{self.bp.name}.{f.__name__}"
            self.add_public_endpoint(endpoint)
        return f
    
    def init_app(self, app):
        app.auth_manager = self
        app.register_blueprint(self.create_blueprint())
        @app.errorhandler(AuthError)
        def handle_auth_error(e):
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
            return response

    def create_blueprint(self):
        bp = Blueprint('auth', __name__, url_prefix='/api/v1/users')
        self.bp = bp
        bp.public_endpoint = self.public_endpoint

        @bp.errorhandler(AuthError)
        def handle_auth_error(err):
            response = jsonify(err.to_dict())
            response.status_code = err.status_code
            return response

        @bp.before_request
        def load_user():
            if request.method == 'OPTIONS':
                return  # Skip authentication for OPTIONS
            if request.endpoint not in self.public_endpoints:
                g.requesting_user = self._authenticate_request()

        @bp.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                raise AuthError('Username and password required', 400)
            
            with self.db.get_cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cur.fetchone()
                
                if not user or not self._verify_password(password, user['password_hash']):
                    raise AuthError('Invalid username or password', 401)
                
                # Fetch roles
                cur.execute("""
                    SELECT r.name FROM roles r
                    JOIN user_roles ur ON ur.role_id = r.id
                    WHERE ur.user_id = %s
                """, (user['id'],))
                roles = [row['name'] for row in cur.fetchall()]
                user['roles'] = roles
                
                # Check if user is validated
                if 'validated' not in roles:
                    raise AuthError('Account not yet validated. Please check your email for the validation link.', 403)
                
                token = self._create_token(user)
                refresh_token = self._create_refresh_token(user)
                
                return jsonify({
                    'token': token,
                    'refresh_token': refresh_token,
                    'user': user
                })

        @bp.route('/login/oauth', methods=['POST'])
        def oauth_login():
            provider = request.json.get('provider')
            if provider not in self.oauth_config:
                logger.error(f"Invalid OAuth provider: {provider}")
                logger.error(f"These are the known ones: {self.oauth_config.keys()}")
                raise AuthError('Invalid OAuth provider', 400)

            redirect_uri = self.get_redirect_uri()
            return jsonify({
                'redirect_url': self._get_oauth_url(provider, redirect_uri)
            })

        @bp.route('/login/oauth2callback')
        def oauth_callback():
            code = request.args.get('code')
            provider = request.args.get('state')
            
            if not code or not provider:
                raise AuthError('Invalid OAuth callback', 400)
            from urllib.parse import urlencode, urlparse, urlunparse
            get_redirect_uri = self.get_redirect_uri()
            parsed_uri = urlparse(get_redirect_uri)
            frontend_url = os.getenv('FRONTEND_URL', urlunparse((parsed_uri.scheme, parsed_uri.netloc, '', '', '', '')))
            
            #if provider == 'microsoft':
            #    client = msal.ConfidentialClientApplication(
            #        self.oauth_config[provider]['client_id'], client_credential=self.oauth_config[provider]['client_secret'], authority=f"https://login.microsoftonline.com/common"
            #    )
            #    result = client.acquire_token_by_authorization_code(code, scopes=["email"], redirect_uri=self.get_redirect_uri())
            #    code = result['access_token']
            
            try:
                user_info = self._get_oauth_user_info(provider, code)
                token = self._create_token(user_info)
                refresh_token = self._create_refresh_token(user_info)
                # Redirect to frontend with tokens
                return redirect(f"{frontend_url}/oauth-callback?" + urlencode({'token': token, 'refresh_token': refresh_token}))
            except AuthError as e:
                # Surface error to frontend for user-friendly messaging
                params = {
                    'error': str(e.message) if hasattr(e, 'message') else str(e),
                    'status': getattr(e, 'status_code', 500),
                    'provider': provider,
                }
                return redirect(f"{frontend_url}/oauth-callback?" + urlencode(params))

        @bp.route('/login/profile')
        def profile():
            user = g.requesting_user
            return jsonify(user)

        @bp.route('/api-tokens', methods=['GET'])
        def get_tokens():
            tokens = self.get_user_api_tokens(g.requesting_user['id'])
            return jsonify(tokens)

        @bp.route('/api-tokens', methods=['POST'])
        def create_token():
            name = request.json.get('name')
            expires_in_days = request.json.get('expires_in_days')
            if not name:
                raise AuthError('Token name is required', 400)
            api_token = self.create_api_token(g.requesting_user['id'], name, expires_in_days)
            return jsonify({
                'id': api_token.id,
                'name': api_token.name,
                'token': api_token.get_full_token(),
                'created_at': api_token.created_at,
                'expires_at': api_token.expires_at
            })

        @bp.route('/token-refresh', methods=['POST'])
        def refresh_token():
            refresh_token = request.json.get('refresh_token')
            if not refresh_token:
                raise AuthError('No refresh token provided', 400)

            try:
                payload = jwt.decode(refresh_token, self.jwt_secret, algorithms=['HS256'])
                user_id = payload['sub']
                
                with self.db.get_cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                    user = cur.fetchone()

                if not user:
                    raise AuthError('User not found', 404)

                return jsonify({
                    'token': self._create_token(user),
                    'refresh_token': self._create_refresh_token(user)
                })
            except jwt.InvalidTokenError:
                raise AuthError('Invalid refresh token', 401)

        @bp.route('/api-tokens', methods=['POST'])
        def create_api_token():
            name = request.json.get('name')
            if not name:
                raise AuthError('Token name required', 400)

            token = self.create_api_token(g.requesting_user['id'], name)
            return jsonify({'token': token.token})

        @bp.route('/api-tokens/validate', methods=['GET'])
        def validate_api_token():
            token = request.json.get('token')
            if not token:
                raise AuthError('No API token provided', 401)
            token = ApiToken.parse_token_id(token)

            with self.db.get_cursor() as cur:
                cur.execute("""
                    SELECT * FROM api_tokens 
                    WHERE user_id = %s AND id = %s
                """, (g.requesting_user['id'], token))
                api_token = cur.fetchone()

            if not api_token:
                raise AuthError('Invalid API token', 401)

            # Check if token is expired
            if api_token['expires_at'] and api_token['expires_at'] < datetime.utcnow():
                raise AuthError('API token has expired', 401)

            # Update last used timestamp
            with self.db.get_cursor() as cur:
                cur.execute("""
                    UPDATE api_tokens 
                    SET last_used_at = %s
                    WHERE id = %s
                """, (datetime.utcnow(), api_token['id']))

            return jsonify({'valid': True})

        @bp.route('/api-tokens', methods=['DELETE'])
        def delete_api_token():
            token = request.json.get('token')
            if not token:
                raise AuthError('Token required', 400)
            token = ApiToken.parse_token_id(token)

            with self.db.get_cursor() as cur:
                cur.execute("""
                    DELETE FROM api_tokens 
                    WHERE user_id = %s AND id = %s
                    RETURNING id
                """, (g.requesting_user['id'], token))
                deleted_id = cur.fetchone()
                if not deleted_id:
                    raise ValueError('Token not found or already deleted')

            return jsonify({'deleted': True})

        @bp.route('/register', methods=['POST'])
        def register():
            data = request.get_json()
            
            password = data.get('password')
            if not password:
                raise AuthError('Password is required', 400)
            
            username = data.get('username')
            email = data.get('email')
            
            if not username:
                raise AuthError('Username is required', 400)
            if not email:
                raise AuthError('Email is required', 400)
            
            # Validate password strength
            self._validate_password_strength(password, username=username, email=email)
            
            # Hash the password
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            user = User(
                username=username,
                email=email,
                real_name=data['real_name'],
                roles=data.get('roles', []),
                id_generator=self.db.get_id_generator()
            )

            with self.db.get_cursor() as cur:
                # Check if username or email already exists
                cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
                existing_user = cur.fetchone()
                
                if existing_user:
                    user_id = existing_user['id']
                    
                    # Check if user is validated
                    cur.execute("""
                        SELECT r.name FROM roles r
                        JOIN user_roles ur ON ur.role_id = r.id
                        WHERE ur.user_id = %s AND r.name = 'validated'
                    """, (user_id,))
                    if cur.fetchone():
                        # User is validated, reject registration
                        raise AuthError('Username or email already exists', 400)
                    
                    # User exists but not validated - allow re-registration
                    # This works even if the previous registration hasn't expired yet
                    # Update existing user with new registration data
                    cur.execute("""
                        UPDATE users 
                        SET username = %s, email = %s, real_name = %s, password_hash = %s, updated_at = %s
                        WHERE id = %s
                    """, (username, email, user.real_name, password_hash.decode('utf-8'), datetime.utcnow(), user_id))
                    
                    # Remove all existing register-* roles (including non-expired ones)
                    cur.execute("""
                        DELETE FROM user_roles
                        WHERE user_id = %s
                        AND role_id IN (
                            SELECT id FROM roles WHERE name LIKE 'register-%'
                        )
                    """, (user_id,))
                    
                    user.id = user_id
                else:
                    # New user - create it
                    if user.id is None:
                        cur.execute("""
                            INSERT INTO users (username, email, real_name, password_hash, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (user.username, user.email, user.real_name, password_hash.decode('utf-8'),
                              user.created_at, user.updated_at))
                        user.id = cur.fetchone()['id']
                    else:
                        cur.execute("""
                            INSERT INTO users (id, username, email, real_name, password_hash, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (user.id, user.username, user.email, user.real_name, password_hash.decode('utf-8'),
                              user.created_at, user.updated_at))
                
                # Generate nonce and timestamp for validation
                nonce = str(uuid.uuid4())
                timestamp = int(time.time())
                role_name = f'register-{nonce}-{timestamp}'
                
                # Create temporary validation role
                cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
                role = cur.fetchone()
                if not role:
                    role_obj = Role(role_name, description='Temporary registration validation role', id_generator=self.db.get_id_generator())
                    if role_obj.id is None:
                        cur.execute("""
                            INSERT INTO roles (name, description, created_at)
                            VALUES (%s, %s, %s)
                            RETURNING id
                        """, (role_obj.name, role_obj.description, role_obj.created_at))
                        role_id = cur.fetchone()['id']
                    else:
                        cur.execute("""
                            INSERT INTO roles (id, name, description, created_at)
                            VALUES (%s, %s, %s, %s)
                        """, (role_obj.id, role_obj.name, role_obj.description, role_obj.created_at))
                        role_id = role_obj.id
                else:
                    role_id = role['id']
                
                # Associate role with user
                cur.execute("""
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id, role_id) DO NOTHING
                """, (user.id, role_id))
                
                # Send validation email
                frontend_url = self._get_frontend_url()
                validation_link = f"{frontend_url}/register/{nonce}"
                email_subject = "Please validate your account"
                email_body = f"""Hello {user.real_name},

Thank you for registering. Please click the link below to validate your account:

{validation_link}

This link will expire in 24 hours.

If you did not register for this account, please ignore this email.
"""
                self._send_email(user.email, email_subject, email_body)

            return jsonify({'id': user.id, 'message': 'Registration successful. Please check your email for validation link.'}), 201

        @bp.route('/register/<nonce>', methods=['GET'])
        @bp.public_endpoint
        def validate_registration(nonce):
            with self.db.get_cursor() as cur:
                # Find user with register-{nonce}-{timestamp} role
                cur.execute("""
                    SELECT u.id, u.username, u.email, r.name as role_name
                    FROM users u
                    JOIN user_roles ur ON ur.user_id = u.id
                    JOIN roles r ON ur.role_id = r.id
                    WHERE r.name LIKE %s
                """, (f'register-{nonce}-%',))
                results = cur.fetchall()
                
                if not results:
                    raise AuthError('Invalid or expired validation link', 400)
                
                # Check if expired (24 hours)
                current_time = int(time.time())
                user_id = None
                expired = True
                
                for row in results:
                    role_name = row['role_name']
                    if role_name.startswith(f'register-{nonce}-'):
                        try:
                            timestamp = int(role_name.split('-')[-1])
                            if current_time - timestamp < 86400:  # 24 hours
                                expired = False
                                user_id = row['id']
                                break
                        except (ValueError, IndexError):
                            continue
                
                if expired or not user_id:
                    raise AuthError('Validation link has expired. Please request a new validation email.', 400)
                
                # Remove all register-* roles from user
                cur.execute("""
                    DELETE FROM user_roles
                    WHERE user_id = %s
                    AND role_id IN (
                        SELECT id FROM roles WHERE name LIKE 'register-%%'
                    )
                """, (user_id,))
                
                # Ensure validated role exists
                cur.execute("SELECT id FROM roles WHERE name = 'validated'")
                validated_role = cur.fetchone()
                if not validated_role:
                    role_obj = Role('validated', description='User has validated their email', id_generator=self.db.get_id_generator())
                    if role_obj.id is None:
                        cur.execute("""
                            INSERT INTO roles (name, description, created_at)
                            VALUES (%s, %s, %s)
                            RETURNING id
                        """, (role_obj.name, role_obj.description, role_obj.created_at))
                        validated_role_id = cur.fetchone()['id']
                    else:
                        cur.execute("""
                            INSERT INTO roles (id, name, description, created_at)
                            VALUES (%s, %s, %s, %s)
                        """, (role_obj.id, role_obj.name, role_obj.description, role_obj.created_at))
                        validated_role_id = role_obj.id
                else:
                    validated_role_id = validated_role['id']
                
                # Add validated role to user
                cur.execute("""
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id, role_id) DO NOTHING
                """, (user_id, validated_role_id))
            
            return jsonify({'message': 'Account validated successfully. You can now log in.'})

        @bp.route('/resend-validation', methods=['POST'])
        @bp.public_endpoint
        def resend_validation():
            data = request.get_json()
            email = data.get('email')
            username = data.get('username')
            
            if not email and not username:
                raise AuthError('Email or username is required', 400)
            
            with self.db.get_cursor() as cur:
                # Find user by email or username
                if email:
                    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                else:
                    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cur.fetchone()
                
                if not user:
                    # Don't reveal if user exists
                    return jsonify({'message': 'If an account exists, a validation email has been sent.'})
                
                # Check if user is already validated
                cur.execute("""
                    SELECT r.name FROM roles r
                    JOIN user_roles ur ON ur.role_id = r.id
                    WHERE ur.user_id = %s AND r.name = 'validated'
                """, (user['id'],))
                if cur.fetchone():
                    # User is already validated, don't reveal this
                    return jsonify({'message': 'If an account exists, a validation email has been sent.'})
                
                # Remove existing register-* roles
                cur.execute("""
                    DELETE FROM user_roles
                    WHERE user_id = %s
                    AND role_id IN (
                        SELECT id FROM roles WHERE name LIKE 'register-%%'
                    )
                """, (user['id'],))
                
                # Generate new nonce and timestamp
                nonce = str(uuid.uuid4())
                timestamp = int(time.time())
                role_name = f'register-{nonce}-{timestamp}'
                
                # Create new validation role
                cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
                role = cur.fetchone()
                if not role:
                    role_obj = Role(role_name, description='Temporary registration validation role', id_generator=self.db.get_id_generator())
                    if role_obj.id is None:
                        cur.execute("""
                            INSERT INTO roles (name, description, created_at)
                            VALUES (%s, %s, %s)
                            RETURNING id
                        """, (role_obj.name, role_obj.description, role_obj.created_at))
                        role_id = cur.fetchone()['id']
                    else:
                        cur.execute("""
                            INSERT INTO roles (id, name, description, created_at)
                            VALUES (%s, %s, %s, %s)
                        """, (role_obj.id, role_obj.name, role_obj.description, role_obj.created_at))
                        role_id = role_obj.id
                else:
                    role_id = role['id']
                
                # Associate role with user
                cur.execute("""
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id, role_id) DO NOTHING
                """, (user['id'], role_id))
                
                # Send validation email
                frontend_url = self._get_frontend_url()
                validation_link = f"{frontend_url}/register/{nonce}"
                email_subject = "Please validate your account"
                email_body = f"""Hello {user['real_name']},

Please click the link below to validate your account:

{validation_link}

This link will expire in 24 hours.

If you did not request this email, please ignore it.
"""
                self._send_email(user['email'], email_subject, email_body)
            
            return jsonify({'message': 'If an account exists, a validation email has been sent.'})

        @bp.route('/request-password-reset', methods=['POST'])
        @bp.public_endpoint
        def request_password_reset():
            data = request.get_json()
            username = data.get('username')
            
            if not username:
                raise AuthError('Username is required', 400)
            
            with self.db.get_cursor() as cur:
                # Find user by username
                cur.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cur.fetchone()
                
                if not user:
                    # Don't reveal if user exists
                    return jsonify({'message': 'If an account exists, a password reset email has been sent.'})
                
                # Remove existing password-reset-* roles
                cur.execute("""
                    DELETE FROM user_roles
                    WHERE user_id = %s
                    AND role_id IN (
                        SELECT id FROM roles WHERE name LIKE 'password-reset-%%'
                    )
                """, (user['id'],))
                
                # Generate new nonce and timestamp
                nonce = str(uuid.uuid4())
                timestamp = int(time.time())
                role_name = f'password-reset-{nonce}-{timestamp}'
                
                # Create new password reset role
                cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
                role = cur.fetchone()
                if not role:
                    role_obj = Role(role_name, description='Temporary password reset role', id_generator=self.db.get_id_generator())
                    if role_obj.id is None:
                        cur.execute("""
                            INSERT INTO roles (name, description, created_at)
                            VALUES (%s, %s, %s)
                            RETURNING id
                        """, (role_obj.name, role_obj.description, role_obj.created_at))
                        role_id = cur.fetchone()['id']
                    else:
                        cur.execute("""
                            INSERT INTO roles (id, name, description, created_at)
                            VALUES (%s, %s, %s, %s)
                        """, (role_obj.id, role_obj.name, role_obj.description, role_obj.created_at))
                        role_id = role_obj.id
                else:
                    role_id = role['id']
                
                # Associate role with user
                cur.execute("""
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id, role_id) DO NOTHING
                """, (user['id'], role_id))
                
                # Send password reset email
                frontend_url = self._get_frontend_url()
                reset_link = f"{frontend_url}/password-reset/{nonce}"
                email_subject = "Password Reset Request"
                email_body = f"""Hello {user['real_name']},

You requested to reset your password. Please click the link below to reset your password:

{reset_link}

This link will expire in 24 hours.

If you did not request a password reset, please ignore this email.
"""
                self._send_email(user['email'], email_subject, email_body)
            
            return jsonify({'message': 'If an account exists, a password reset email has been sent.'})

        @bp.route('/password-reset/<nonce>', methods=['GET'])
        @bp.public_endpoint
        def validate_password_reset(nonce):
            with self.db.get_cursor() as cur:
                # Find user with password-reset-{nonce}-{timestamp} role
                cur.execute("""
                    SELECT u.id, u.username, u.email, r.name as role_name
                    FROM users u
                    JOIN user_roles ur ON ur.user_id = u.id
                    JOIN roles r ON ur.role_id = r.id
                    WHERE r.name LIKE %s
                """, (f'password-reset-{nonce}-%',))
                results = cur.fetchall()
                
                if not results:
                    raise AuthError('Invalid or expired password reset link', 400)
                
                # Check if expired (24 hours)
                current_time = int(time.time())
                user_id = None
                expired = True
                
                for row in results:
                    role_name = row['role_name']
                    if role_name.startswith(f'password-reset-{nonce}-'):
                        try:
                            timestamp = int(role_name.split('-')[-1])
                            if current_time - timestamp < 86400:  # 24 hours
                                expired = False
                                user_id = row['id']
                                break
                        except (ValueError, IndexError):
                            continue
                
                if expired or not user_id:
                    raise AuthError('Password reset link has expired. Please request a new password reset email.', 400)
                
                # Return user info (username only for security)
                cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
                user = cur.fetchone()
                
                return jsonify({'username': user['username'], 'message': 'Password reset link is valid.'})

        @bp.route('/password-reset/<nonce>', methods=['POST'])
        @bp.public_endpoint
        def reset_password(nonce):
            data = request.get_json()
            password = data.get('password')
            confirm_password = data.get('confirmPassword')
            
            if not password:
                raise AuthError('Password is required', 400)
            if password != confirm_password:
                raise AuthError('Passwords do not match', 400)
            
            with self.db.get_cursor() as cur:
                # Find user with password-reset-{nonce}-{timestamp} role
                cur.execute("""
                    SELECT u.id, u.username, u.email, r.name as role_name
                    FROM users u
                    JOIN user_roles ur ON ur.user_id = u.id
                    JOIN roles r ON ur.role_id = r.id
                    WHERE r.name LIKE %s
                """, (f'password-reset-{nonce}-%',))
                results = cur.fetchall()
                
                if not results:
                    raise AuthError('Invalid or expired password reset link', 400)
                
                # Check if expired (24 hours)
                current_time = int(time.time())
                user_id = None
                username = None
                email = None
                expired = True
                
                for row in results:
                    role_name = row['role_name']
                    if role_name.startswith(f'password-reset-{nonce}-'):
                        try:
                            timestamp = int(role_name.split('-')[-1])
                            if current_time - timestamp < 86400:  # 24 hours
                                expired = False
                                user_id = row['id']
                                username = row['username']
                                email = row['email']
                                break
                        except (ValueError, IndexError):
                            continue
                
                if expired or not user_id:
                    raise AuthError('Password reset link has expired. Please request a new password reset email.', 400)
                
                # Validate password strength
                self._validate_password_strength(password, username=username, email=email)
                
                # Hash new password
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
                
                # Update user's password
                cur.execute("""
                    UPDATE users 
                    SET password_hash = %s, updated_at = %s
                    WHERE id = %s
                """, (password_hash.decode('utf-8'), datetime.utcnow(), user_id))
                
                # Remove all password-reset-* roles from user
                cur.execute("""
                    DELETE FROM user_roles
                    WHERE user_id = %s
                    AND role_id IN (
                        SELECT id FROM roles WHERE name LIKE 'password-reset-%%'
                    )
                """, (user_id,))
            
            return jsonify({'message': 'Password has been reset successfully. You can now log in with your new password.'})

        @bp.route('/change-password', methods=['POST'])
        def change_password():
            user = g.requesting_user
            if not user:
                raise AuthError('Authentication required', 401)
            
            data = request.get_json()
            current_password = data.get('currentPassword')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')
            
            if not current_password or not password or not confirm_password:
                raise AuthError('Current password, new password, and confirmation are required', 400)
            
            if password != confirm_password:
                raise AuthError('New password and confirmation do not match', 400)
            
            with self.db.get_cursor() as cur:
                # Get user with password hash
                cur.execute("SELECT * FROM users WHERE id = %s", (user['id'],))
                db_user = cur.fetchone()
                
                if not db_user:
                    raise AuthError('User not found', 404)
                
                # Check if user has a password (OAuth-only users might not have one)
                if not db_user.get('password_hash'):
                    raise AuthError('No password set for this account. Please use password reset instead.', 400)
                
                # Verify current password
                if not self._verify_password(current_password, db_user['password_hash']):
                    raise AuthError('Current password is incorrect', 401)
                
                # Validate new password strength
                self._validate_password_strength(password, username=db_user['username'], email=db_user.get('email'))
                
                # Hash new password
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
                
                # Update user's password
                cur.execute("""
                    UPDATE users 
                    SET password_hash = %s, updated_at = %s
                    WHERE id = %s
                """, (password_hash.decode('utf-8'), datetime.utcnow(), user['id']))
            
            return jsonify({'message': 'Password has been changed successfully.'})

        @bp.route('/roles', methods=['GET'])
        def get_roles():
            with self.db.get_cursor() as cur:
                cur.execute("SELECT * FROM roles")
                roles = cur.fetchall()
            return jsonify(roles)

        # Admin endpoints - require administrator role
        @bp.route('/admin/users', methods=['GET'])
        def admin_get_users():
            self._require_admin_role()
            with self.db.get_cursor() as cur:
                cur.execute("""
                    SELECT u.*, 
                           COALESCE(array_agg(r.name) FILTER (WHERE r.name IS NOT NULL), '{}') as roles
                    FROM users u
                    LEFT JOIN user_roles ur ON ur.user_id = u.id
                    LEFT JOIN roles r ON ur.role_id = r.id
                    GROUP BY u.id, u.username, u.email, u.real_name, u.created_at, u.updated_at
                    ORDER BY u.created_at DESC
                """)
                users = cur.fetchall()
            return jsonify(users)

        @bp.route('/admin/users', methods=['POST'])
        def admin_create_user():
            self._require_admin_role()
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['username', 'email', 'real_name', 'password']
            for field in required_fields:
                if not data.get(field):
                    raise AuthError(f'{field} is required', 400)
            
            # Validate password strength
            self._validate_password_strength(data['password'], username=data['username'], email=data['email'])
            
            # Hash the password
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
            
            with self.db.get_cursor() as cur:
                # Check if username or email already exists
                cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", 
                           (data['username'], data['email']))
                if cur.fetchone():
                    raise AuthError('Username or email already exists', 400)
                
                # Create user
                cur.execute("""
                    INSERT INTO users (username, email, real_name, password_hash, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (data['username'], data['email'], data['real_name'], 
                      password_hash.decode('utf-8'), datetime.utcnow(), datetime.utcnow()))
                user_id = cur.fetchone()['id']
                
                # Assign roles if provided
                if data.get('roles'):
                    for role_name in data['roles']:
                        cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
                        role = cur.fetchone()
                        if role:
                            cur.execute("""
                                INSERT INTO user_roles (user_id, role_id)
                                VALUES (%s, %s)
                                ON CONFLICT (user_id, role_id) DO NOTHING
                            """, (user_id, role['id']))
            
            return jsonify({'id': user_id}), 201

        @bp.route('/admin/users/<user_id>', methods=['PUT'])
        def admin_update_user(user_id):
            self._require_admin_role()
            data = request.get_json()
            
            with self.db.get_cursor() as cur:
                # Check if user exists and get current username/email
                cur.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
                user = cur.fetchone()
                if not user:
                    raise AuthError('User not found', 404)
                
                # Get username and email for password validation (use updated values if provided)
                username = data.get('username', user['username'])
                email = data.get('email', user['email'])
                
                # Validate password strength if password is being updated
                if 'password' in data:
                    self._validate_password_strength(data['password'], username=username, email=email)
                
                # Update user fields
                update_fields = []
                update_values = []
                
                if 'username' in data:
                    update_fields.append('username = %s')
                    update_values.append(data['username'])
                if 'email' in data:
                    update_fields.append('email = %s')
                    update_values.append(data['email'])
                if 'real_name' in data:
                    update_fields.append('real_name = %s')
                    update_values.append(data['real_name'])
                if 'password' in data:
                    salt = bcrypt.gensalt()
                    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
                    update_fields.append('password_hash = %s')
                    update_values.append(password_hash.decode('utf-8'))
                
                if update_fields:
                    update_fields.append('updated_at = %s')
                    update_values.append(datetime.utcnow())
                    update_values.append(user_id)
                    
                    cur.execute(f"""
                        UPDATE users 
                        SET {', '.join(update_fields)}
                        WHERE id = %s
                    """, update_values)
                
                # Update roles if provided
                if 'roles' in data:
                    # Remove existing roles
                    cur.execute("DELETE FROM user_roles WHERE user_id = %s", (user_id,))
                    
                    # Add new roles
                    for role_name in data['roles']:
                        cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
                        role = cur.fetchone()
                        if role:
                            cur.execute("""
                                INSERT INTO user_roles (user_id, role_id)
                                VALUES (%s, %s)
                            """, (user_id, role['id']))
            
            return jsonify({'success': True})

        @bp.route('/admin/users/<user_id>', methods=['DELETE'])
        def admin_delete_user(user_id):
            self._require_admin_role()
            
            with self.db.get_cursor() as cur:
                # Check if user exists
                cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
                if not cur.fetchone():
                    raise AuthError('User not found', 404)
                
                # Delete user (cascade will handle related records)
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
            return jsonify({'success': True})

        @bp.route('/admin/roles', methods=['GET'])
        def admin_get_roles():
            self._require_admin_role()
            with self.db.get_cursor() as cur:
                cur.execute("SELECT * FROM roles ORDER BY name")
                roles = cur.fetchall()
            return jsonify(roles)

        @bp.route('/admin/roles', methods=['POST'])
        def admin_create_role():
            self._require_admin_role()
            data = request.get_json()
            
            if not data.get('name'):
                raise AuthError('Role name is required', 400)
            
            with self.db.get_cursor() as cur:
                # Check if role already exists
                cur.execute("SELECT id FROM roles WHERE name = %s", (data['name'],))
                if cur.fetchone():
                    raise AuthError('Role already exists', 400)
                
                cur.execute("""
                    INSERT INTO roles (name, description, created_at)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (data['name'], data.get('description', ''), datetime.utcnow()))
                role_id = cur.fetchone()['id']
            
            return jsonify({'id': role_id}), 201

        @bp.route('/admin/roles/<role_id>', methods=['PUT'])
        def admin_update_role(role_id):
            self._require_admin_role()
            data = request.get_json()
            
            with self.db.get_cursor() as cur:
                # Check if role exists
                cur.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
                if not cur.fetchone():
                    raise AuthError('Role not found', 404)
                
                update_fields = []
                update_values = []
                
                if 'name' in data:
                    update_fields.append('name = %s')
                    update_values.append(data['name'])
                if 'description' in data:
                    update_fields.append('description = %s')
                    update_values.append(data['description'])
                
                if update_fields:
                    update_values.append(role_id)
                    cur.execute(f"""
                        UPDATE roles 
                        SET {', '.join(update_fields)}
                        WHERE id = %s
                    """, update_values)
            
            return jsonify({'success': True})

        @bp.route('/admin/roles/<role_id>', methods=['DELETE'])
        def admin_delete_role(role_id):
            self._require_admin_role()
            
            with self.db.get_cursor() as cur:
                # Check if role exists
                cur.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
                if not cur.fetchone():
                    raise AuthError('Role not found', 404)
                
                # Check if role is assigned to any users
                cur.execute("SELECT COUNT(*) as count FROM user_roles WHERE role_id = %s", (role_id,))
                count = cur.fetchone()['count']
                if count > 0:
                    raise AuthError('Cannot delete role that is assigned to users', 400)
                
                cur.execute("DELETE FROM roles WHERE id = %s", (role_id,))
            
            return jsonify({'success': True})

        @bp.route('/admin/api-tokens', methods=['GET'])
        def admin_get_all_tokens():
            self._require_admin_role()
            with self.db.get_cursor() as cur:
                cur.execute("""
                    SELECT t.*, u.username, u.email
                    FROM api_tokens t
                    JOIN users u ON t.user_id = u.id
                    ORDER BY t.created_at DESC
                """)
                tokens = cur.fetchall()
            return jsonify(tokens)

        @bp.route('/admin/api-tokens', methods=['POST'])
        def admin_create_token():
            self._require_admin_role()
            data = request.get_json()
            
            if not data.get('user_id') or not data.get('name'):
                raise AuthError('user_id and name are required', 400)
            
            expires_in_days = data.get('expires_in_days')
            token = self.create_api_token(data['user_id'], data['name'], expires_in_days)
            
            return jsonify({
                'id': token.id,
                'name': token.name,
                'token': token.get_full_token(),
                'created_at': token.created_at,
                'expires_at': token.expires_at
            }), 201

        @bp.route('/admin/api-tokens/<token_id>', methods=['DELETE'])
        def admin_delete_token(token_id):
            self._require_admin_role()
            
            with self.db.get_cursor() as cur:
                cur.execute("DELETE FROM api_tokens WHERE id = %s", (token_id,))
                if cur.rowcount == 0:
                    raise AuthError('Token not found', 404)
            
            return jsonify({'success': True})

        @bp.route('/admin/invite', methods=['POST'])
        def admin_send_invitation():
            self._require_admin_role()
            data = request.get_json()
            
            if not data.get('email'):
                raise AuthError('Email is required', 400)
            
            # Check if user already exists
            with self.db.get_cursor() as cur:
                cur.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
                if cur.fetchone():
                    raise AuthError('User with this email already exists', 400)
            
            # Send invitation email (placeholder - implement actual email sending)
            invitation_token = str(uuid.uuid4())
            
            # Store invitation in database (you might want to create an invitations table)
            # For now, we'll just return success
            return jsonify({
                'success': True,
                'message': f'Invitation sent to {data["email"]}',
                'invitation_token': invitation_token
            })

        return bp

    def validate_token(self, token):
        try:
            logger.debug(f"Validating token: {token}")
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            logger.debug(f"Token payload: {payload}")
            
            # Check if token has function-based resolution
            if 'f' in payload:
                func_name = payload['f']
                data = payload['data']
                
                # Look up function from registered token resolvers
                if func_name not in self._token_resolvers:
                    raise AuthError(f'Function "{func_name}" not found. Register it using register_token_resolver().', 401)
                
                func = self._token_resolvers[func_name]
                if not callable(func):
                    raise AuthError(f'"{func_name}" is not callable', 401)
                
                # Call function with data
                try:
                    result = func(data)
                except AuthError:
                    raise
                except Exception as e:
                    logger.error(f"Error calling function {func_name}: {str(e)}")
                    raise AuthError(f'Error resolving user data: {str(e)}', 500)
                
                # Validate function return format
                if not isinstance(result, dict):
                    raise AuthError('Function must return a dict', 500)
                if 'user' not in result:
                    raise AuthError('Function must return dict with "user" key', 500)
                if 'roles' not in result:
                    raise AuthError('Function must return dict with "roles" key', 500)
                
                # Ensure roles is a list of strings
                roles = result['roles']
                if not isinstance(roles, list):
                    raise AuthError('roles must be a list', 500)
                
                user = result['user'].copy()
                user['roles'] = roles
                return user
            
            # Check if token has user/roles directly (new format without function)
            if 'user' in payload and 'roles' in payload:
                user = payload['user'].copy()
                roles = payload['roles']
                
                # Normalize roles: if dicts, extract 'name' field
                if isinstance(roles, list) and len(roles) > 0 and isinstance(roles[0], dict):
                    roles = [role['name'] for role in roles if isinstance(role, dict) and 'name' in role]
                
                user['roles'] = roles
                return user
            
            # Fall back to existing format with 'sub' (database lookup)
            if 'sub' not in payload:
                raise AuthError('Invalid token format', 401)
            
            user_id = int(payload['sub'])  # Convert string ID back to integer
            
            # Check cache first
            cache_key = f"user_{user_id}"
            current_time = datetime.utcnow()
            
            if cache_key in self._user_cache:
                cached_data, cache_time = self._user_cache[cache_key]
                if (current_time - cache_time).total_seconds() < self._cache_ttl:
                    logger.debug(f"Returning cached user data for ID: {user_id}")
                    return cached_data.copy()  # Return a copy to avoid modifying cache
            
            # Cache miss or expired, fetch from database
            if not self.db:
                raise AuthError('Database not configured for token validation', 500)
            
            with self.db.get_cursor() as cur:
                cur.execute("""
                    SELECT u.*, r.name as role_name FROM users u
                    LEFT JOIN user_roles ur ON ur.user_id = u.id
                    LEFT JOIN roles r ON ur.role_id = r.id
                    WHERE u.id = %s
                """, (user_id,))
                results = cur.fetchall()
                if not results:
                    logger.error(f"User not found for ID: {user_id}")
                    raise AuthError('User not found', 404)
                
                # Get the first row for user data (all rows will have same user data)
                user = results[0]
                
                # Extract roles from results
                roles = [row['role_name'] for row in results if row['role_name'] is not None]
                user['roles'] = roles

            # Cache the result
            self._user_cache[cache_key] = (user.copy(), current_time)
            
            # Clean up expired cache entries
            self._cleanup_cache()
            
            return user
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token error: {str(e)}")
            raise AuthError('Invalid token', 401)
        except AuthError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during token validation: {str(e)}")
            raise AuthError(str(e), 500)

    def _cleanup_cache(self):
        """Remove expired cache entries."""
        current_time = datetime.utcnow()
        expired_keys = [
            key for key, (_, cache_time) in self._user_cache.items()
            if (current_time - cache_time).total_seconds() >= self._cache_ttl
        ]
        for key in expired_keys:
            del self._user_cache[key]

    def _start_update_thread(self):
        """Start the background thread for processing last_used_at updates."""
        if self._update_thread is None or not self._update_thread.is_alive():
            self._update_thread = threading.Thread(target=self._update_worker, daemon=True)
            self._update_thread.start()
            logger.debug("Started background update thread")

    def _schedule_last_used_update(self, token_id):
        """Schedule a last_used_at update for an API token with 10s delay."""
        with self._update_lock:
            self._last_used_updates[token_id] = time.time()
            logger.debug(f"Scheduled last_used update for token {token_id}")

    def _update_worker(self):
        """Background worker that processes last_used_at updates."""
        while not self._shutdown_event.is_set():
            try:
                current_time = time.time()
                tokens_to_update = []
                
                # Collect tokens that need updating (older than 10 seconds)
                with self._update_lock:
                    for token_id, schedule_time in list(self._last_used_updates.items()):
                        if current_time - schedule_time >= 10:  # 10 second delay
                            tokens_to_update.append(token_id)
                            del self._last_used_updates[token_id]
                
                # Perform batch update
                if tokens_to_update:
                    self._perform_batch_update(tokens_to_update)
                
                # Sleep for a short interval
                time.sleep(10)
                
            except Exception as e:
                logger.error(f"Error in update worker: {e}")
                time.sleep(5)  # Wait longer on error

    def _perform_batch_update(self, token_ids):
        """Perform batch update of last_used_at for multiple tokens."""
        try:
            with self.db.get_cursor() as cur:
                # Update all tokens in a single query
                placeholders = ','.join(['%s'] * len(token_ids))
                cur.execute(f"""
                    UPDATE api_tokens 
                    SET last_used_at = %s
                    WHERE id IN ({placeholders})
                """, [datetime.utcnow()] + token_ids)
                
                logger.debug(f"Updated last_used_at for {len(token_ids)} tokens: {token_ids}")
                
        except Exception as e:
            logger.error(f"Error performing batch update: {e}")

    def shutdown(self):
        """Shutdown the background update thread."""
        self._shutdown_event.set()
        if self._update_thread and self._update_thread.is_alive():
            self._update_thread.join(timeout=5)
            logger.debug("Background update thread shutdown complete")

    def get_current_user(self):
        return self._authenticate_request()

    def _expand_roles(self, roles):
        """Expand roles list to include all implied roles.
        
        Args:
            roles: List of role names
            
        Returns:
            Set of role names including all implied roles
        """
        expanded = set(roles)
        to_process = list(roles)
        
        while to_process:
            role = to_process.pop()
            if role in self.role_implications:
                for implied_role in self.role_implications[role]:
                    if implied_role not in expanded:
                        expanded.add(implied_role)
                        to_process.append(implied_role)
        
        return expanded

    def _require_admin_role(self):
        """Require the current user to have administrator role."""
        user = g.requesting_user
        if not user or 'administrator' not in user.get('roles', []):
            raise AuthError('Administrator role required', 403)

    def get_user_api_tokens(self, user_id):
        """Get all API tokens for a user."""
        with self.db.get_cursor() as cur:
            cur.execute("""
                SELECT id, name, created_at, expires_at, last_used_at
                FROM api_tokens 
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))
            return cur.fetchall()

    def create_api_token(self, user_id, name, expires_in_days=None):
        """Create a new API token for a user."""
        token = ApiToken(user_id, name, expires_in_days)
        
        with self.db.get_cursor() as cur:
            cur.execute("""
                INSERT INTO api_tokens (id, user_id, name, token, created_at, expires_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (token.id, token.user_id, token.name, token.token, token.created_at, token.expires_at))
            return token

    def register_token_resolver(self, name: str, func):
        """Register a function to be used for token resolution.
        
        Args:
            name: Function name (string identifier used in create_jwt_token)
            func: Callable function that takes a dict and returns dict with 'user' and 'roles'
        
        Raises:
            ValueError: If func is not callable
        """
        if not callable(func):
            raise ValueError(f'Function must be callable')
        self._token_resolvers[name] = func
        logger.debug(f"Registered token resolver: {name}")

    def create_jwt_token(self, user_input: dict, f: str = None) -> str:
        """Create a JWT token from user input dict.
        
        Args:
            user_input: Dict containing user and roles data
            f: Optional function name to call during token validation
        
        Returns:
            JWT token string
        
        Raises:
            AuthError: If validation fails or required keys are missing
        """
        if f is None:
            # Validate user_input structure
            if 'user' not in user_input:
                raise AuthError('user_input must contain "user" key', 400)
            if 'roles' not in user_input:
                raise AuthError('user_input must contain "roles" key', 400)
            
            user = user_input['user']
            roles = user_input['roles']
            
            # Validate user dict
            if not isinstance(user, dict):
                raise AuthError('user must be a dict', 400)
            if 'id' not in user:
                raise AuthError('user must contain "id" key', 400)
            if 'username' not in user:
                raise AuthError('user must contain "username" key', 400)
            
            # Validate roles list
            if not isinstance(roles, list):
                raise AuthError('roles must be a list', 400)
            for role in roles:
                if not isinstance(role, dict):
                    raise AuthError('each role must be a dict', 400)
                if 'id' not in role:
                    raise AuthError('each role must contain "id" key', 400)
                if 'name' not in role:
                    raise AuthError('each role must contain "name" key', 400)
            
            # Create JWT payload with user and roles
            payload = {
                'user': user,
                'roles': roles,
                'exp': datetime.utcnow() + self.expiry_time,
                'iat': datetime.utcnow()
            }
        else:
            # Store function name and user_input in payload
            payload = {
                'f': f,
                'data': user_input,
                'exp': datetime.utcnow() + self.expiry_time,
                'iat': datetime.utcnow()
            }
        
        logger.debug(f"Creating JWT token with payload: {payload}")
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        logger.info(f"Created JWT token")
        return token

    def _create_token(self, user):
        payload = {
            'sub': str(user['id']),
            'exp': datetime.utcnow() + self.expiry_time,
            'iat': datetime.utcnow()
        }
        logger.debug(f"Creating token with payload: {payload}")
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        logger.info(f"Created token: {token}")
        return token

    def _create_refresh_token(self, user):
        payload = {
            'sub': str(user['id']),
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')

    def _verify_password(self, password, password_hash):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def _validate_password_strength(self, password, username=None, email=None):
        """Validate password strength and return error message listing all rules and failures."""
        rules = []
        failures = []
        
        # Rule 1: Minimum length
        min_length = 8
        rules.append(f"At least {min_length} characters long")
        if len(password) < min_length:
            failures.append(f"At least {min_length} characters long")
        
        # Rule 2: Maximum length
        max_length = 128
        rules.append(f"No more than {max_length} characters long")
        if len(password) > max_length:
            failures.append(f"No more than {max_length} characters long")
        
        # Rule 3: Uppercase letter
        rules.append("Contains at least one uppercase letter (A-Z)")
        if not re.search(r'[A-Z]', password):
            failures.append("Contains at least one uppercase letter (A-Z)")
        
        # Rule 4: Lowercase letter
        rules.append("Contains at least one lowercase letter (a-z)")
        if not re.search(r'[a-z]', password):
            failures.append("Contains at least one lowercase letter (a-z)")
        
        # Rule 5: Digit
        rules.append("Contains at least one number (0-9)")
        if not re.search(r'\d', password):
            failures.append("Contains at least one number (0-9)")
        
        # Rule 6: Special character
        rules.append("Contains at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            failures.append("Contains at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")
        
        # Rule 7: Not contain username
        if username:
            rules.append("Does not contain your username")
            if username.lower() in password.lower():
                failures.append("Does not contain your username")
        
        # Rule 8: Not contain email username
        if email:
            email_username = email.split('@')[0].lower()
            rules.append("Does not contain your email username")
            if email_username and email_username in password.lower():
                failures.append("Does not contain your email username")
        
        # Rule 9: Not a common password
        common_passwords = {'password', 'password123', '12345678', 'qwerty', 'abc123', 'letmein', 'welcome', 'monkey', '1234567890', 'password1'}
        rules.append("Is not a common password")
        if password.lower() in common_passwords:
            failures.append("Is not a common password")
        
        if failures:
            all_rules_text = "\n".join([f"  {'✗' if rule in failures else '✓'} {rule}" for rule in rules])
            error_msg = f"Password does not meet the following requirements:\n\n{all_rules_text}\n\nPlease fix the issues marked with ✗."
            raise AuthError(error_msg, 400)
        
        return True

    def _get_oauth_url(self, provider, redirect_uri):
        meta = self._get_provider_meta(provider)
        client_id = self.oauth_config[provider]['client_id']
        scope = self.oauth_config[provider].get('scope', meta['default_scope'])
        state = provider  # Pass provider as state for callback
        # Some providers require additional params
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': scope,
            'state': state
        }
        # Facebook requires display; GitHub supports prompt
        if provider == 'facebook':
            params['display'] = 'page'
        # Build URL
        from urllib.parse import urlencode
        return f"{meta['auth_url']}?{urlencode(params)}"

    def _get_oauth_user_info(self, provider, code):
        meta = self._get_provider_meta(provider)
        client_id = self.oauth_config[provider]['client_id']
        client_secret = self.oauth_config[provider]['client_secret']
        redirect_uri = self.get_redirect_uri()


        if provider == 'microsoft':
            import msal
            client = msal.ConfidentialClientApplication(
                client_id, 
                client_credential=client_secret, 
                authority="https://login.microsoftonline.com/common"
            )
            tokens = client.acquire_token_by_authorization_code(
                code, 
                scopes=["email"], 
                redirect_uri=redirect_uri
            )
        else:
            # Standard OAuth flow for other providers
            token_data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
                'scope': meta['default_scope']
            }
            token_headers = {}
            if provider == 'github':
                token_headers['Accept'] = 'application/json'
            token_response = requests.post(meta['token_url'], data=token_data, headers=token_headers)
            logger.info("TOKEN RESPONSE: {} {} {} [[[{}]]]".format(token_response.text, token_response.status_code, token_response.headers, token_data))
            token_response.raise_for_status()
            tokens = token_response.json()


        access_token = tokens.get('access_token') or tokens.get('id_token')
        if not access_token:
            # Some providers return id_token separately but require access_token for userinfo
            access_token = tokens.get('access_token')

        # Build userinfo request
        userinfo_url = meta['userinfo_url']
        userinfo_headers = {'Authorization': f"Bearer {access_token}"}
        if provider == 'facebook':
            # Ensure fields
            from urllib.parse import urlencode
            userinfo_url = f"{userinfo_url}?{urlencode({'fields': 'id,name,email'})}"

        userinfo_response = requests.get(userinfo_url, headers=userinfo_headers)
        userinfo_response.raise_for_status()
        raw_userinfo = userinfo_response.json()

        # Special handling for GitHub missing email
        if provider == 'github' and not raw_userinfo.get('email'):
            emails_resp = requests.get('https://api.github.com/user/emails', headers={**userinfo_headers, 'Accept': 'application/vnd.github+json'})
            if emails_resp.ok:
                emails = emails_resp.json()
                primary = next((e for e in emails if e.get('primary') and e.get('verified')), None)
                raw_userinfo['email'] = (primary or (emails[0] if emails else {})).get('email')




        # Normalize
        norm = self._normalize_userinfo(provider, raw_userinfo)
        if not norm.get('email'):
            # Fallback pseudo-email if allowed
            norm['email'] = f"{norm['sub']}@{provider}.local"

        # Create or update user
        with self.db.get_cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (norm['email'],))
            user = cur.fetchone()

            if not user:
                if not self.allow_oauth_auto_create:
                    raise AuthError('User not found and auto-create disabled', 403)
                # Create new user (auto-create enabled)
                user_obj = User(
                    username=norm['email'],
                    email=norm['email'],
                    real_name=norm.get('name', norm['email']),
                    id_generator=self.db.get_id_generator()
                )
                cur.execute("""
                    INSERT INTO users (username, email, real_name, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (user_obj.username, user_obj.email, user_obj.real_name, 
                      user_obj.created_at, user_obj.updated_at))
                new_id = cur.fetchone()['id']
                user = {'id': new_id, 'username': user_obj.username, 'email': user_obj.email, 
                        'real_name': user_obj.real_name, 'roles': []}
            else:
                # Update existing user
                cur.execute("""
                    UPDATE users 
                    SET real_name = %s, updated_at = %s
                    WHERE email = %s
                """, (norm.get('name', norm['email']), datetime.utcnow(), norm['email']))
                user['real_name'] = norm.get('name', norm['email'])

        return user

    def _get_provider_meta(self, provider):
        providers = {
            'google': {
                'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
                'token_url': 'https://oauth2.googleapis.com/token',
                'userinfo_url': 'https://www.googleapis.com/oauth2/v3/userinfo',
                'default_scope': 'openid email profile'
            },
            'github': {
                'auth_url': 'https://github.com/login/oauth/authorize',
                'token_url': 'https://github.com/login/oauth/access_token',
                'userinfo_url': 'https://api.github.com/user',
                'default_scope': 'read:user user:email'
            },
            'facebook': {
                'auth_url': 'https://www.facebook.com/v11.0/dialog/oauth',
                'token_url': 'https://graph.facebook.com/v11.0/oauth/access_token',
                'userinfo_url': 'https://graph.facebook.com/me',
                'default_scope': 'email public_profile'
            },
            'microsoft': {
                'auth_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
                'token_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
                'userinfo_url': 'https://graph.microsoft.com/oidc/userinfo',
                'default_scope': 'openid email profile'
            },
            'linkedin': {
                'auth_url': 'https://www.linkedin.com/oauth/v2/authorization',
                'token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
                'userinfo_url': 'https://api.linkedin.com/v2/userinfo',
                'default_scope': 'openid profile email'
            },
            'slack': {
                'auth_url': 'https://slack.com/openid/connect/authorize',
                'token_url': 'https://slack.com/api/openid.connect.token',
                'userinfo_url': 'https://slack.com/api/openid.connect.userInfo',
                'default_scope': 'openid profile email'
            },
            'apple': {
                'auth_url': 'https://appleid.apple.com/auth/authorize',
                'token_url': 'https://appleid.apple.com/auth/token',
                'userinfo_url': 'https://appleid.apple.com/auth/userinfo',
                'default_scope': 'name email'
            }
        }
        if provider not in providers:
            raise AuthError('Invalid OAuth provider ' + provider)
        return providers[provider]

    def _normalize_userinfo(self, provider, info):
        # Map into a common structure: sub, email, name
        if provider == 'google':
            return {'sub': info.get('sub'), 'email': info.get('email'), 'name': info.get('name')}
        if provider == 'github':
            return {'sub': str(info.get('id')), 'email': info.get('email'), 'name': info.get('name') or info.get('login')}
        if provider == 'facebook':
            return {'sub': info.get('id'), 'email': info.get('email'), 'name': info.get('name')}
        if provider == 'microsoft':
            # OIDC userinfo
            return {'sub': info.get('sub') or info.get('oid'), 'email': info.get('email') or info.get('preferred_username'), 'name': info.get('name')}
        if provider == 'linkedin':
            return {'sub': info.get('sub') or info.get('id'), 'email': info.get('email'), 'name': info.get('name')}
        if provider == 'slack':
            return {'sub': info.get('sub'), 'email': info.get('email'), 'name': info.get('name')}
        if provider == 'apple':
            # Apple email may be private relay; name not always present
            return {'sub': info.get('sub'), 'email': info.get('email'), 'name': info.get('name')}
        return {'sub': info.get('sub'), 'email': info.get('email'), 'name': info.get('name')}
    
    def _send_email(self, to_email, subject, body):
        if not self.email_server or not self.email_username or not self.email_password:
            logger.error('Email configuration not set, cannot send email')
            raise AuthError('Email configuration not set. Cannot send validation email.', 500)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Reply-To'] = self.email_reply_to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_server, self.email_port)
            server.starttls()
            server.login(self.email_username, self.email_password)
            server.send_message(msg)
            server.quit()
            logger.info(f'Validation email sent to {to_email}')
        except AuthError:
            raise
        except Exception as e:
            logger.error(f'Failed to send email to {to_email}: {e}')
            raise AuthError(f'Failed to send validation email: {str(e)}', 500)
    
    def _get_frontend_url(self):
        frontend_url = os.getenv('FRONTEND_URL')
        if not frontend_url:
            from urllib.parse import urlparse, urlunparse
            redirect_uri = self.get_redirect_uri()
            parsed_uri = urlparse(redirect_uri)
            frontend_url = urlunparse((parsed_uri.scheme, parsed_uri.netloc, '', '', '', ''))
        return frontend_url
