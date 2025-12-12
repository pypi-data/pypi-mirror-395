"""
PyDiscoBasePro Chaos Engineering, Forensics, Reliability & Compliance Systems
Advanced systems for testing resilience, investigating incidents, and ensuring compliance
"""

import asyncio
import json
import logging
import time
import random
import hashlib
import secrets
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import psutil
import os
import subprocess
from pathlib import Path

from ..core.config import Config
from ..core.metrics import MetricsCollector
from ..core.audit import AuditLogger

class ChaosExperimentType(Enum):
    LATENCY_INJECTION = "latency_injection"
    FAILURE_INJECTION = "failure_injection"
    CPU_STRESS = "cpu_stress"
    MEMORY_STRESS = "memory_stress"
    DISK_STRESS = "disk_stress"
    NETWORK_PARTITION = "network_partition"
    PROCESS_KILL = "process_kill"
    DEPENDENCY_FAILURE = "dependency_failure"

class ChaosExperimentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"

class ForensicsEventType(Enum):
    SECURITY_INCIDENT = "security_incident"
    SYSTEM_CRASH = "system_crash"
    DATA_BREACH = "data_breach"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    CONFIGURATION_CHANGE = "configuration_change"
    PERFORMANCE_DEGRADATION = "performance_degradation"

class ComplianceFramework(Enum):
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOX = "sox"
    PCI_DSS = "pci_dss"
    ISO_27001 = "iso_27001"
    NIST = "nist"

@dataclass
class ChaosExperiment:
    """Chaos experiment definition"""
    id: str
    name: str
    description: str
    type: ChaosExperimentType
    target: str  # service, host, or resource identifier
    parameters: Dict[str, Any]
    duration: int  # seconds
    status: ChaosExperimentStatus
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    results: Dict[str, Any]
    safety_checks: List[Dict[str, Any]]
    rollback_plan: Dict[str, Any]

@dataclass
class ForensicsSnapshot:
    """Forensic snapshot of system state"""
    id: str
    timestamp: datetime
    event_type: ForensicsEventType
    description: str
    system_state: Dict[str, Any]
    process_list: List[Dict[str, Any]]
    network_connections: List[Dict[str, Any]]
    file_system_state: Dict[str, Any]
    memory_dump: Optional[bytes]
    logs: List[Dict[str, Any]]
    evidence_chain: List[Dict[str, Any]]

@dataclass
class ReliabilityMetric:
    """Reliability metric"""
    name: str
    value: float
    timestamp: datetime
    service: str
    threshold: float
    status: str  # healthy, warning, critical

@dataclass
class ComplianceCheck:
    """Compliance check result"""
    id: str
    framework: ComplianceFramework
    control: str
    description: str
    status: str  # compliant, non_compliant, not_applicable
    severity: str  # low, medium, high, critical
    evidence: List[Dict[str, Any]]
    remediation: str
    checked_at: datetime
    next_check: datetime

class ChaosEngineeringEngine:
    """Chaos engineering engine for testing system resilience"""

    def __init__(self, config: Config):
        self.config = config
        self.experiments: Dict[str, ChaosExperiment] = {}
        self.active_experiments: Set[str] = set()
        self.safety_limits = {
            'max_cpu_stress': 80.0,  # Max CPU usage %
            'max_memory_stress': 85.0,  # Max memory usage %
            'max_latency_injection': 5000,  # Max latency in ms
            'max_failure_rate': 50.0,  # Max failure rate %
            'min_services_running': 3  # Minimum services that must remain running
        }

    def create_experiment(self,
                         name: str,
                         description: str,
                         experiment_type: ChaosExperimentType,
                         target: str,
                         parameters: Dict[str, Any],
                         duration: int,
                         safety_checks: Optional[List[Dict[str, Any]]] = None,
                         rollback_plan: Optional[Dict[str, Any]] = None) -> ChaosExperiment:
        """Create a new chaos experiment"""
        experiment_id = f"chaos_{secrets.token_hex(8)}"

        experiment = ChaosExperiment(
            id=experiment_id,
            name=name,
            description=description,
            type=experiment_type,
            target=target,
            parameters=parameters,
            duration=duration,
            status=ChaosExperimentStatus.PENDING,
            created_at=datetime.utcnow(),
            started_at=None,
            completed_at=None,
            results={},
            safety_checks=safety_checks or self._default_safety_checks(),
            rollback_plan=rollback_plan or {}
        )

        self.experiments[experiment_id] = experiment
        return experiment

    async def run_experiment(self, experiment_id: str) -> Dict[str, Any]:
        """Run a chaos experiment"""
        experiment = self.experiments.get(experiment_id)
        if not experiment:
            raise ValueError(f"Experiment {experiment_id} not found")

        if experiment.status != ChaosExperimentStatus.PENDING:
            raise ValueError(f"Experiment {experiment_id} is not in pending state")

        # Pre-flight safety checks
        if not await self._run_safety_checks(experiment):
            experiment.status = ChaosExperimentStatus.FAILED
            experiment.results['error'] = 'Safety checks failed'
            return experiment.results

        experiment.status = ChaosExperimentStatus.RUNNING
        experiment.started_at = datetime.utcnow()
        self.active_experiments.add(experiment_id)

        try:
            # Execute the experiment
            results = await self._execute_experiment(experiment)

            # Wait for duration
            await asyncio.sleep(experiment.duration)

            # Run rollback if specified
            if experiment.rollback_plan:
                await self._execute_rollback(experiment)

            experiment.status = ChaosExperimentStatus.COMPLETED
            experiment.completed_at = datetime.utcnow()
            experiment.results = results

        except Exception as e:
            experiment.status = ChaosExperimentStatus.FAILED
            experiment.results['error'] = str(e)
            experiment.completed_at = datetime.utcnow()

            # Emergency rollback
            try:
                await self._execute_rollback(experiment)
            except Exception as rollback_error:
                logging.error(f"Rollback failed for experiment {experiment_id}: {rollback_error}")

        finally:
            self.active_experiments.discard(experiment_id)

        return experiment.results

    async def stop_experiment(self, experiment_id: str) -> bool:
        """Stop a running experiment"""
        experiment = self.experiments.get(experiment_id)
        if not experiment or experiment.status != ChaosExperimentStatus.RUNNING:
            return False

        experiment.status = ChaosExperimentStatus.STOPPED
        experiment.completed_at = datetime.utcnow()

        # Execute rollback
        try:
            await self._execute_rollback(experiment)
        except Exception as e:
            logging.error(f"Rollback failed for experiment {experiment_id}: {e}")

        self.active_experiments.discard(experiment_id)
        return True

    async def _execute_experiment(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Execute the actual chaos experiment"""
        if experiment.type == ChaosExperimentType.LATENCY_INJECTION:
            return await self._inject_latency(experiment)
        elif experiment.type == ChaosExperimentType.FAILURE_INJECTION:
            return await self._inject_failure(experiment)
        elif experiment.type == ChaosExperimentType.CPU_STRESS:
            return await self._inject_cpu_stress(experiment)
        elif experiment.type == ChaosExperimentType.MEMORY_STRESS:
            return await self._inject_memory_stress(experiment)
        elif experiment.type == ChaosExperimentType.DISK_STRESS:
            return await self._inject_disk_stress(experiment)
        elif experiment.type == ChaosExperimentType.NETWORK_PARTITION:
            return await self._inject_network_partition(experiment)
        elif experiment.type == ChaosExperimentType.PROCESS_KILL:
            return await self._kill_process(experiment)
        elif experiment.type == ChaosExperimentType.DEPENDENCY_FAILURE:
            return await self._inject_dependency_failure(experiment)
        else:
            raise ValueError(f"Unsupported experiment type: {experiment.type}")

    async def _inject_latency(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Inject latency into service calls"""
        latency_ms = experiment.parameters.get('latency_ms', 1000)
        service = experiment.target

        # Implementation would modify service configuration or use service mesh
        # For demo, we'll simulate the effect
        return {
            'latency_injected': latency_ms,
            'service': service,
            'method': 'configuration_update'
        }

    async def _inject_failure(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Inject failures into service calls"""
        failure_rate = experiment.parameters.get('failure_rate', 10.0)
        service = experiment.target

        # Implementation would modify service behavior
        return {
            'failure_rate_injected': failure_rate,
            'service': service,
            'method': 'circuit_breaker_modification'
        }

    async def _inject_cpu_stress(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Inject CPU stress"""
        target_cpu = experiment.parameters.get('target_cpu', 80.0)

        # Start CPU stress process
        stress_command = f"stress --cpu 4 --timeout {experiment.duration}"
        process = await asyncio.create_subprocess_shell(
            stress_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await process.wait()

        return {
            'target_cpu': target_cpu,
            'actual_cpu': psutil.cpu_percent(),
            'method': 'stress_process'
        }

    async def _inject_memory_stress(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Inject memory stress"""
        target_memory_mb = experiment.parameters.get('target_memory_mb', 1024)

        # Start memory stress process
        stress_command = f"stress --vm 2 --vm-bytes {target_memory_mb}M --timeout {experiment.duration}"
        process = await asyncio.create_subprocess_shell(
            stress_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await process.wait()

        memory = psutil.virtual_memory()
        return {
            'target_memory_mb': target_memory_mb,
            'actual_memory_percent': memory.percent,
            'method': 'stress_process'
        }

    async def _inject_disk_stress(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Inject disk I/O stress"""
        # Implementation would use tools like fio or dd
        return {'method': 'disk_stress_not_implemented'}

    async def _inject_network_partition(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Inject network partition"""
        # Implementation would use iptables or network tools
        return {'method': 'network_partition_not_implemented'}

    async def _kill_process(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Kill a process"""
        process_name = experiment.parameters.get('process_name')
        if not process_name:
            raise ValueError("process_name parameter required")

        # Find and kill process
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                proc.kill()
                return {
                    'process_killed': process_name,
                    'pid': proc.info['pid']
                }

        return {'error': f'Process {process_name} not found'}

    async def _inject_dependency_failure(self, experiment: ChaosExperiment) -> Dict[str, Any]:
        """Inject dependency failure"""
        dependency = experiment.parameters.get('dependency')
        # Implementation would modify dependency behavior
        return {'method': 'dependency_failure_not_implemented'}

    async def _run_safety_checks(self, experiment: ChaosExperiment) -> bool:
        """Run safety checks before experiment"""
        for check in experiment.safety_checks:
            check_type = check.get('type')
            if check_type == 'cpu_limit':
                current_cpu = psutil.cpu_percent()
                if current_cpu > check.get('threshold', 90):
                    return False
            elif check_type == 'memory_limit':
                memory = psutil.virtual_memory()
                if memory.percent > check.get('threshold', 90):
                    return False
            elif check_type == 'service_count':
                # Check minimum number of services running
                running_services = len([p for p in psutil.process_iter() if p.is_running()])
                if running_services < check.get('min_count', 5):
                    return False

        return True

    async def _execute_rollback(self, experiment: ChaosExperiment) -> None:
        """Execute rollback plan"""
        rollback_type = experiment.rollback_plan.get('type')
        if rollback_type == 'restart_service':
            service_name = experiment.rollback_plan.get('service')
            # Implementation would restart service
            pass
        elif rollback_type == 'restore_config':
            # Restore configuration
            pass

    def _default_safety_checks(self) -> List[Dict[str, Any]]:
        """Default safety checks"""
        return [
            {'type': 'cpu_limit', 'threshold': 90},
            {'type': 'memory_limit', 'threshold': 90},
            {'type': 'service_count', 'min_count': 3}
        ]

    def get_experiment(self, experiment_id: str) -> Optional[ChaosExperiment]:
        """Get experiment by ID"""
        return self.experiments.get(experiment_id)

    def list_experiments(self, status_filter: Optional[ChaosExperimentStatus] = None) -> List[ChaosExperiment]:
        """List experiments with optional status filter"""
        experiments = list(self.experiments.values())
        if status_filter:
            experiments = [e for e in experiments if e.status == status_filter]
        return experiments

class ForensicsEngine:
    """Digital forensics engine for incident investigation"""

    def __init__(self, config: Config):
        self.config = config
        self.snapshots: Dict[str, ForensicsSnapshot] = {}
        self.evidence_store: Dict[str, bytes] = {}
        self.chain_of_custody: List[Dict[str, Any]] = []

    def create_snapshot(self,
                       event_type: ForensicsEventType,
                       description: str,
                       include_memory: bool = False,
                       include_logs: bool = True) -> ForensicsSnapshot:
        """Create a forensic snapshot"""
        snapshot_id = f"forensic_{secrets.token_hex(8)}"

        # Capture system state
        system_state = self._capture_system_state()
        process_list = self._capture_process_list()
        network_connections = self._capture_network_connections()
        file_system_state = self._capture_file_system_state()
        logs = self._capture_logs() if include_logs else []
        memory_dump = self._capture_memory_dump() if include_memory else None

        snapshot = ForensicsSnapshot(
            id=snapshot_id,
            timestamp=datetime.utcnow(),
            event_type=event_type,
            description=description,
            system_state=system_state,
            process_list=process_list,
            network_connections=network_connections,
            file_system_state=file_system_state,
            memory_dump=memory_dump,
            logs=logs,
            evidence_chain=[]
        )

        self.snapshots[snapshot_id] = snapshot

        # Add to chain of custody
        self._add_to_chain_of_custody(snapshot_id, 'created', f'Snapshot created for {event_type.value}')

        return snapshot

    def analyze_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """Analyze a forensic snapshot"""
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            raise ValueError(f"Snapshot {snapshot_id} not found")

        analysis = {
            'snapshot_id': snapshot_id,
            'timestamp': snapshot.timestamp,
            'event_type': snapshot.event_type.value,
            'findings': [],
            'recommendations': []
        }

        # Analyze system state
        if snapshot.system_state.get('cpu_percent', 0) > 90:
            analysis['findings'].append({
                'type': 'high_cpu',
                'severity': 'medium',
                'description': 'High CPU usage detected'
            })

        # Analyze processes
        suspicious_processes = []
        for proc in snapshot.process_list:
            if self._is_suspicious_process(proc):
                suspicious_processes.append(proc)

        if suspicious_processes:
            analysis['findings'].append({
                'type': 'suspicious_processes',
                'severity': 'high',
                'description': f'Found {len(suspicious_processes)} suspicious processes',
                'details': suspicious_processes
            })

        # Analyze network connections
        suspicious_connections = []
        for conn in snapshot.network_connections:
            if self._is_suspicious_connection(conn):
                suspicious_connections.append(conn)

        if suspicious_connections:
            analysis['findings'].append({
                'type': 'suspicious_connections',
                'severity': 'high',
                'description': f'Found {len(suspicious_connections)} suspicious network connections',
                'details': suspicious_connections
            })

        # Generate recommendations
        if analysis['findings']:
            analysis['recommendations'].append('Isolate affected systems')
            analysis['recommendations'].append('Review access logs')
            analysis['recommendations'].append('Update security policies')

        return analysis

    def export_snapshot(self, snapshot_id: str, format: str = 'json') -> str:
        """Export snapshot in specified format"""
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            raise ValueError(f"Snapshot {snapshot_id} not found")

        if format == 'json':
            data = asdict(snapshot)
            # Convert bytes to base64 for JSON serialization
            if snapshot.memory_dump:
                data['memory_dump'] = snapshot.memory_dump.hex()
            return json.dumps(data, default=str, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def verify_integrity(self, snapshot_id: str) -> bool:
        """Verify snapshot integrity"""
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            return False

        # Calculate hash of snapshot data
        snapshot_data = json.dumps(asdict(snapshot), default=str, sort_keys=True)
        calculated_hash = hashlib.sha256(snapshot_data.encode()).hexdigest()

        # Check against stored hash (would be stored separately in production)
        stored_hash = self._get_stored_hash(snapshot_id)
        return calculated_hash == stored_hash

    def _capture_system_state(self) -> Dict[str, Any]:
        """Capture current system state"""
        cpu = psutil.cpu_times_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()

        return {
            'cpu_percent': psutil.cpu_percent(),
            'cpu_times': dict(cpu._asdict()),
            'memory_total': memory.total,
            'memory_available': memory.available,
            'memory_percent': memory.percent,
            'disk_total': disk.total,
            'disk_free': disk.free,
            'disk_percent': disk.percent,
            'network_bytes_sent': network.bytes_sent,
            'network_bytes_recv': network.bytes_recv,
            'boot_time': psutil.boot_time(),
            'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
        }

    def _capture_process_list(self) -> List[Dict[str, Any]]:
        """Capture list of running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append(dict(proc.info))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes

    def _capture_network_connections(self) -> List[Dict[str, Any]]:
        """Capture network connections"""
        connections = []
        for conn in psutil.net_connections():
            connections.append({
                'fd': conn.fd,
                'family': conn.family,
                'type': conn.type,
                'laddr': conn.laddr,
                'raddr': conn.raddr,
                'status': conn.status,
                'pid': conn.pid
            })
        return connections

    def _capture_file_system_state(self) -> Dict[str, Any]:
        """Capture file system state"""
        # Capture important file metadata
        important_files = [
            '/etc/passwd',
            '/etc/shadow',
            '/var/log/auth.log',
            '/var/log/syslog'
        ]

        file_states = {}
        for file_path in important_files:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                file_states[file_path] = {
                    'size': stat.st_size,
                    'mtime': stat.st_mtime,
                    'ctime': stat.st_ctime,
                    'mode': oct(stat.st_mode)
                }

        return file_states

    def _capture_logs(self) -> List[Dict[str, Any]]:
        """Capture recent log entries"""
        # This would capture from various log sources
        # For demo, return empty list
        return []

    def _capture_memory_dump(self) -> Optional[bytes]:
        """Capture memory dump (dangerous, use with caution)"""
        # This is extremely dangerous and should never be done in production
        # without proper safeguards and legal authorization
        return None

    def _is_suspicious_process(self, process: Dict[str, Any]) -> bool:
        """Check if a process looks suspicious"""
        suspicious_names = ['nc', 'ncat', 'netcat', 'wget', 'curl', 'python', 'perl', 'ruby']
        name = process.get('name', '').lower()

        return any(suspicious in name for suspicious in suspicious_names)

    def _is_suspicious_connection(self, connection: Dict[str, Any]) -> bool:
        """Check if a network connection looks suspicious"""
        # Check for connections to known malicious IPs or unusual ports
        raddr = connection.get('raddr')
        if raddr:
            port = raddr.get('port')
            # Flag unusual ports or known bad IPs
            suspicious_ports = [22, 23, 53, 80, 443, 3389]  # Common attack targets
            if port and port not in suspicious_ports and port < 1024:
                return True

        return False

    def _add_to_chain_of_custody(self, snapshot_id: str, action: str, description: str):
        """Add entry to chain of custody"""
        entry = {
            'timestamp': datetime.utcnow(),
            'snapshot_id': snapshot_id,
            'action': action,
            'description': description,
            'user': 'system',  # In production, get from current user
            'hash': self._calculate_snapshot_hash(snapshot_id)
        }

        self.chain_of_custody.append(entry)

    def _calculate_snapshot_hash(self, snapshot_id: str) -> str:
        """Calculate hash of snapshot for integrity checking"""
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            return ''

        data = json.dumps(asdict(snapshot), default=str, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def _get_stored_hash(self, snapshot_id: str) -> str:
        """Get stored hash for integrity verification"""
        # In production, this would be stored separately
        return self._calculate_snapshot_hash(snapshot_id)

    def get_snapshot(self, snapshot_id: str) -> Optional[ForensicsSnapshot]:
        """Get snapshot by ID"""
        return self.snapshots.get(snapshot_id)

    def list_snapshots(self, event_type_filter: Optional[ForensicsEventType] = None) -> List[ForensicsSnapshot]:
        """List snapshots with optional event type filter"""
        snapshots = list(self.snapshots.values())
        if event_type_filter:
            snapshots = [s for s in snapshots if s.event_type == event_type_filter]
        return snapshots

class ReliabilityEngine:
    """Reliability engineering and monitoring engine"""

    def __init__(self, config: Config):
        self.config = config
        self.metrics: List[ReliabilityMetric] = []
        self.sla_targets = {
            'availability': 99.9,  # 99.9% uptime
            'latency_p95': 500,    # 500ms p95 latency
            'error_rate': 0.1      # 0.1% error rate
        }
        self.error_budget = {
            'total_budget': 43200,  # 12 hours per month (for 99.9% SLA)
            'used_budget': 0,
            'remaining_budget': 43200
        }

    def record_metric(self, name: str, value: float, service: str, threshold: Optional[float] = None):
        """Record a reliability metric"""
        status = 'healthy'
        if threshold and value > threshold:
            status = 'warning' if value < threshold * 1.5 else 'critical'

        metric = ReliabilityMetric(
            name=name,
            value=value,
            timestamp=datetime.utcnow(),
            service=service,
            threshold=threshold or 0,
            status=status
        )

        self.metrics.append(metric)

        # Keep only last 1000 metrics
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]

    def calculate_sla_compliance(self, service: str, time_window: timedelta = timedelta(days=30)) -> Dict[str, Any]:
        """Calculate SLA compliance for a service"""
        cutoff_time = datetime.utcnow() - time_window

        service_metrics = [m for m in self.metrics
                          if m.service == service and m.timestamp > cutoff_time]

        if not service_metrics:
            return {'compliance': 0, 'message': 'No metrics available'}

        # Calculate availability
        total_checks = len(service_metrics)
        successful_checks = len([m for m in service_metrics if m.status == 'healthy'])
        availability = (successful_checks / total_checks) * 100

        # Calculate error budget usage
        failed_checks = total_checks - successful_checks
        error_budget_used = (failed_checks / total_checks) * 100

        compliance = {
            'service': service,
            'time_window_days': time_window.days,
            'availability_percent': availability,
            'error_budget_used_percent': error_budget_used,
            'sla_target_percent': self.sla_targets['availability'],
            'compliant': availability >= self.sla_targets['availability'],
            'total_checks': total_checks,
            'successful_checks': successful_checks,
            'failed_checks': failed_checks
        }

        return compliance

    def get_error_budget_status(self) -> Dict[str, Any]:
        """Get current error budget status"""
        return {
            'total_budget_seconds': self.error_budget['total_budget'],
            'used_budget_seconds': self.error_budget['used_budget'],
            'remaining_budget_seconds': self.error_budget['remaining_budget'],
            'used_percent': (self.error_budget['used_budget'] / self.error_budget['total_budget']) * 100,
            'status': 'healthy' if self.error_budget['remaining_budget'] > 0 else 'exhausted'
        }

    def predict_failures(self, service: str) -> List[Dict[str, Any]]:
        """Predict potential failures based on metrics trends"""
        # Simple trend analysis
        recent_metrics = [m for m in self.metrics
                         if m.service == service][-50:]  # Last 50 metrics

        if len(recent_metrics) < 10:
            return []

        predictions = []

        # Check for increasing error rates
        error_metrics = [m for m in recent_metrics if 'error' in m.name.lower()]
        if len(error_metrics) >= 5:
            recent_errors = [m.value for m in error_metrics[-5:]]
            avg_recent = sum(recent_errors) / len(recent_errors)
            avg_older = sum([m.value for m in error_metrics[:-5]]) / len(error_metrics[:-5])

            if avg_recent > avg_older * 1.5:
                predictions.append({
                    'type': 'increasing_error_rate',
                    'severity': 'high',
                    'description': 'Error rate is increasing significantly',
                    'confidence': 0.8
                })

        # Check for performance degradation
        latency_metrics = [m for m in recent_metrics if 'latency' in m.name.lower()]
        if len(latency_metrics) >= 5:
            recent_latency = sum([m.value for m in latency_metrics[-5:]]) / len(latency_metrics[-5:])
            older_latency = sum([m.value for m in latency_metrics[:-5]]) / len(latency_metrics[:-5])

            if recent_latency > older_latency * 1.2:
                predictions.append({
                    'type': 'performance_degradation',
                    'severity': 'medium',
                    'description': 'Latency is increasing',
                    'confidence': 0.7
                })

        return predictions

    def generate_reliability_report(self, service: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive reliability report"""
        services = set(m.service for m in self.metrics)
        if service:
            services = {service}

        report = {
            'generated_at': datetime.utcnow(),
            'services': {},
            'overall_health': 'healthy',
            'recommendations': []
        }

        worst_health = 'healthy'

        for svc in services:
            compliance = self.calculate_sla_compliance(svc)
            predictions = self.predict_failures(svc)

            health_score = self._calculate_health_score(svc)
            health_status = self._get_health_status(health_score)

            report['services'][svc] = {
                'compliance': compliance,
                'predictions': predictions,
                'health_score': health_score,
                'health_status': health_status,
                'active_alerts': len([p for p in predictions if p['severity'] in ['high', 'critical']])
            }

            if self._compare_health_status(health_status, worst_health) > 0:
                worst_health = health_status

        report['overall_health'] = worst_health

        # Generate recommendations
        if worst_health in ['warning', 'critical']:
            report['recommendations'].append('Review recent changes and roll back if necessary')
            report['recommendations'].append('Increase monitoring frequency')
            report['recommendations'].append('Consider scaling resources')

        if any(svc_data['active_alerts'] > 0 for svc_data in report['services'].values()):
            report['recommendations'].append('Address predicted failures proactively')

        return report

    def _calculate_health_score(self, service: str) -> float:
        """Calculate health score for a service (0-100)"""
        recent_metrics = [m for m in self.metrics if m.service == service][-20:]

        if not recent_metrics:
            return 50.0  # Neutral score

        healthy_count = len([m for m in recent_metrics if m.status == 'healthy'])
        warning_count = len([m for m in recent_metrics if m.status == 'warning'])
        critical_count = len([m for m in recent_metrics if m.status == 'critical'])

        total = len(recent_metrics)
        score = (healthy_count * 100 + warning_count * 50 + critical_count * 0) / total

        return min(100.0, max(0.0, score))

    def _get_health_status(self, score: float) -> str:
        """Get health status from score"""
        if score >= 90:
            return 'healthy'
        elif score >= 70:
            return 'warning'
        else:
            return 'critical'

    def _compare_health_status(self, status1: str, status2: str) -> int:
        """Compare health statuses (higher number = worse health)"""
        order = {'healthy': 0, 'warning': 1, 'critical': 2}
        return order.get(status1, 0) - order.get(status2, 0)

class ComplianceEngine:
    """Compliance monitoring and enforcement engine"""

    def __init__(self, config: Config):
        self.config = config
        self.checks: Dict[str, ComplianceCheck] = {}
        self.frameworks_enabled = {
            ComplianceFramework.GDPR: True,
            ComplianceFramework.HIPAA: False,
            ComplianceFramework.SOX: False,
            ComplianceFramework.PCI_DSS: False
        }

    def run_compliance_check(self, framework: ComplianceFramework, control: str) -> ComplianceCheck:
        """Run a specific compliance check"""
        check_id = f"{framework.value}_{control}_{secrets.token_hex(4)}"

        # Simulate compliance check
        status = random.choice(['compliant', 'non_compliant', 'not_applicable'])
        severity = random.choice(['low', 'medium', 'high', 'critical']) if status == 'non_compliant' else 'info'

        check = ComplianceCheck(
            id=check_id,
            framework=framework,
            control=control,
            description=f"Check for {framework.value} control {control}",
            status=status,
            severity=severity,
            evidence=[{'type': 'test', 'result': 'passed'}],
            remediation='Implement required controls' if status == 'non_compliant' else '',
            checked_at=datetime.utcnow(),
            next_check=datetime.utcnow() + timedelta(days=30)
        )

        self.checks[check_id] = check
        return check

    def run_all_checks(self, framework: Optional[ComplianceFramework] = None) -> List[ComplianceCheck]:
        """Run all compliance checks for enabled frameworks"""
        results = []

        frameworks_to_check = [framework] if framework else \
                             [f for f, enabled in self.frameworks_enabled.items() if enabled]

        controls = {
            ComplianceFramework.GDPR: ['data_processing', 'consent', 'data_portability', 'right_to_erasure'],
            ComplianceFramework.HIPAA: ['privacy_rule', 'security_rule', 'breach_notification'],
            ComplianceFramework.SOX: ['internal_controls', 'financial_reporting', 'audit_trail'],
            ComplianceFramework.PCI_DSS: ['data_security', 'access_control', 'monitoring']
        }

        for fw in frameworks_to_check:
            for control in controls.get(fw, []):
                check = self.run_compliance_check(fw, control)
                results.append(check)

        return results

    def generate_compliance_report(self, framework: Optional[ComplianceFramework] = None) -> Dict[str, Any]:
        """Generate compliance report"""
        checks = [c for c in self.checks.values()
                 if framework is None or c.framework == framework]

        total_checks = len(checks)
        compliant_checks = len([c for c in checks if c.status == 'compliant'])
        non_compliant_checks = len([c for c in checks if c.status == 'non_compliant'])

        compliance_score = (compliant_checks / total_checks * 100) if total_checks > 0 else 0

        report = {
            'generated_at': datetime.utcnow(),
            'framework': framework.value if framework else 'all',
            'total_checks': total_checks,
            'compliant_checks': compliant_checks,
            'non_compliant_checks': non_compliant_checks,
            'compliance_score': compliance_score,
            'critical_findings': [c for c in checks if c.severity == 'critical'],
            'recommendations': []
        }

        # Generate recommendations
        if non_compliant_checks > 0:
            report['recommendations'].append('Address non-compliant controls immediately')
            report['recommendations'].append('Implement automated compliance monitoring')
            report['recommendations'].append('Conduct regular compliance training')

        if compliance_score < 80:
            report['recommendations'].append('Perform comprehensive compliance audit')
            report['recommendations'].append('Engage compliance consultants if needed')

        return report

    def enable_framework(self, framework: ComplianceFramework):
        """Enable a compliance framework"""
        self.frameworks_enabled[framework] = True

    def disable_framework(self, framework: ComplianceFramework):
        """Disable a compliance framework"""
        self.frameworks_enabled[framework] = False

    def get_check(self, check_id: str) -> Optional[ComplianceCheck]:
        """Get compliance check by ID"""
        return self.checks.get(check_id)

    def list_checks(self, framework: Optional[ComplianceFramework] = None,
                   status: Optional[str] = None) -> List[ComplianceCheck]:
        """List compliance checks with filters"""
        checks = list(self.checks.values())

        if framework:
            checks = [c for c in checks if c.framework == framework]

        if status:
            checks = [c for c in checks if c.status == status]

        return checks