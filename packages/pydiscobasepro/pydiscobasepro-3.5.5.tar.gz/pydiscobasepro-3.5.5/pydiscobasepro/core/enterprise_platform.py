"""
PyDiscoBasePro Enterprise Platform
Multi-tenant enterprise features including RBAC, SAML, audit trails, and governance
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import secrets
import re

from ..core.config import Config
from ..core.audit import AuditLogger
from ..core.rbac import RBACManager
from ..core.secrets_vault import SecretsVault
from ..core.metrics import MetricsCollector

class OrganizationStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class RoleType(Enum):
    SYSTEM = "system"
    ORGANIZATION = "organization"
    CUSTOM = "custom"

@dataclass
class Organization:
    """Organization entity"""
    id: str
    name: str
    domain: str
    status: OrganizationStatus
    created_at: datetime
    updated_at: datetime
    settings: Dict[str, Any]
    metadata: Dict[str, Any]
    parent_org_id: Optional[str] = None
    subscription_tier: str = "free"
    max_users: int = 100
    features: Set[str] = None

    def __post_init__(self):
        if self.features is None:
            self.features = set()

@dataclass
class User:
    """User entity"""
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    status: UserStatus
    organization_id: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    password_hash: str
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    email_verified: bool = False
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Dict[str, Any] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}
        if self.metadata is None:
            self.metadata = {}

@dataclass
class Role:
    """Role entity"""
    id: str
    name: str
    description: str
    type: RoleType
    organization_id: Optional[str]
    permissions: Set[str]
    created_at: datetime
    updated_at: datetime
    is_system: bool = False
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class Permission:
    """Permission entity"""
    id: str
    name: str
    description: str
    resource: str
    action: str
    scope: str  # global, organization, project, resource
    created_at: datetime
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class Policy:
    """Policy entity"""
    id: str
    name: str
    description: str
    type: str  # security, compliance, access, resource
    organization_id: Optional[str]
    rules: List[Dict[str, Any]]
    enforcement_level: str  # monitor, warn, block, remediate
    status: str  # active, inactive, draft
    created_at: datetime
    updated_at: datetime
    created_by: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class AuditEvent:
    """Audit event entity"""
    id: str
    timestamp: datetime
    organization_id: Optional[str]
    user_id: Optional[str]
    action: str
    resource_type: str
    resource_id: Optional[str]
    details: Dict[str, Any]
    ip_address: Optional[str]
    user_agent: Optional[str]
    session_id: Optional[str]
    risk_score: int = 0
    compliance_flags: List[str] = None

    def __post_init__(self):
        if self.compliance_flags is None:
            self.compliance_flags = []

class EnterprisePlatform:
    """Main enterprise platform class"""

    def __init__(self, config: Config):
        self.config = config
        self.audit_logger = AuditLogger()
        self.rbac_manager = RBACManager()
        self.secrets_vault = SecretsVault()
        self.metrics_collector = MetricsCollector()

        # In-memory storage (in production, use database)
        self.organizations: Dict[str, Organization] = {}
        self.users: Dict[str, User] = {}
        self.roles: Dict[str, Role] = {}
        self.permissions: Dict[str, Permission] = {}
        self.policies: Dict[str, Policy] = {}
        self.audit_events: List[AuditEvent] = []

        # SAML/LDAP configuration
        self.saml_config: Dict[str, Any] = {}
        self.ldap_config: Dict[str, Any] = {}

        # SCIM configuration
        self.scim_config: Dict[str, Any] = {}

        # Compliance settings
        self.compliance_settings: Dict[str, Any] = {
            'gdpr_enabled': True,
            'hipaa_enabled': False,
            'sox_enabled': False,
            'pci_dss_enabled': False,
            'data_retention_days': 2555,  # 7 years
            'audit_retention_days': 2555
        }

        # Initialize system roles and permissions
        self._initialize_system_roles()
        self._initialize_system_permissions()

        # Setup background tasks
        self._setup_background_tasks()

    def _initialize_system_roles(self):
        """Initialize system roles"""
        system_roles = [
            {
                'id': 'system_admin',
                'name': 'System Administrator',
                'description': 'Full system access',
                'permissions': ['*']
            },
            {
                'id': 'org_admin',
                'name': 'Organization Administrator',
                'description': 'Organization-level administration',
                'permissions': ['org.*', 'user.*', 'role.*', 'policy.*']
            },
            {
                'id': 'developer',
                'name': 'Developer',
                'description': 'Development and deployment access',
                'permissions': ['project.*', 'deployment.*', 'logs.view']
            },
            {
                'id': 'viewer',
                'name': 'Viewer',
                'description': 'Read-only access',
                'permissions': ['*.view', 'metrics.view']
            }
        ]

        for role_data in system_roles:
            role = Role(
                id=role_data['id'],
                name=role_data['name'],
                description=role_data['description'],
                type=RoleType.SYSTEM,
                organization_id=None,
                permissions=set(role_data['permissions']),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_system=True
            )
            self.roles[role.id] = role

    def _initialize_system_permissions(self):
        """Initialize system permissions"""
        system_permissions = [
            # Organization permissions
            ('org.view', 'View organization details', 'organization', 'read', 'organization'),
            ('org.update', 'Update organization settings', 'organization', 'update', 'organization'),
            ('org.delete', 'Delete organization', 'organization', 'delete', 'organization'),

            # User permissions
            ('user.view', 'View user details', 'user', 'read', 'organization'),
            ('user.create', 'Create users', 'user', 'create', 'organization'),
            ('user.update', 'Update user details', 'user', 'update', 'organization'),
            ('user.delete', 'Delete users', 'user', 'delete', 'organization'),

            # Role permissions
            ('role.view', 'View roles', 'role', 'read', 'organization'),
            ('role.create', 'Create roles', 'role', 'create', 'organization'),
            ('role.update', 'Update roles', 'role', 'update', 'organization'),
            ('role.delete', 'Delete roles', 'role', 'delete', 'organization'),

            # Policy permissions
            ('policy.view', 'View policies', 'policy', 'read', 'organization'),
            ('policy.create', 'Create policies', 'policy', 'create', 'organization'),
            ('policy.update', 'Update policies', 'policy', 'update', 'organization'),
            ('policy.delete', 'Delete policies', 'policy', 'delete', 'organization'),

            # Project permissions
            ('project.view', 'View projects', 'project', 'read', 'organization'),
            ('project.create', 'Create projects', 'project', 'create', 'organization'),
            ('project.update', 'Update projects', 'project', 'update', 'organization'),
            ('project.delete', 'Delete projects', 'project', 'delete', 'organization'),

            # Deployment permissions
            ('deployment.view', 'View deployments', 'deployment', 'read', 'organization'),
            ('deployment.create', 'Create deployments', 'deployment', 'create', 'organization'),
            ('deployment.update', 'Update deployments', 'deployment', 'update', 'organization'),
            ('deployment.approve', 'Approve deployments', 'deployment', 'approve', 'organization'),

            # Security permissions
            ('security.view', 'View security settings', 'security', 'read', 'organization'),
            ('security.update', 'Update security settings', 'security', 'update', 'organization'),
            ('security.scan', 'Run security scans', 'security', 'execute', 'organization'),

            # Audit permissions
            ('audit.view', 'View audit logs', 'audit', 'read', 'organization'),
            ('audit.export', 'Export audit logs', 'audit', 'export', 'organization'),

            # Metrics permissions
            ('metrics.view', 'View metrics', 'metrics', 'read', 'organization'),
            ('metrics.export', 'Export metrics', 'metrics', 'export', 'organization'),
        ]

        for perm_data in system_permissions:
            perm_id, desc, resource, action, scope = perm_data
            permission = Permission(
                id=perm_id,
                name=perm_id,
                description=desc,
                resource=resource,
                action=action,
                scope=scope,
                created_at=datetime.utcnow()
            )
            self.permissions[permission.id] = permission

    def _setup_background_tasks(self):
        """Setup background tasks"""
        asyncio.create_task(self._audit_cleanup_task())
        asyncio.create_task(self._compliance_monitoring_task())
        asyncio.create_task(self._security_monitoring_task())

    # Organization management
    def create_organization(self,
                          name: str,
                          domain: str,
                          admin_email: str,
                          settings: Optional[Dict[str, Any]] = None) -> Organization:
        """Create a new organization"""
        org_id = f"org_{secrets.token_hex(8)}"

        organization = Organization(
            id=org_id,
            name=name,
            domain=domain,
            status=OrganizationStatus.ACTIVE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            settings=settings or {},
            metadata={}
        )

        self.organizations[org_id] = organization

        # Create admin user
        self.create_user(
            email=admin_email,
            username=admin_email.split('@')[0],
            first_name="Admin",
            last_name="User",
            organization_id=org_id,
            role_ids=['org_admin']
        )

        # Log audit event
        self.audit_logger.log_event('organization_created', {
            'organization_id': org_id,
            'organization_name': name,
            'admin_email': admin_email
        })

        return organization

    def update_organization(self, org_id: str, updates: Dict[str, Any]) -> Optional[Organization]:
        """Update organization"""
        org = self.organizations.get(org_id)
        if not org:
            return None

        for key, value in updates.items():
            if hasattr(org, key):
                setattr(org, key, value)

        org.updated_at = datetime.utcnow()
        self.audit_logger.log_event('organization_updated', {
            'organization_id': org_id,
            'updates': updates
        })

        return org

    def delete_organization(self, org_id: str) -> bool:
        """Delete organization (soft delete)"""
        org = self.organizations.get(org_id)
        if not org:
            return False

        org.status = OrganizationStatus.DELETED
        org.updated_at = datetime.utcnow()

        # Mark all users as inactive
        for user in self.users.values():
            if user.organization_id == org_id:
                user.status = UserStatus.INACTIVE

        self.audit_logger.log_event('organization_deleted', {
            'organization_id': org_id
        })

        return True

    # User management
    def create_user(self,
                   email: str,
                   username: str,
                   first_name: str,
                   last_name: str,
                   organization_id: str,
                   role_ids: Optional[List[str]] = None) -> User:
        """Create a new user"""
        user_id = f"user_{secrets.token_hex(8)}"
        password_hash = self._hash_password(secrets.token_hex(16))  # Temporary password

        user = User(
            id=user_id,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            status=UserStatus.PENDING,
            organization_id=organization_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_login=None,
            password_hash=password_hash,
            preferences={},
            metadata={}
        )

        self.users[user_id] = user

        # Assign roles
        if role_ids:
            for role_id in role_ids:
                self.assign_role_to_user(user_id, role_id)

        self.audit_logger.log_event('user_created', {
            'user_id': user_id,
            'organization_id': organization_id,
            'email': email
        })

        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = None
        for u in self.users.values():
            if u.email == email:
                user = u
                break

        if not user or not self._verify_password(password, user.password_hash):
            self.audit_logger.log_event('authentication_failed', {
                'email': email,
                'user_id': user.id if user else None
            })
            return None

        if user.status != UserStatus.ACTIVE:
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        user.updated_at = datetime.utcnow()

        self.audit_logger.log_event('user_authenticated', {
            'user_id': user.id,
            'organization_id': user.organization_id
        })

        return user

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        """Update user"""
        user = self.users.get(user_id)
        if not user:
            return None

        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)

        user.updated_at = datetime.utcnow()

        self.audit_logger.log_event('user_updated', {
            'user_id': user_id,
            'updates': list(updates.keys())
        })

        return user

    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        user = self.users.get(user_id)
        if not user:
            return False

        user.status = UserStatus.INACTIVE
        user.updated_at = datetime.utcnow()

        self.audit_logger.log_event('user_deleted', {
            'user_id': user_id,
            'organization_id': user.organization_id
        })

        return True

    # Role and permission management
    def create_role(self,
                   name: str,
                   description: str,
                   organization_id: Optional[str],
                   permissions: List[str]) -> Role:
        """Create a new role"""
        role_id = f"role_{secrets.token_hex(8)}"

        role = Role(
            id=role_id,
            name=name,
            description=description,
            type=RoleType.ORGANIZATION if organization_id else RoleType.SYSTEM,
            organization_id=organization_id,
            permissions=set(permissions),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_system=False
        )

        self.roles[role_id] = role

        self.audit_logger.log_event('role_created', {
            'role_id': role_id,
            'organization_id': organization_id,
            'permissions': permissions
        })

        return role

    def assign_role_to_user(self, user_id: str, role_id: str) -> bool:
        """Assign role to user"""
        user = self.users.get(user_id)
        role = self.roles.get(role_id)

        if not user or not role:
            return False

        # Check if role belongs to user's organization or is system role
        if role.organization_id and role.organization_id != user.organization_id:
            return False

        success = self.rbac_manager.assign_role(user_id, role_id)

        if success:
            self.audit_logger.log_event('role_assigned', {
                'user_id': user_id,
                'role_id': role_id,
                'organization_id': user.organization_id
            })

        return success

    def revoke_role_from_user(self, user_id: str, role_id: str) -> bool:
        """Revoke role from user"""
        user = self.users.get(user_id)
        if not user:
            return False

        success = self.rbac_manager.revoke_role(user_id, role_id)

        if success:
            self.audit_logger.log_event('role_revoked', {
                'user_id': user_id,
                'role_id': role_id,
                'organization_id': user.organization_id
            })

        return success

    def check_permission(self, user_id: str, permission: str, resource_id: Optional[str] = None) -> bool:
        """Check if user has permission"""
        return self.rbac_manager.check_permission(user_id, permission, resource_id)

    # Policy management
    def create_policy(self,
                     name: str,
                     description: str,
                     policy_type: str,
                     organization_id: Optional[str],
                     rules: List[Dict[str, Any]],
                     enforcement_level: str,
                     created_by: str) -> Policy:
        """Create a new policy"""
        policy_id = f"policy_{secrets.token_hex(8)}"

        policy = Policy(
            id=policy_id,
            name=name,
            description=description,
            type=policy_type,
            organization_id=organization_id,
            rules=rules,
            enforcement_level=enforcement_level,
            status='active',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by=created_by
        )

        self.policies[policy_id] = policy

        self.audit_logger.log_event('policy_created', {
            'policy_id': policy_id,
            'organization_id': organization_id,
            'type': policy_type,
            'created_by': created_by
        })

        return policy

    def evaluate_policy(self, policy_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate policy against context"""
        policy = self.policies.get(policy_id)
        if not policy or policy.status != 'active':
            return {'result': 'allow', 'reason': 'Policy not found or inactive'}

        violations = []
        for rule in policy.rules:
            if self._evaluate_rule(rule, context):
                violations.append({
                    'rule': rule,
                    'context': context
                })

        if violations:
            return {
                'result': policy.enforcement_level,
                'violations': violations,
                'policy_id': policy_id
            }

        return {'result': 'allow', 'policy_id': policy_id}

    def _evaluate_rule(self, rule: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a single policy rule"""
        condition = rule.get('condition', '')
        # Simple condition evaluation - in production, use proper policy engine
        try:
            return eval(condition, {'context': context, '__builtins__': {}})
        except:
            return False

    # SAML/LDAP integration
    def configure_saml(self, config: Dict[str, Any]) -> bool:
        """Configure SAML authentication"""
        required_fields = ['entity_id', 'sso_url', 'x509_cert']
        if not all(field in config for field in required_fields):
            return False

        self.saml_config = config
        self.audit_logger.log_event('saml_configured', {
            'entity_id': config['entity_id']
        })
        return True

    def configure_ldap(self, config: Dict[str, Any]) -> bool:
        """Configure LDAP authentication"""
        required_fields = ['server', 'base_dn', 'bind_dn', 'bind_password']
        if not all(field in config for field in required_fields):
            return False

        self.ldap_config = config
        self.audit_logger.log_event('ldap_configured', {
            'server': config['server']
        })
        return True

    def authenticate_with_saml(self, saml_response: str) -> Optional[User]:
        """Authenticate user with SAML"""
        # SAML authentication implementation would go here
        # For now, return None
        return None

    def authenticate_with_ldap(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with LDAP"""
        # LDAP authentication implementation would go here
        # For now, return None
        return None

    # SCIM integration
    def configure_scim(self, config: Dict[str, Any]) -> bool:
        """Configure SCIM provisioning"""
        self.scim_config = config
        self.audit_logger.log_event('scim_configured', {})
        return True

    # Compliance and audit
    def get_audit_events(self,
                        organization_id: Optional[str] = None,
                        user_id: Optional[str] = None,
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None,
                        limit: int = 100) -> List[AuditEvent]:
        """Get audit events with filtering"""
        events = self.audit_events

        if organization_id:
            events = [e for e in events if e.organization_id == organization_id]

        if user_id:
            events = [e for e in events if e.user_id == user_id]

        if start_date:
            events = [e for e in events if e.timestamp >= start_date]

        if end_date:
            events = [e for e in events if e.timestamp <= end_date]

        return events[-limit:]

    def export_audit_logs(self,
                         organization_id: Optional[str] = None,
                         format: str = 'json') -> str:
        """Export audit logs"""
        events = self.get_audit_events(organization_id=organization_id, limit=10000)

        if format == 'json':
            return json.dumps([asdict(event) for event in events], default=str, indent=2)
        elif format == 'csv':
            # CSV export implementation
            return "CSV format not implemented yet"
        else:
            raise ValueError(f"Unsupported format: {format}")

    def get_compliance_report(self, organization_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate compliance report"""
        events = self.get_audit_events(organization_id=organization_id,
                                     start_date=datetime.utcnow() - timedelta(days=30))

        report = {
            'organization_id': organization_id,
            'period': '30 days',
            'total_events': len(events),
            'security_events': len([e for e in events if 'security' in e.action.lower()]),
            'compliance_violations': len([e for e in events if e.compliance_flags]),
            'high_risk_events': len([e for e in events if e.risk_score >= 7]),
            'recommendations': []
        }

        # Generate recommendations based on events
        if report['security_events'] > 10:
            report['recommendations'].append('Consider implementing additional security measures')

        if report['compliance_violations'] > 0:
            report['recommendations'].append('Review and address compliance violations')

        return report

    # Data residency and retention
    def enforce_data_retention(self):
        """Enforce data retention policies"""
        cutoff_date = datetime.utcnow() - timedelta(days=self.compliance_settings['data_retention_days'])

        # Remove old audit events
        self.audit_events = [e for e in self.audit_events if e.timestamp > cutoff_date]

        # Mark old organizations for deletion
        for org in self.organizations.values():
            if org.updated_at < cutoff_date and org.status == OrganizationStatus.DELETED:
                del self.organizations[org.id]

    def check_data_residency(self, organization_id: str, data_location: str) -> bool:
        """Check if data location complies with organization's residency requirements"""
        org = self.organizations.get(organization_id)
        if not org:
            return False

        required_location = org.settings.get('data_residency', 'any')
        if required_location == 'any':
            return True

        return data_location in required_location

    # Background tasks
    async def _audit_cleanup_task(self):
        """Background task to clean up old audit events"""
        while True:
            try:
                self.enforce_data_retention()
                await asyncio.sleep(86400)  # Run daily
            except Exception as e:
                logging.error(f"Error in audit cleanup task: {e}")
                await asyncio.sleep(3600)

    async def _compliance_monitoring_task(self):
        """Background task for compliance monitoring"""
        while True:
            try:
                # Check for compliance violations
                for org_id, org in self.organizations.items():
                    if org.status == OrganizationStatus.ACTIVE:
                        report = self.get_compliance_report(org_id)
                        if report['compliance_violations'] > 0:
                            self.audit_logger.log_event('compliance_violation_detected', {
                                'organization_id': org_id,
                                'violations': report['compliance_violations']
                            })

                await asyncio.sleep(3600)  # Run hourly
            except Exception as e:
                logging.error(f"Error in compliance monitoring task: {e}")
                await asyncio.sleep(1800)

    async def _security_monitoring_task(self):
        """Background task for security monitoring"""
        while True:
            try:
                # Monitor for suspicious activity
                recent_events = self.get_audit_events(
                    start_date=datetime.utcnow() - timedelta(minutes=5)
                )

                # Check for brute force attempts
                failed_auths = {}
                for event in recent_events:
                    if event.action == 'authentication_failed':
                        ip = event.ip_address or 'unknown'
                        failed_auths[ip] = failed_auths.get(ip, 0) + 1

                for ip, count in failed_auths.items():
                    if count >= 5:  # Threshold for suspicious activity
                        self.audit_logger.log_event('suspicious_activity_detected', {
                            'type': 'brute_force_attempt',
                            'ip_address': ip,
                            'attempts': count
                        })

                await asyncio.sleep(300)  # Run every 5 minutes
            except Exception as e:
                logging.error(f"Error in security monitoring task: {e}")
                await asyncio.sleep(300)

    # Utility methods
    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password"""
        return self._hash_password(password) == password_hash

    # Getters for external access
    def get_organization(self, org_id: str) -> Optional[Organization]:
        """Get organization by ID"""
        return self.organizations.get(org_id)

    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_role(self, role_id: str) -> Optional[Role]:
        """Get role by ID"""
        return self.roles.get(role_id)

    def get_policy(self, policy_id: str) -> Optional[Policy]:
        """Get policy by ID"""
        return self.policies.get(policy_id)

    def list_organizations(self) -> List[Organization]:
        """List all organizations"""
        return list(self.organizations.values())

    def list_users(self, organization_id: Optional[str] = None) -> List[User]:
        """List users, optionally filtered by organization"""
        users = list(self.users.values())
        if organization_id:
            users = [u for u in users if u.organization_id == organization_id]
        return users

    def list_roles(self, organization_id: Optional[str] = None) -> List[Role]:
        """List roles, optionally filtered by organization"""
        roles = list(self.roles.values())
        if organization_id:
            roles = [r for r in roles if r.organization_id == organization_id or r.is_system]
        return roles

    def list_policies(self, organization_id: Optional[str] = None) -> List[Policy]:
        """List policies, optionally filtered by organization"""
        policies = list(self.policies.values())
        if organization_id:
            policies = [p for p in policies if p.organization_id == organization_id]
        return policies