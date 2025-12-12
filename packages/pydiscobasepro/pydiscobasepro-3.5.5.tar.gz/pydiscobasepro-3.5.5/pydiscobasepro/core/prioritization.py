"""
Task Prioritization System

Advanced task scheduling with priority queues and resource allocation.
"""

import asyncio
import heapq
from typing import Dict, Any, List, Optional, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
import time

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class TaskPriority(Enum):
    """Task priority levels with resource allocation."""
    BACKGROUND = 1    # Low priority, minimal resources
    LOW = 2          # Standard low priority
    NORMAL = 3       # Default priority
    HIGH = 4         # High priority
    CRITICAL = 5     # Critical priority, maximum resources
    SYSTEM = 6       # System-level priority, highest

@dataclass(order=True)
class PrioritizedTask:
    """A task with priority and resource requirements."""
    priority: TaskPriority
    created_at: float
    task_id: str
    coroutine: Callable[..., Awaitable[Any]]
    args: tuple = field(compare=False)
    kwargs: dict = field(compare=False)
    resource_requirements: Dict[str, Any] = field(default_factory=dict, compare=False)
    timeout: Optional[float] = field(default=None, compare=False)
    retry_count: int = field(default=0, compare=False)
    max_retries: int = field(default=3, compare=False)
    dependencies: List[str] = field(default_factory=list, compare=False)
    callback: Optional[Callable] = field(default=None, compare=False)

class TaskPrioritization:
    """Advanced task prioritization and scheduling system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_concurrent_tasks = config.get("max_concurrent_tasks", 10)
        self.resource_limits = config.get("resource_limits", {})

        # Priority queues for different priority levels
        self.task_queues: Dict[TaskPriority, List[PrioritizedTask]] = {
            priority: [] for priority in TaskPriority
        }

        # Active tasks and resource tracking
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.current_resources: Dict[str, float] = {}
        self.task_results: Dict[str, Any] = {}
        self.task_errors: Dict[str, Exception] = {}
        self.dependency_graph: Dict[str, List[str]] = {}  # task_id -> dependent tasks

        self.running = False
        self.worker_tasks: List[asyncio.Task] = []
        self.resource_lock = asyncio.Lock()

        # Statistics
        self.stats = {
            "tasks_processed": 0,
            "tasks_failed": 0,
            "avg_execution_time": 0.0,
            "resource_utilization": {}
        }

    async def start(self):
        """Start the task prioritization system."""
        if self.running:
            return

        self.running = True

        # Start worker tasks for each priority level
        for priority in TaskPriority:
            worker = asyncio.create_task(self._priority_worker(priority))
            self.worker_tasks.append(worker)

        logger.info("Task prioritization system started")

    async def stop(self):
        """Stop the task prioritization system."""
        self.running = False

        # Cancel all workers
        for worker in self.worker_tasks:
            worker.cancel()

        await asyncio.gather(*self.worker_tasks, return_exceptions=True)

        # Cancel active tasks
        for task in self.active_tasks.values():
            task.cancel()

        logger.info("Task prioritization system stopped")

    async def submit_task(
        self,
        task_id: str,
        coroutine: Callable[..., Awaitable[Any]],
        *args,
        priority: TaskPriority = TaskPriority.NORMAL,
        resource_requirements: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        dependencies: Optional[List[str]] = None,
        callback: Optional[Callable] = None,
        **kwargs
    ) -> str:
        """Submit a task with priority and resource requirements."""
        task = PrioritizedTask(
            priority=priority,
            created_at=time.time(),
            task_id=task_id,
            coroutine=coroutine,
            args=args,
            kwargs=kwargs,
            resource_requirements=resource_requirements or {},
            timeout=timeout,
            max_retries=max_retries,
            dependencies=dependencies or [],
            callback=callback
        )

        # Add to dependency graph
        for dep in task.dependencies:
            if dep not in self.dependency_graph:
                self.dependency_graph[dep] = []
            self.dependency_graph[dep].append(task_id)

        # Add to appropriate priority queue
        heapq.heappush(self.task_queues[priority], task)

        logger.debug(f"Task {task_id} submitted with priority {priority.name}")
        return task_id

    async def _priority_worker(self, priority: TaskPriority):
        """Worker for a specific priority level."""
        while self.running:
            try:
                # Get next task for this priority
                task = await self._get_next_task(priority)
                if not task:
                    await asyncio.sleep(0.1)
                    continue

                # Check resource availability
                if not await self._check_resource_availability(task):
                    # Put task back and wait
                    heapq.heappush(self.task_queues[priority], task)
                    await asyncio.sleep(0.5)
                    continue

                # Check dependencies
                if not await self._check_dependencies_satisfied(task):
                    # Dependencies not satisfied, put back
                    heapq.heappush(self.task_queues[priority], task)
                    await asyncio.sleep(1)
                    continue

                # Execute task
                await self._execute_task(task)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Priority worker {priority.name} error: {e}")
                await asyncio.sleep(1)

    async def _get_next_task(self, priority: TaskPriority) -> Optional[PrioritizedTask]:
        """Get the next task for a priority level."""
        queue = self.task_queues[priority]
        if queue:
            return heapq.heappop(queue)
        return None

    async def _check_resource_availability(self, task: PrioritizedTask) -> bool:
        """Check if required resources are available."""
        async with self.resource_lock:
            for resource, required in task.resource_requirements.items():
                limit = self.resource_limits.get(resource, float('inf'))
                current = self.current_resources.get(resource, 0)

                if current + required > limit:
                    return False

            # Reserve resources
            for resource, required in task.resource_requirements.items():
                self.current_resources[resource] = self.current_resources.get(resource, 0) + required

        return True

    async def _check_dependencies_satisfied(self, task: PrioritizedTask) -> bool:
        """Check if all task dependencies are satisfied."""
        for dep in task.dependencies:
            if dep not in self.task_results and dep not in self.task_errors:
                return False
        return True

    async def _execute_task(self, task: PrioritizedTask):
        """Execute a prioritized task."""
        start_time = time.time()

        try:
            # Execute with timeout if specified
            if task.timeout:
                result = await asyncio.wait_for(
                    task.coroutine(*task.args, **task.kwargs),
                    timeout=task.timeout
                )
            else:
                result = await task.coroutine(*task.args, **task.kwargs)

            # Store result
            self.task_results[task.task_id] = result

            # Execute callback
            if task.callback:
                try:
                    await task.callback(result)
                except Exception as e:
                    logger.error(f"Task callback error for {task.task_id}: {e}")

            # Notify dependent tasks
            await self._notify_dependents(task.task_id)

            execution_time = time.time() - start_time
            self._update_stats(success=True, execution_time=execution_time)

            logger.debug(f"Task {task.task_id} completed in {execution_time:.2f}s")

        except Exception as e:
            await self._handle_task_failure(task, e)

        finally:
            # Release resources
            async with self.resource_lock:
                for resource, required in task.resource_requirements.items():
                    self.current_resources[resource] = max(
                        0, self.current_resources.get(resource, 0) - required
                    )

    async def _handle_task_failure(self, task: PrioritizedTask, error: Exception):
        """Handle task execution failure."""
        logger.warning(f"Task {task.task_id} failed: {error}")

        if task.retry_count < task.max_retries:
            # Retry task
            task.retry_count += 1
            task.created_at = time.time()  # Reset priority

            heapq.heappush(self.task_queues[task.priority], task)
            logger.info(f"Task {task.task_id} scheduled for retry ({task.retry_count}/{task.max_retries})")
        else:
            # Task failed permanently
            self.task_errors[task.task_id] = error
            self._update_stats(success=False)

            # Notify dependents of failure
            await self._notify_dependents(task.task_id, failed=True)

            logger.error(f"Task {task.task_id} failed permanently after {task.max_retries} retries")

    async def _notify_dependents(self, task_id: str, failed: bool = False):
        """Notify dependent tasks."""
        if task_id in self.dependency_graph:
            dependents = self.dependency_graph[task_id]
            # In a real implementation, this would trigger dependent tasks
            # For now, just log
            logger.debug(f"Task {task_id} completion notified to {len(dependents)} dependents")

    def _update_stats(self, success: bool, execution_time: float = 0):
        """Update execution statistics."""
        if success:
            self.stats["tasks_processed"] += 1
        else:
            self.stats["tasks_failed"] += 1

        if execution_time > 0:
            current_avg = self.stats["avg_execution_time"]
            total_tasks = self.stats["tasks_processed"] + self.stats["tasks_failed"]
            self.stats["avg_execution_time"] = (
                (current_avg * (total_tasks - 1)) + execution_time
            ) / total_tasks

    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task."""
        if task_id in self.task_results:
            return {"status": "completed", "result": self.task_results[task_id]}
        elif task_id in self.task_errors:
            return {"status": "failed", "error": str(self.task_errors[task_id])}
        elif task_id in self.active_tasks:
            return {"status": "running"}
        else:
            # Check queues
            for priority, queue in self.task_queues.items():
                for task in queue:
                    if task.task_id == task_id:
                        return {
                            "status": "queued",
                            "priority": priority.name,
                            "position": queue.index(task)
                        }
            return None

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task."""
        # Cancel active task
        if task_id in self.active_tasks:
            self.active_tasks[task_id].cancel()
            del self.active_tasks[task_id]
            return True

        # Remove from queues
        for queue in self.task_queues.values():
            for i, task in enumerate(queue):
                if task.task_id == task_id:
                    queue.pop(i)
                    heapq.heapify(queue)
                    return True

        return False

    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        queue_stats = {}
        for priority, queue in self.task_queues.items():
            queue_stats[priority.name] = len(queue)

        return {
            "active_tasks": len(self.active_tasks),
            "queued_tasks": queue_stats,
            "completed_tasks": len(self.task_results),
            "failed_tasks": len(self.task_errors),
            "current_resources": self.current_resources.copy(),
            "resource_limits": self.resource_limits.copy(),
            **self.stats
        }

    def set_resource_limit(self, resource: str, limit: float):
        """Set resource limit."""
        self.resource_limits[resource] = limit
        logger.info(f"Resource limit set: {resource} = {limit}")

    def get_resource_usage(self, resource: str) -> float:
        """Get current resource usage."""
        return self.current_resources.get(resource, 0)