"""
PyDiscoBasePro Web Dashboard
Enterprise-grade web interface for managing Discord bots
"""

import os
import json
import asyncio
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from functools import wraps

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

from ..core.config import Config
from ..core.metrics import MetricsCollector
from ..core.plugins import PluginManager
from ..core.security import SecurityManager
from ..core.audit import AuditLogger
from ..core.rbac import RBACManager
from ..core.secrets_vault import SecretsVault
from ..core.workflow_engine import WorkflowEngine
from ..core.kubernetes_manager import KubernetesManager
from ..core.docker_manager import DockerManager

class User(UserMixin):
    """User model for Flask-Login"""

    def __init__(self, user_id: str, username: str, email: str, role: str, permissions: List[str]):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role
        self.permissions = permissions

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')

class UserForm(FlaskForm):
    """User management form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('viewer', 'Viewer')
    ])
    password = PasswordField('Password', validators=[Length(min=8)])

class PluginForm(FlaskForm):
    """Plugin management form"""
    name = StringField('Plugin Name', validators=[DataRequired()])
    version = StringField('Version', validators=[DataRequired()])
    description = TextAreaField('Description')
    category = SelectField('Category', choices=[
        ('security', 'Security'),
        ('monitoring', 'Monitoring'),
        ('automation', 'Automation'),
        ('integration', 'Integration'),
        ('utility', 'Utility')
    ])

class WebDashboard:
    """Main web dashboard application"""

    def __init__(self, config: Config):
        self.config = config
        self.app = Flask(__name__,
                        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                        static_folder=os.path.join(os.path.dirname(__file__), 'static'))

        # Configure Flask
        self.app.config['SECRET_KEY'] = secrets.token_hex(32)
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

        # Initialize SocketIO
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", async_mode='threading')

        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.plugin_manager = PluginManager()
        self.security_manager = SecurityManager()
        self.audit_logger = AuditLogger()
        self.rbac_manager = RBACManager()
        self.secrets_vault = SecretsVault()
        self.workflow_engine = WorkflowEngine()
        self.kubernetes_manager = KubernetesManager()
        self.docker_manager = DockerManager()

        # Initialize Flask-Login
        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = 'login'

        # Setup routes and handlers
        self.setup_routes()
        self.setup_socket_handlers()
        self.setup_login_manager()

        # Load users (in production, this would be from a database)
        self.users = self.load_users()

    def setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/')
        @login_required
        def index():
            return render_template('dashboard.html',
                                 user=current_user,
                                 metrics=self.get_dashboard_metrics())

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if current_user.is_authenticated:
                return redirect(url_for('index'))

            form = LoginForm()
            if form.validate_on_submit():
                user = self.authenticate_user(form.username.data, form.password.data)
                if user:
                    login_user(user, remember=form.remember.data)
                    self.audit_logger.log_event('user_login', {
                        'user_id': user.id,
                        'username': user.username,
                        'ip_address': request.remote_addr
                    })
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('index'))
                else:
                    flash('Invalid username or password', 'error')
            return render_template('login.html', form=form)

        @self.app.route('/logout')
        @login_required
        def logout():
            self.audit_logger.log_event('user_logout', {
                'user_id': current_user.id,
                'username': current_user.username
            })
            logout_user()
            return redirect(url_for('login'))

        @self.app.route('/api/metrics')
        @login_required
        @self.require_permission('view_metrics')
        def api_metrics():
            return jsonify(self.metrics_collector.get_all_metrics())

        @self.app.route('/api/plugins')
        @login_required
        @self.require_permission('view_plugins')
        def api_plugins():
            return jsonify(self.plugin_manager.get_all_plugins())

        @self.app.route('/api/workflows')
        @login_required
        @self.require_permission('view_workflows')
        def api_workflows():
            return jsonify(self.workflow_engine.get_all_workflows())

        @self.app.route('/api/kubernetes/status')
        @login_required
        @self.require_permission('view_kubernetes')
        def api_kubernetes_status():
            return jsonify(self.kubernetes_manager.get_status())

        @self.app.route('/api/docker/status')
        @login_required
        @self.require_permission('view_docker')
        def api_docker_status():
            return jsonify(self.docker_manager.get_status())

        @self.app.route('/api/secrets')
        @login_required
        @self.require_permission('view_secrets')
        def api_secrets():
            return jsonify(self.secrets_vault.get_secrets_list())

        @self.app.route('/api/audit/logs')
        @login_required
        @self.require_permission('view_audit')
        def api_audit_logs():
            return jsonify(self.audit_logger.get_recent_logs())

        @self.app.route('/api/users')
        @login_required
        @self.require_permission('manage_users')
        def api_users():
            return jsonify(self.get_users_list())

        @self.app.route('/admin/users', methods=['GET', 'POST'])
        @login_required
        @self.require_permission('manage_users')
        def admin_users():
            form = UserForm()
            if form.validate_on_submit():
                self.create_user(form)
                flash('User created successfully', 'success')
                return redirect(url_for('admin_users'))

            return render_template('admin/users.html',
                                 form=form,
                                 users=self.users.values())

        @self.app.route('/admin/plugins', methods=['GET', 'POST'])
        @login_required
        @self.require_permission('manage_plugins')
        def admin_plugins():
            form = PluginForm()
            if form.validate_on_submit():
                self.install_plugin(form)
                flash('Plugin installed successfully', 'success')
                return redirect(url_for('admin_plugins'))

            return render_template('admin/plugins.html',
                                 form=form,
                                 plugins=self.plugin_manager.get_all_plugins())

        @self.app.route('/monitoring')
        @login_required
        @self.require_permission('view_metrics')
        def monitoring():
            return render_template('monitoring.html',
                                 metrics=self.metrics_collector.get_all_metrics())

        @self.app.route('/security')
        @login_required
        @self.require_permission('view_security')
        def security():
            return render_template('security.html',
                                 security_status=self.security_manager.get_status(),
                                 audit_logs=self.audit_logger.get_recent_logs())

        @self.app.route('/workflows')
        @login_required
        @self.require_permission('view_workflows')
        def workflows():
            return render_template('workflows.html',
                                 workflows=self.workflow_engine.get_all_workflows())

        @self.app.route('/kubernetes')
        @login_required
        @self.require_permission('view_kubernetes')
        def kubernetes():
            return render_template('kubernetes.html',
                                 status=self.kubernetes_manager.get_status())

        @self.app.route('/docker')
        @login_required
        @self.require_permission('view_docker')
        def docker():
            return render_template('docker.html',
                                 status=self.docker_manager.get_status())

    def setup_socket_handlers(self):
        """Setup SocketIO event handlers"""

        @self.socketio.on('connect')
        @login_required
        def handle_connect():
            join_room('metrics')
            join_room('logs')
            join_room('alerts')
            emit('connected', {'status': 'connected'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            leave_room('metrics')
            leave_room('logs')
            leave_room('alerts')

        @self.socketio.on('subscribe_metrics')
        @login_required
        def handle_subscribe_metrics():
            join_room('metrics')

        @self.socketio.on('unsubscribe_metrics')
        def handle_unsubscribe_metrics():
            leave_room('metrics')

        @self.socketio.on('get_realtime_metrics')
        @login_required
        def handle_get_realtime_metrics():
            emit('metrics_update', self.metrics_collector.get_realtime_metrics())

    def setup_login_manager(self):
        """Setup Flask-Login user loader"""

        @self.login_manager.user_loader
        def load_user(user_id):
            return self.users.get(user_id)

    def require_permission(self, permission: str):
        """Decorator to require specific permissions"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not current_user.is_authenticated:
                    return self.app.login_manager.unauthorized()

                if permission not in current_user.permissions:
                    return jsonify({'error': 'Insufficient permissions'}), 403

                return f(*args, **kwargs)
            return decorated_function
        return decorator

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user_data = self.users.get(username)
        if user_data and check_password_hash(user_data.get('password_hash', ''), password):
            permissions = self.rbac_manager.get_user_permissions(username)
            return User(
                user_id=username,
                username=username,
                email=user_data.get('email', ''),
                role=user_data.get('role', 'viewer'),
                permissions=permissions
            )
        return None

    def load_users(self) -> Dict[str, Dict[str, Any]]:
        """Load users from storage"""
        # In production, this would load from a database
        return {
            'admin': {
                'password_hash': generate_password_hash('admin123'),
                'email': 'admin@pydiscobasepro.com',
                'role': 'admin'
            },
            'manager': {
                'password_hash': generate_password_hash('manager123'),
                'email': 'manager@pydiscobasepro.com',
                'role': 'manager'
            },
            'developer': {
                'password_hash': generate_password_hash('dev123'),
                'email': 'dev@pydiscobasepro.com',
                'role': 'developer'
            }
        }

    def create_user(self, form: UserForm):
        """Create a new user"""
        username = form.username.data
        if username in self.users:
            raise ValueError('User already exists')

        self.users[username] = {
            'password_hash': generate_password_hash(form.password.data),
            'email': form.email.data,
            'role': form.role.data
        }

        self.rbac_manager.assign_role(username, form.role.data)
        self.audit_logger.log_event('user_created', {
            'created_by': current_user.username,
            'new_user': username,
            'role': form.role.data
        })

    def install_plugin(self, form: PluginForm):
        """Install a plugin"""
        plugin_data = {
            'name': form.name.data,
            'version': form.version.data,
            'description': form.description.data,
            'category': form.category.data
        }

        self.plugin_manager.install_plugin(plugin_data)
        self.audit_logger.log_event('plugin_installed', {
            'installed_by': current_user.username,
            'plugin_name': form.name.data,
            'version': form.version.data
        })

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get metrics for dashboard display"""
        return {
            'system': self.metrics_collector.get_system_metrics(),
            'application': self.metrics_collector.get_application_metrics(),
            'security': self.security_manager.get_security_metrics(),
            'plugins': len(self.plugin_manager.get_all_plugins()),
            'workflows': len(self.workflow_engine.get_all_workflows()),
            'users': len(self.users)
        }

    def get_users_list(self) -> List[Dict[str, Any]]:
        """Get list of users for admin interface"""
        return [
            {
                'username': username,
                'email': user_data.get('email'),
                'role': user_data.get('role'),
                'last_login': user_data.get('last_login')
            }
            for username, user_data in self.users.items()
        ]

    def run(self, host: str = '0.0.0.0', port: int = 8080, debug: bool = False):
        """Run the web dashboard"""
        print(f"Starting PyDiscoBasePro Web Dashboard on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)

    async def start_background_tasks(self):
        """Start background tasks for real-time updates"""
        asyncio.create_task(self.metrics_update_loop())
        asyncio.create_task(self.security_monitoring_loop())

    async def metrics_update_loop(self):
        """Background task to update metrics"""
        while True:
            try:
                metrics = self.metrics_collector.get_realtime_metrics()
                self.socketio.emit('metrics_update', metrics, room='metrics')
                await asyncio.sleep(5)  # Update every 5 seconds
            except Exception as e:
                print(f"Error in metrics update loop: {e}")
                await asyncio.sleep(30)

    async def security_monitoring_loop(self):
        """Background task for security monitoring"""
        while True:
            try:
                alerts = self.security_manager.check_for_alerts()
                if alerts:
                    self.socketio.emit('security_alerts', alerts, room='alerts')
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Error in security monitoring loop: {e}")
                await asyncio.sleep(300)