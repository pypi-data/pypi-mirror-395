"""
Background Worker Engine

Async job queue with prioritization and background task management.
"""

import asyncio
import heapq
from typing import Dict, Any, List, Optional, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
import time
import threading

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class JobPriority(Enum):
    """Job priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

@dataclass(order=True)
class Job:
    """Represents a background job."""
    priority: JobPriority
    created_at: float
    job_id: str
    task: Callable[..., Awaitable[Any]]
    args: tuple = field(compare=False)
    kwargs: dict = field(compare=False)
    max_retries: int = field(default=3, compare=False)
    retry_count: int = field(default=0, compare=False)
    timeout: Optional[float] = field(default=None, compare=False)
    callback: Optional[Callable] = field(default=None, compare=False)

class BackgroundWorkerEngine:
    """Background worker engine for async job processing."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_workers = config.get("max_workers", 5)
        self.job_queue: List[Job] = []
        self.active_jobs: Dict[str, asyncio.Task] = {}
        self.completed_jobs: Dict[str, Any] = {}
        self.failed_jobs: Dict[str, Exception] = {}

        self.queue_lock = asyncio.Lock()
        self.running = False
        self.workers: List[asyncio.Task] = []

        # Job statistics
        self.stats = {
            "jobs_processed": 0,
            "jobs_failed": 0,
            "jobs_retried": 0,
            "avg_processing_time": 0.0
        }

    async def start(self):
        """Start the background worker engine."""
        if self.running:
            return

        self.running = True

        # Start worker tasks
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker_loop(i))
            self.workers.append(worker)

        logger.info(f"Background worker engine started with {self.max_workers} workers")

    async def stop(self):
        """Stop the background worker engine."""
        self.running = False

        # Cancel all workers
        for worker in self.workers:
            worker.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)

        # Cancel active jobs
        for job_task in self.active_jobs.values():
            job_task.cancel()

        logger.info("Background worker engine stopped")

    async def submit_job(
        self,
        job_id: str,
        task: Callable[..., Awaitable[Any]],
        *args,
        priority: JobPriority = JobPriority.NORMAL,
        max_retries: int = 3,
        timeout: Optional[float] = None,
        callback: Optional[Callable] = None,
        **kwargs
    ) -> str:
        """Submit a job to the background queue."""
        job = Job(
            priority=priority,
            created_at=time.time(),
            job_id=job_id,
            task=task,
            args=args,
            kwargs=kwargs,
            max_retries=max_retries,
            timeout=timeout,
            callback=callback
        )

        async with self.queue_lock:
            heapq.heappush(self.job_queue, job)

        logger.debug(f"Job {job_id} submitted with priority {priority.name}")
        return job_id

    async def _worker_loop(self, worker_id: int):
        """Worker loop for processing jobs."""
        logger.debug(f"Worker {worker_id} started")

        while self.running:
            try:
                # Get next job from queue
                job = await self._get_next_job()
                if not job:
                    await asyncio.sleep(0.1)  # No jobs available
                    continue

                # Execute job
                await self._execute_job(job)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                await asyncio.sleep(1)

        logger.debug(f"Worker {worker_id} stopped")

    async def _get_next_job(self) -> Optional[Job]:
        """Get the next job from the priority queue."""
        async with self.queue_lock:
            if self.job_queue:
                return heapq.heappop(self.job_queue)
        return None

    async def _execute_job(self, job: Job):
        """Execute a background job."""
        start_time = time.time()

        try:
            # Create task for job execution
            if job.timeout:
                result = await asyncio.wait_for(
                    job.task(*job.args, **job.kwargs),
                    timeout=job.timeout
                )
            else:
                result = await job.task(*job.args, **job.kwargs)

            # Store result
            self.completed_jobs[job.job_id] = result

            # Execute callback if provided
            if job.callback:
                try:
                    await job.callback(result)
                except Exception as e:
                    logger.error(f"Job callback error for {job.job_id}: {e}")

            processing_time = time.time() - start_time
            self._update_stats(success=True, processing_time=processing_time)

            logger.debug(f"Job {job.job_id} completed in {processing_time:.2f}s")

        except Exception as e:
            await self._handle_job_failure(job, e)

    async def _handle_job_failure(self, job: Job, error: Exception):
        """Handle job execution failure."""
        logger.warning(f"Job {job.job_id} failed: {error}")

        if job.retry_count < job.max_retries:
            # Retry job
            job.retry_count += 1
            job.created_at = time.time()  # Reset priority

            async with self.queue_lock:
                heapq.heappush(self.job_queue, job)

            self.stats["jobs_retried"] += 1
            logger.info(f"Job {job.job_id} scheduled for retry ({job.retry_count}/{job.max_retries})")
        else:
            # Job failed permanently
            self.failed_jobs[job.job_id] = error
            self._update_stats(success=False)

            logger.error(f"Job {job.job_id} failed permanently after {job.max_retries} retries")

    def _update_stats(self, success: bool, processing_time: float = 0):
        """Update job processing statistics."""
        if success:
            self.stats["jobs_processed"] += 1
        else:
            self.stats["jobs_failed"] += 1

        if processing_time > 0:
            # Update rolling average
            current_avg = self.stats["avg_processing_time"]
            total_jobs = self.stats["jobs_processed"] + self.stats["jobs_failed"]
            self.stats["avg_processing_time"] = (
                (current_avg * (total_jobs - 1)) + processing_time
            ) / total_jobs

    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a job."""
        if job_id in self.completed_jobs:
            return {"status": "completed", "result": self.completed_jobs[job_id]}
        elif job_id in self.failed_jobs:
            return {"status": "failed", "error": str(self.failed_jobs[job_id])}
        elif job_id in self.active_jobs:
            return {"status": "running"}
        else:
            # Check if job is in queue
            async with self.queue_lock:
                for job in self.job_queue:
                    if job.job_id == job_id:
                        return {"status": "queued", "priority": job.priority.name}
            return None

    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a queued or running job."""
        # Cancel running job
        if job_id in self.active_jobs:
            self.active_jobs[job_id].cancel()
            del self.active_jobs[job_id]
            return True

        # Remove from queue
        async with self.queue_lock:
            for i, job in enumerate(self.job_queue):
                if job.job_id == job_id:
                    self.job_queue.pop(i)
                    heapq.heapify(self.job_queue)  # Restore heap property
                    return True

        return False

    async def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        async with self.queue_lock:
            queued_by_priority = {}
            for job in self.job_queue:
                priority = job.priority.name
                queued_by_priority[priority] = queued_by_priority.get(priority, 0) + 1

        return {
            "queued_jobs": len(self.job_queue),
            "active_jobs": len(self.active_jobs),
            "completed_jobs": len(self.completed_jobs),
            "failed_jobs": len(self.failed_jobs),
            "queued_by_priority": queued_by_priority,
            **self.stats
        }

    async def clear_completed_jobs(self):
        """Clear completed job results to free memory."""
        self.completed_jobs.clear()
        logger.info("Completed jobs cleared")

    async def retry_failed_jobs(self):
        """Retry all failed jobs."""
        failed_job_ids = list(self.failed_jobs.keys())

        for job_id in failed_job_ids:
            # This would need the original job definition
            # For now, just log
            logger.info(f"Would retry failed job: {job_id}")

        self.failed_jobs.clear()