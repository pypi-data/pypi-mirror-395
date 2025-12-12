"""Task scheduler for periodic execution."""

import time
import threading
from typing import Callable, Optional
from datetime import datetime, timedelta


class Scheduler:
    """Simple cron-like scheduler for FlowMind tasks.
    
    Supports interval-based scheduling (e.g., every 5 minutes).
    
    Attributes:
        interval: Time between executions
        callback: Function to call
        running: Whether scheduler is active
    """
    
    def __init__(self):
        self.jobs = []
        self._running = False
        self._thread: Optional[threading.Thread] = None
    
    def every(self, interval: str, callback: Callable):
        """Schedule a job to run at intervals.
        
        Args:
            interval: Interval string (e.g., "5m", "1h", "30s")
            callback: Function to call
            
        Returns:
            Job instance
        """
        seconds = self._parse_interval(interval)
        job = ScheduledJob(seconds, callback)
        self.jobs.append(job)
        return job
    
    def _parse_interval(self, interval: str) -> int:
        """Parse interval string to seconds.
        
        Args:
            interval: Interval string (e.g., "5m", "1h", "30s")
            
        Returns:
            Interval in seconds
        """
        if interval.endswith('s'):
            return int(interval[:-1])
        elif interval.endswith('m'):
            return int(interval[:-1]) * 60
        elif interval.endswith('h'):
            return int(interval[:-1]) * 3600
        elif interval.endswith('d'):
            return int(interval[:-1]) * 86400
        else:
            raise ValueError(f"Invalid interval format: {interval}")
    
    def start(self):
        """Start the scheduler."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._thread:
            self._thread.join()
    
    def _run(self):
        """Main scheduler loop."""
        while self._running:
            now = time.time()
            
            for job in self.jobs:
                if job.should_run(now):
                    try:
                        job.run()
                    except Exception as e:
                        print(f"Job failed: {e}")
            
            time.sleep(1)  # Check every second
    
    def __repr__(self) -> str:
        return f"Scheduler(jobs={len(self.jobs)}, running={self._running})"


class ScheduledJob:
    """A scheduled job.
    
    Attributes:
        interval: Seconds between executions
        callback: Function to call
        last_run: Last execution time
    """
    
    def __init__(self, interval: int, callback: Callable):
        self.interval = interval
        self.callback = callback
        self.last_run: Optional[float] = None
        self.enabled = True
    
    def should_run(self, now: float) -> bool:
        """Check if job should run now.
        
        Args:
            now: Current timestamp
            
        Returns:
            True if job should execute
        """
        if not self.enabled:
            return False
        
        if self.last_run is None:
            return True
        
        return (now - self.last_run) >= self.interval
    
    def run(self):
        """Execute the job."""
        self.last_run = time.time()
        self.callback()
    
    def disable(self):
        """Disable the job."""
        self.enabled = False
    
    def enable(self):
        """Enable the job."""
        self.enabled = True
