"""
Load Testing Module

Load testing capabilities for the system.
"""

import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
import time

class LoadTestingModule:
    """Load testing module for system performance evaluation."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)

    async def run_load_test(self, url: str, concurrent_users: int = 10, duration: int = 60) -> Dict[str, Any]:
        """Run load test against a URL."""
        if not self.enabled:
            return {"status": "disabled"}

        results = {
            "url": url,
            "concurrent_users": concurrent_users,
            "duration": duration,
            "requests_sent": 0,
            "responses_received": 0,
            "errors": 0,
            "response_times": []
        }

        async def make_request(session: aiohttp.ClientSession):
            start_time = time.time()
            try:
                async with session.get(url) as response:
                    end_time = time.time()
                    results["responses_received"] += 1
                    results["response_times"].append(end_time - start_time)
                    return response.status
            except Exception:
                results["errors"] += 1
                return None

        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = []

            while time.time() - start_time < duration:
                if len(tasks) < concurrent_users:
                    task = asyncio.create_task(make_request(session))
                    tasks.append(task)
                    results["requests_sent"] += 1

                # Clean up completed tasks
                tasks = [t for t in tasks if not t.done()]

                await asyncio.sleep(0.01)

            # Wait for remaining tasks
            await asyncio.gather(*tasks, return_exceptions=True)

        # Calculate statistics
        if results["response_times"]:
            results["avg_response_time"] = sum(results["response_times"]) / len(results["response_times"])
            results["min_response_time"] = min(results["response_times"])
            results["max_response_time"] = max(results["response_times"])

        results["requests_per_second"] = results["requests_sent"] / duration

        return results