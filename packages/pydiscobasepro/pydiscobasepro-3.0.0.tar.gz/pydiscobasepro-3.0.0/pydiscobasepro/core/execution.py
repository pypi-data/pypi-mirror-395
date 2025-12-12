"""
Core Execution Engine

Pluggable execution engine with priority pipelines, sandboxing, and resource management.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Callable, Awaitable
from concurrent.futures import ThreadPoolExecutor
import threading
from dataclasses import dataclass
from enum import Enum

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class ExecutionPriority(Enum):
    """Execution priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ExecutionTask:
    """Represents an executable task."""
    id: str
    function: Callable[..., Awaitable[Any]]
    args: tuple
    kwargs: dict
    priority: ExecutionPriority
    timeout: Optional[float]
    created_at: float
    retry_count: int = 0
    max_retries: int = 3

class ExecutionEngine:
    """Advanced execution engine with priority queues and resource management."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_workers = config.get("max_workers", 10)
        self.timeout = config.get("timeout", 30)
        self.retry_attempts = config.get("retry_attempts", 3)

        # Priority queues
        self.queues: Dict[ExecutionPriority, asyncio.Queue] = {
            priority: asyncio.Queue() for priority in ExecutionPriority
        }

        # Execution pools
        self.thread_executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.process_executor = None  # For CPU-intensive tasks

        # Active tasks tracking
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.task_results: Dict[str, Any] = {}
        self.task_errors: Dict[str, Exception] = {}

        # Resource limits
        self.max_concurrent_tasks = self.max_workers * 2
        self.current_tasks = 0
        self.resource_lock = asyncio.Lock()

        # Control flags
        self.running = False
        self.workers: List[asyncio.Task] = []

    async def initialize(self):
        """Initialize the execution engine."""
        self.running = True

        # Start worker tasks for each priority level
        for priority in ExecutionPriority:
            for _ in range(2):  # 2 workers per priority level
                worker = asyncio.create_task(self._worker_loop(priority))
                self.workers.append(worker)

        logger.info(f"Execution engine initialized with {len(self.workers)} workers")

    async def shutdown(self):
        """Shutdown the execution engine."""
        self.running = False

        # Cancel all workers
        for worker in self.workers:
            worker.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)

        # Cancel active tasks
        for task in self.active_tasks.values():
            task.cancel()

        # Shutdown executors
        self.thread_executor.shutdown(wait=True)
        if self.process_executor:
            self.process_executor.shutdown(wait=True)

        logger.info("Execution engine shutdown complete")

    async def submit_task(
        self,
        task_id: str,
        function: Callable[..., Awaitable[Any]],
        *args,
        priority: ExecutionPriority = ExecutionPriority.NORMAL,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """Submit a task for execution."""
        task = ExecutionTask(
            id=task_id,
            function=function,
            args=args,
            kwargs=kwargs,
            priority=priority,
            timeout=timeout or self.timeout,
            created_at=time.time(),
            max_retries=max_retries
        )

        await self.queues[priority].put(task)
        logger.debug(f"Task {task_id} submitted with priority {priority.name}")

        return task_id

    async def _worker_loop(self, priority: ExecutionPriority):
        """Worker loop for processing tasks of a specific priority."""
        while self.running:
            try:
                # Get task from queue
                task = await self.queues[priority].get()

                # Check resource limits
                async with self.resource_lock:
                    if self.current_tasks >= self.max_concurrent_tasks:
                        # Put task back and wait
                        await self.queues[priority].put(task)
                        await asyncio.sleep(0.1)
                        continue
                    self.current_tasks += 1

                # Execute task
                execution_task = asyncio.create_task(self._execute_task(task))
                self.active_tasks[task.id] = execution_task

                # Don't wait for completion, let it run in background

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error for priority {priority.name}: {e}")
                await asyncio.sleep(1)

    async def _execute_task(self, task: ExecutionTask):
        """Execute a single task with retry logic."""
        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                task.function(*task.args, **task.kwargs),
                timeout=task.timeout
            )

            self.task_results[task.id] = result
            logger.debug(f"Task {task.id} completed successfully")

        except asyncio.TimeoutError:
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                logger.warning(f"Task {task.id} timed out, retrying ({task.retry_count}/{task.max_retries})")
                await self.queues[task.priority].put(task)
            else:
                error = Exception(f"Task {task.id} timed out after {task.max_retries} retries")
                self.task_errors[task.id] = error
                logger.error(str(error))

        except Exception as e:
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                logger.warning(f"Task {task.id} failed, retrying ({task.retry_count}/{task.max_retries}): {e}")
                await self.queues[task.priority].put(task)
            else:
                self.task_errors[task.id] = e
                logger.error(f"Task {task.id} failed permanently: {e}")

        finally:
            # Cleanup
            async with self.resource_lock:
                self.current_tasks -= 1

            self.active_tasks.pop(task.id, None)

    async def get_task_result(self, task_id: str) -> Optional[Any]:
        """Get the result of a completed task."""
        return self.task_results.get(task_id)

    async def get_task_error(self, task_id: str) -> Optional[Exception]:
        """Get the error of a failed task."""
        return self.task_errors.get(task_id)

    async def is_task_complete(self, task_id: str) -> bool:
        """Check if a task is complete."""
        return task_id in self.task_results or task_id in self.task_errors

    async def cancel_task(self, task_id: str):
        """Cancel a running task."""
        if task_id in self.active_tasks:
            self.active_tasks[task_id].cancel()
            del self.active_tasks[task_id]
            logger.info(f"Task {task_id} cancelled")

    async def get_queue_stats(self) -> Dict[str, Any]:
        """Get statistics about task queues."""
        stats = {}
        for priority in ExecutionPriority:
            stats[priority.name.lower()] = {
                "queued": self.queues[priority].qsize(),
                "active": sum(1 for task in self.active_tasks.values()
                            if not task.done() and hasattr(task, '_task') and
                            task._task.priority == priority)
            }
        return stats

    async def get_engine_stats(self) -> Dict[str, Any]:
        """Get overall engine statistics."""
        return {
            "active_tasks": len(self.active_tasks),
            "current_concurrent": self.current_tasks,
            "max_concurrent": self.max_concurrent_tasks,
            "completed_tasks": len(self.task_results),
            "failed_tasks": len(self.task_errors),
            "queue_stats": await self.get_queue_stats(),
            "thread_pool_active": self.thread_executor._threads,
            "uptime": time.time() - getattr(self, '_start_time', time.time())
        }

    def run_in_thread(self, func: Callable, *args, **kwargs) -> asyncio.Future:
        """Run a function in the thread pool."""
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(self.thread_executor, func, *args, **kwargs)

    def run_in_process(self, func: Callable, *args, **kwargs) -> asyncio.Future:
        """Run a function in a separate process (for CPU-intensive tasks)."""
        if not self.process_executor:
            from concurrent.futures import ProcessPoolExecutor
            self.process_executor = ProcessPoolExecutor(max_workers=2)

        loop = asyncio.get_event_loop()
        return loop.run_in_executor(self.process_executor, func, *args, **kwargs)