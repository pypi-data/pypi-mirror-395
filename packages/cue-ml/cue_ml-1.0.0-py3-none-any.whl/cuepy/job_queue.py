# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import time
from enum import Enum
from dataclasses import dataclass
from queue import Queue as ThreadSafeQueue
from typing import Optional, List, Any, Dict

class JobState(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Job:
    """Represents a single unit of work (an experiment run)."""
    id: str
    script: str
    args: List[str]
    state: JobState = JobState.QUEUED
    gpu_req: int = 1
    gpu_ids: Optional[List[int]] = None 
    
    # Timing metrics
    submitted_at: float = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    # Outcomes
    exit_code: Optional[int] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.submitted_at is None: 
            self.submitted_at = time.time()
        if self.metadata is None: 
            self.metadata = {}
    
    def mark_running(self, gpu_ids: List[int]) -> None:
        self.state = JobState.RUNNING
        self.gpu_ids = gpu_ids
        self.started_at = time.time()
    
    def mark_completed(self, exit_code: int) -> None:
        self.state = JobState.COMPLETED if exit_code == 0 else JobState.FAILED
        self.exit_code = exit_code
        self.completed_at = time.time()
    
    def mark_failed(self, error_message: str, exit_code: Optional[int] = None) -> None:
        self.state = JobState.FAILED
        self.error_message = error_message
        self.exit_code = exit_code
        self.completed_at = time.time()
    
    def mark_cancelled(self) -> None:
        self.state = JobState.CANCELLED
        self.completed_at = time.time()
    
    def duration(self) -> Optional[float]:
        if self.started_at and self.completed_at: 
            return self.completed_at - self.started_at
        return None
    
    def wait_time(self) -> Optional[float]:
        if self.started_at: 
            return self.started_at - self.submitted_at
        return None
    
    def get_command(self, python_interpreter: str = "python") -> List[str]:
        """Constructs the subprocess command list."""
        return [python_interpreter, self.script] + self.args
    
    def __repr__(self) -> str:
        gpu_info = f", gpus={self.gpu_ids}" if self.gpu_ids is not None else ""
        return f"Job(id='{self.id}', script='{self.script}', state={self.state.value}{gpu_info})"

class JobQueue:
    """Manages the FIFO queue of jobs and tracks their lifecycle states."""
    
    def __init__(self):
        self._queue: ThreadSafeQueue = ThreadSafeQueue()
        self._jobs: Dict[str, Job] = {}     # Lookup all jobs by ID
        self._running: Dict[str, Job] = {}  # Currently active jobs
        self._completed: List[Job] = []     # History of finished jobs
    
    def add_job(self, job: Job) -> None:
        self._jobs[job.id] = job
        self._queue.put(job)
    
    def get_next_job(self, block: bool = False, timeout: Optional[float] = None) -> Optional[Job]:
        try:
            job = self._queue.get(block=block, timeout=timeout)
            return job
        except: 
            return None
    
    def mark_job_running(self, job_id: str, gpu_ids: List[int]) -> bool:
        job = self._jobs.get(job_id)
        if job:
            job.mark_running(gpu_ids)
            self._running[job_id] = job
            return True
        return False
    
    def mark_job_completed(self, job_id: str, exit_code: int) -> bool:
        job = self._jobs.get(job_id)
        if job:
            job.mark_completed(exit_code)
            if job_id in self._running:
                del self._running[job_id]
            self._completed.append(job)
            return True
        return False
    
    def mark_job_failed(self, job_id: str, error_message: str, exit_code: Optional[int] = None) -> bool:
        job = self._jobs.get(job_id)
        if job:
            job.mark_failed(error_message, exit_code)
            if job_id in self._running:
                del self._running[job_id]
            self._completed.append(job)
            return True
        return False
    
    def get_job(self, job_id: str) -> Optional[Job]: 
        return self._jobs.get(job_id)
    
    def get_running_jobs(self) -> List[Job]: 
        return list(self._running.values())
    
    def get_completed_jobs(self) -> List[Job]: 
        return self._completed
    
    def get_all_jobs(self) -> List[Job]: 
        return list(self._jobs.values())
    
    def is_empty(self) -> bool: 
        return self._queue.empty()
    
    def queued_count(self) -> int: 
        return self._queue.qsize()
    
    def running_count(self) -> int: 
        return len(self._running)
    
    def completed_count(self) -> int: 
        return len(self._completed)
    
    def total_jobs(self) -> int: 
        return len(self._jobs)
    
    def get_status_summary(self) -> Dict[str, int]:
        summary = {state.value: 0 for state in JobState}
        for job in self._jobs.values(): 
            summary[job.state.value] += 1
        return summary
    
    def __repr__(self) -> str:
        return (f"JobQueue(queued={self.queued_count()}, "
                f"running={self.running_count()}, "
                f"completed={self.completed_count()})")