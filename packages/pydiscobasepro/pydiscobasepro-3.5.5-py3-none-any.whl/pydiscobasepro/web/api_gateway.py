"""
PyDiscoBasePro API Gateway
Enterprise-grade API gateway with security, monitoring, and scalability features
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import hmac
import base64
import re

from aiohttp import web, ClientSession, ClientTimeout, ClientError
from aiohttp.web import Request, Response
import aiohttp_cors
import redis.asyncio as redis
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import jwt
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import OpenSSL

from ..core.config import Config
from ..core.metrics import MetricsCollector
from ..core.security import SecurityManager
from ..core.audit import AuditLogger
from ..core.rbac import RBACManager
from ..core.rate_limiter import RateLimiter
from ..core.circuit_breaker import CircuitBreaker

class APIGateway:
    """Enterprise API Gateway for PyDiscoBasePro"""

    def __init__(self, config: Config):
        self.config = config
        self.app = web.Application()
        self.cors = aiohttp_cors.setup(self.app)

        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.security_manager = SecurityManager()
        self.audit_logger = AuditLogger()
        self.rbac_manager = RBACManager()
        self.rate_limiter = RateLimiter()
        self.circuit_breaker = CircuitBreaker()

        # Redis for distributed state
        self.redis = redis.Redis(
            host=config.redis_host,
            port=config.redis_port,
            password=config.redis_password,
            decode_responses=True
        )

        # Setup routes and middleware
        self.setup_routes()
        self.setup_middleware()
        self.setup_cors()

        # Initialize metrics
        self.setup_metrics()

        # Load configuration
        self.routes_config = self.load_routes_config()
        self.upstream_services = self.load_upstream_services()

    def setup_routes(self):
        """Setup API gateway routes"""

        # Health check
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/metrics', self.metrics_endpoint)

        # API routes (these will be dynamically configured)
        self.app.router.add_route('*', '/api/{path:.*}', self.handle_api_request)

        # Admin routes
        self.app.router.add_post('/admin/routes', self.add_route)
        self.app.router.add_delete('/admin/routes/{route_id}', self.remove_route)
        self.app.router.add_get('/admin/routes', self.list_routes)
        self.app.router.add_post('/admin/services', self.register_service)
        self.app.router.add_delete('/admin/services/{service_id}', self.deregister_service)

    def setup_middleware(self):
        """Setup middleware for security, monitoring, etc."""

        @web.middleware
        async def security_middleware(request: Request, handler: Callable):
            """Security middleware with WAF, authentication, authorization"""
            start_time = time.time()

            # Rate limiting
            client_ip = self.get_client_ip(request)
            if not await self.rate_limiter.check_rate_limit(client_ip, request.path):
                return self.create_error_response(429, "Rate limit exceeded")

            # WAF (Web Application Firewall)
            if await self.check_waf_rules(request):
                await self.audit_logger.log_security_event('waf_blocked', {
                    'client_ip': client_ip,
                    'path': request.path,
                    'user_agent': request.headers.get('User-Agent')
                })
                return self.create_error_response(403, "Request blocked by WAF")

            # Authentication
            auth_result = await self.authenticate_request(request)
            if not auth_result['authenticated']:
                return self.create_error_response(401, auth_result.get('error', 'Authentication failed'))

            user_id = auth_result.get('user_id')

            # Authorization
            if not await self.authorize_request(request, user_id):
                await self.audit_logger.log_security_event('unauthorized_access', {
                    'user_id': user_id,
                    'path': request.path,
                    'method': request.method
                })
                return self.create_error_response(403, "Insufficient permissions")

            # Add user context to request
            request['user_id'] = user_id
            request['client_ip'] = client_ip

            try:
                # Call handler
                response = await handler(request)

                # Log successful request
                processing_time = time.time() - start_time
                await self.log_request(request, response, processing_time)

                return response

            except Exception as e:
                # Log error
                processing_time = time.time() - start_time
                await self.log_error(request, e, processing_time)
                return self.create_error_response(500, "Internal server error")

        @web.middleware
        async def circuit_breaker_middleware(request: Request, handler: Callable):
            """Circuit breaker middleware"""
            service_name = self.get_service_name_from_path(request.path)

            if await self.circuit_breaker.is_open(service_name):
                return self.create_error_response(503, "Service temporarily unavailable")

            try:
                response = await handler(request)
                await self.circuit_breaker.record_success(service_name)
                return response
            except Exception as e:
                await self.circuit_breaker.record_failure(service_name)
                raise e

        @web.middleware
        async def metrics_middleware(request: Request, handler: Callable):
            """Metrics collection middleware"""
            self.requests_total.labels(
                method=request.method,
                endpoint=request.path,
                status='processing'
            ).inc()

            start_time = time.time()
            try:
                response = await handler(request)
                processing_time = time.time() - start_time

                self.requests_total.labels(
                    method=request.method,
                    endpoint=request.path,
                    status=str(response.status)
                ).inc()

                self.request_duration.labels(
                    method=request.method,
                    endpoint=request.path
                ).observe(processing_time)

                return response
            except Exception as e:
                processing_time = time.time() - start_time
                self.requests_total.labels(
                    method=request.method,
                    endpoint=request.path,
                    status='error'
                ).inc()
                raise e

        # Add middleware in order
        self.app.middlewares.append(metrics_middleware)
        self.app.middlewares.append(security_middleware)
        self.app.middlewares.append(circuit_breaker_middleware)

    def setup_cors(self):
        """Setup CORS configuration"""
        self.cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
            )
        })

    def setup_metrics(self):
        """Setup Prometheus metrics"""
        self.requests_total = Counter(
            'api_gateway_requests_total',
            'Total number of requests',
            ['method', 'endpoint', 'status']
        )

        self.request_duration = Histogram(
            'api_gateway_request_duration_seconds',
            'Request duration in seconds',
            ['method', 'endpoint']
        )

        self.active_connections = Gauge(
            'api_gateway_active_connections',
            'Number of active connections'
        )

        self.rate_limit_hits = Counter(
            'api_gateway_rate_limit_hits_total',
            'Total number of rate limit hits',
            ['client_ip']
        )

    async def handle_api_request(self, request: Request) -> Response:
        """Handle API requests by routing to appropriate upstream service"""
        path = request.match_info.get('path', '')

        # Find matching route
        route_config = self.find_matching_route(path, request.method)
        if not route_config:
            return self.create_error_response(404, "Route not found")

        # Get upstream service
        service_config = self.upstream_services.get(route_config['service'])
        if not service_config:
            return self.create_error_response(503, "Service unavailable")

        # Transform request
        upstream_request = await self.transform_request(request, route_config)

        # Forward request to upstream
        try:
            response = await self.forward_request(upstream_request, service_config, route_config)
            return response
        except ClientError as e:
            await self.circuit_breaker.record_failure(route_config['service'])
            return self.create_error_response(502, "Bad gateway")
        except asyncio.TimeoutError:
            return self.create_error_response(504, "Gateway timeout")

    async def authenticate_request(self, request: Request) -> Dict[str, Any]:
        """Authenticate incoming request"""
        # Check for API key
        api_key = request.headers.get('X-API-Key')
        if api_key:
            user_id = await self.validate_api_key(api_key)
            if user_id:
                return {'authenticated': True, 'user_id': user_id}

        # Check for JWT token
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]
            try:
                payload = jwt.decode(token, self.config.jwt_secret, algorithms=['HS256'])
                return {'authenticated': True, 'user_id': payload['user_id']}
            except jwt.ExpiredSignatureError:
                return {'authenticated': False, 'error': 'Token expired'}
            except jwt.InvalidTokenError:
                return {'authenticated': False, 'error': 'Invalid token'}

        # Check for mTLS client certificate
        if request.transport and hasattr(request.transport, 'get_extra_info'):
            ssl_object = request.transport.get_extra_info('ssl_object')
            if ssl_object:
                cert = ssl_object.getpeercert()
                if cert:
                    user_id = await self.validate_client_certificate(cert)
                    if user_id:
                        return {'authenticated': True, 'user_id': user_id}

        return {'authenticated': False, 'error': 'No valid authentication provided'}

    async def authorize_request(self, request: Request, user_id: str) -> bool:
        """Authorize request based on user permissions"""
        path = request.path
        method = request.method

        # Get required permissions for this endpoint
        required_permissions = await self.get_endpoint_permissions(path, method)

        # Check if user has required permissions
        user_permissions = await self.rbac_manager.get_user_permissions(user_id)

        return all(perm in user_permissions for perm in required_permissions)

    async def check_waf_rules(self, request: Request) -> bool:
        """Check Web Application Firewall rules"""
        # SQL injection patterns
        sql_patterns = [
            r'union\s+select',
            r';\s*drop\s+table',
            r';\s*delete\s+from',
            r'--',
            r'/\*.*\*/'
        ]

        # XSS patterns
        xss_patterns = [
            r'<script',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe',
            r'<object'
        ]

        # Check query parameters and body
        check_text = str(request.query) + str(await request.text())

        for pattern in sql_patterns + xss_patterns:
            if re.search(pattern, check_text, re.IGNORECASE):
                return True

        # Check for suspicious headers
        suspicious_headers = ['X-Forwarded-For', 'X-Real-IP']
        for header in suspicious_headers:
            if header in request.headers:
                # Additional validation could be added here
                pass

        return False

    async def forward_request(self, request: Request, service_config: Dict, route_config: Dict) -> Response:
        """Forward request to upstream service"""
        upstream_url = f"{service_config['url']}{request.path}"

        # Add service-specific headers
        headers = dict(request.headers)
        headers['X-Forwarded-By'] = 'PyDiscoBasePro-API-Gateway'
        headers['X-Client-IP'] = request['client_ip']

        # Remove hop-by-hop headers
        hop_by_hop_headers = [
            'connection', 'keep-alive', 'proxy-authenticate',
            'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade'
        ]
        for header in hop_by_hop_headers:
            headers.pop(header, None)

        timeout = ClientTimeout(total=service_config.get('timeout', 30))

        async with ClientSession(timeout=timeout) as session:
            try:
                async with session.request(
                    request.method,
                    upstream_url,
                    headers=headers,
                    data=await request.read() if request.body_exists else None,
                    params=request.query
                ) as upstream_response:

                    # Transform response
                    response_data = await upstream_response.read()
                    response_headers = dict(upstream_response.headers)

                    # Add gateway headers
                    response_headers['X-API-Gateway'] = 'PyDiscoBasePro'

                    return Response(
                        status=upstream_response.status,
                        headers=response_headers,
                        body=response_data
                    )

            except asyncio.TimeoutError:
                raise
            except Exception as e:
                await self.audit_logger.log_error('upstream_request_failed', {
                    'service': service_config['name'],
                    'url': upstream_url,
                    'error': str(e)
                })
                raise

    async def transform_request(self, request: Request, route_config: Dict) -> Request:
        """Transform request according to route configuration"""
        # Apply route-specific transformations
        if 'transformations' in route_config:
            for transformation in route_config['transformations']:
                if transformation['type'] == 'header':
                    if transformation['action'] == 'add':
                        request.headers[transformation['name']] = transformation['value']
                    elif transformation['action'] == 'remove':
                        request.headers.pop(transformation['name'], None)

        return request

    async def validate_api_key(self, api_key: str) -> Optional[str]:
        """Validate API key and return user ID"""
        # Check Redis cache first
        cached_user = await self.redis.get(f"api_key:{api_key}")
        if cached_user:
            return cached_user

        # Validate against database/service
        # In production, this would check a database or auth service
        if api_key.startswith('pk_'):
            user_id = api_key[3:]  # Simple extraction for demo
            await self.redis.setex(f"api_key:{api_key}", 3600, user_id)  # Cache for 1 hour
            return user_id

        return None

    async def validate_client_certificate(self, cert: Dict) -> Optional[str]:
        """Validate client certificate for mTLS"""
        try:
            # Extract subject from certificate
            subject = cert.get('subject', [])
            common_name = None
            for item in subject:
                if item[0][0] == 'commonName':
                    common_name = item[0][1]
                    break

            if common_name:
                # Validate certificate against CA
                # In production, this would verify the certificate chain
                return common_name

        except Exception as e:
            await self.audit_logger.log_error('certificate_validation_failed', {
                'error': str(e)
            })

        return None

    async def get_endpoint_permissions(self, path: str, method: str) -> List[str]:
        """Get required permissions for endpoint"""
        # This would be configured per endpoint
        # For demo purposes, return basic permissions
        if path.startswith('/api/admin'):
            return ['admin']
        elif path.startswith('/api/metrics'):
            return ['view_metrics']
        elif path.startswith('/api/secrets'):
            return ['manage_secrets']
        else:
            return ['api_access']

    def find_matching_route(self, path: str, method: str) -> Optional[Dict]:
        """Find matching route configuration"""
        for route in self.routes_config:
            if re.match(route['pattern'], path) and method in route['methods']:
                return route
        return None

    def get_service_name_from_path(self, path: str) -> str:
        """Extract service name from path"""
        # Simple implementation - in production, this would be more sophisticated
        parts = path.split('/')
        if len(parts) > 2:
            return parts[2]  # e.g., /api/users -> users
        return 'default'

    def get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded headers
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()

        real_ip = request.headers.get('X-Real-IP')
        if real_ip:
            return real_ip

        # Fallback to remote address
        return request.remote or 'unknown'

    def create_error_response(self, status: int, message: str) -> Response:
        """Create standardized error response"""
        return web.json_response({
            'error': {
                'code': status,
                'message': message,
                'timestamp': datetime.utcnow().isoformat()
            }
        }, status=status)

    async def log_request(self, request: Request, response: Response, processing_time: float):
        """Log successful request"""
        await self.audit_logger.log_event('api_request', {
            'method': request.method,
            'path': request.path,
            'status': response.status,
            'user_id': request.get('user_id'),
            'client_ip': request.get('client_ip'),
            'processing_time': processing_time,
            'user_agent': request.headers.get('User-Agent')
        })

    async def log_error(self, request: Request, error: Exception, processing_time: float):
        """Log request error"""
        await self.audit_logger.log_error('api_request_error', {
            'method': request.method,
            'path': request.path,
            'error': str(error),
            'user_id': request.get('user_id'),
            'client_ip': request.get('client_ip'),
            'processing_time': processing_time
        })

    # Health check endpoint
    async def health_check(self, request: Request) -> Response:
        """Health check endpoint"""
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '3.5.0',
            'services': {}
        }

        # Check upstream services
        for service_name, service_config in self.upstream_services.items():
            try:
                async with ClientSession(timeout=ClientTimeout(total=5)) as session:
                    async with session.get(f"{service_config['url']}/health") as response:
                        health_status['services'][service_name] = {
                            'status': 'healthy' if response.status == 200 else 'unhealthy',
                            'response_time': response.headers.get('X-Response-Time', 'unknown')
                        }
            except Exception:
                health_status['services'][service_name] = {'status': 'unreachable'}

        return web.json_response(health_status)

    # Metrics endpoint
    async def metrics_endpoint(self, request: Request) -> Response:
        """Prometheus metrics endpoint"""
        return web.Response(
            text=generate_latest(),
            content_type='text/plain; charset=utf-8'
        )

    # Admin endpoints
    async def add_route(self, request: Request) -> Response:
        """Add new route configuration"""
        route_data = await request.json()

        # Validate route data
        required_fields = ['pattern', 'service', 'methods']
        if not all(field in route_data for field in required_fields):
            return self.create_error_response(400, "Missing required fields")

        # Add route
        route_data['id'] = str(len(self.routes_config) + 1)
        self.routes_config.append(route_data)

        # Save to Redis for distributed config
        await self.redis.set(f"route:{route_data['id']}", json.dumps(route_data))

        return web.json_response({'status': 'success', 'route_id': route_data['id']})

    async def remove_route(self, request: Request) -> Response:
        """Remove route configuration"""
        route_id = request.match_info.get('route_id')

        # Remove from local config
        self.routes_config = [r for r in self.routes_config if r.get('id') != route_id]

        # Remove from Redis
        await self.redis.delete(f"route:{route_id}")

        return web.json_response({'status': 'success'})

    async def list_routes(self, request: Request) -> Response:
        """List all routes"""
        return web.json_response({'routes': self.routes_config})

    async def register_service(self, request: Request) -> Response:
        """Register new upstream service"""
        service_data = await request.json()

        required_fields = ['name', 'url']
        if not all(field in service_data for field in required_fields):
            return self.create_error_response(400, "Missing required fields")

        service_id = service_data['name']
        self.upstream_services[service_id] = service_data

        # Save to Redis
        await self.redis.set(f"service:{service_id}", json.dumps(service_data))

        return web.json_response({'status': 'success', 'service_id': service_id})

    async def deregister_service(self, request: Request) -> Response:
        """Deregister upstream service"""
        service_id = request.match_info.get('service_id')

        if service_id in self.upstream_services:
            del self.upstream_services[service_id]
            await self.redis.delete(f"service:{service_id}")
            return web.json_response({'status': 'success'})
        else:
            return self.create_error_response(404, "Service not found")

    def load_routes_config(self) -> List[Dict]:
        """Load route configuration"""
        # In production, this would load from database/Redis
        return [
            {
                'id': '1',
                'pattern': r'/api/v1/users.*',
                'service': 'user-service',
                'methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'transformations': []
            },
            {
                'id': '2',
                'pattern': r'/api/v1/metrics.*',
                'service': 'metrics-service',
                'methods': ['GET'],
                'transformations': []
            },
            {
                'id': '3',
                'pattern': r'/api/v1/plugins.*',
                'service': 'plugin-service',
                'methods': ['GET', 'POST', 'PUT', 'DELETE'],
                'transformations': []
            }
        ]

    def load_upstream_services(self) -> Dict[str, Dict]:
        """Load upstream service configuration"""
        # In production, this would load from service discovery
        return {
            'user-service': {
                'name': 'user-service',
                'url': 'http://localhost:8081',
                'timeout': 30,
                'health_check': '/health'
            },
            'metrics-service': {
                'name': 'metrics-service',
                'url': 'http://localhost:8082',
                'timeout': 30,
                'health_check': '/health'
            },
            'plugin-service': {
                'name': 'plugin-service',
                'url': 'http://localhost:8083',
                'timeout': 30,
                'health_check': '/health'
            }
        }

    def run(self, host: str = '0.0.0.0', port: int = 8080):
        """Run the API gateway"""
        print(f"Starting PyDiscoBasePro API Gateway on {host}:{port}")
        web.run_app(self.app, host=host, port=port)

    async def cleanup(self):
        """Cleanup resources"""
        await self.redis.close()