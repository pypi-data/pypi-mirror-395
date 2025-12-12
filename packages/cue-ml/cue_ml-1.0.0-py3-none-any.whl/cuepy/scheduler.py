# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import time
import threading
import os
from typing import List

# Use relative imports for package internal consistency
from .gpu_pool import GPUPool, GPU
from .job_queue import JobQueue, Job
from .job_runner import execute_job

class Scheduler:
    """
    The heart of Cue. It runs a loop that matches pending jobs 
    from the queue with available GPUs from the pool.
    """
    
    def __init__(self, pool: GPUPool, queue: JobQueue, log_root: str = "logs"):
        self.pool = pool
        self.queue = queue
        self.log_root = log_root
        self._threads: List[threading.Thread] = []
        self._stop_event = threading.Event()

    def start(self, join: bool = True):
        """
        Starts the scheduling loop.
        
        Args:
            join: If True, blocks until all jobs are completed.
                  If False, runs in background (call join_all() later).
        """
        if join:
            self._run_loop()
        else:
            t = threading.Thread(target=self._run_loop, daemon=True)
            t.start()
            self._threads.append(t)

    def _run_loop(self):
        """Main scheduling loop."""
        try:
            while not self._stop_event.is_set():
                # 1. Exit condition: Queue empty AND no jobs currently running
                if self.queue.is_empty() and self.queue.running_count() == 0:
                    break

                # 2. Check for resources
                # We need at least one available GPU and one pending job to proceed
                if self.pool.available_count() > 0 and not self.queue.is_empty():
                    self._schedule_next()
                else:
                    # Prevent busy waiting if nothing can be done
                    time.sleep(0.1)
        
        except KeyboardInterrupt:
            self.stop()
        finally:
            # Ensure we wait for running jobs to finish even if queue is empty
            self._wait_for_workers()

    def _schedule_next(self):
        """Attempts to match the next job with a GPU."""
        
        # A. Fetch Job (Non-blocking)
        job = self.queue.get_next_job(block=False)
        if not job: 
            return

        # B. Check Resource Requirements
        # If the pool doesn't have enough TOTAL free GPUs right now,
        # put the job back and wait a bit.
        if self.pool.available_count() < job.gpu_req:
            self.queue.add_job(job)
            time.sleep(0.1)
            return

        # C. Allocate GPU(s)
        # We try to allocate ANY available GPUs.
        gpus = self.pool.allocate_gpus(job.id, count=job.gpu_req)

        if not gpus:
            # Edge case: GPU was taken by another thread between check and allocation.
            # Put job back in queue and wait a bit.
            self.queue.add_job(job)
            time.sleep(0.1)
            return

        # D. Mark Running in Queue
        # [FIX] We need to extract IDs from the GPU objects
        gpu_ids = [g.id for g in gpus]
        self.queue.mark_job_running(job.id, gpu_ids)

        # E. Spawn Worker Thread
        # We run the actual subprocess in a separate thread so the 
        # scheduler loop can continue processing other jobs.
        worker = threading.Thread(
            target=self._worker_wrapper,
            args=(job, gpus),
            daemon=True
        )
        worker.start()
        self._threads.append(worker)

    def _worker_wrapper(self, job: Job, gpus: List[GPU]):
        """
        The method running inside the thread. 
        Handles execution and ensures cleanup happens even if crash occurs.
        """
        try:
            # Determine Log Path
            # We prioritize path set in metadata, else fallback to generic
            log_path = job.metadata.get('log_path')
            if not log_path:
                safe_id = job.id.replace(" ", "_")
                log_path = os.path.join(self.log_root, f"{safe_id}.log")

            # Execute (Blocks this thread only)
            success, exit_code = execute_job(job, gpus, log_path)

            # Update Job Status
            if success:
                self.queue.mark_job_completed(job.id, exit_code)
            else:
                self.queue.mark_job_failed(
                    job.id, 
                    error_message=f"Process exited with code {exit_code}", 
                    exit_code=exit_code
                )

        except Exception as e:
            # Catastrophic failure in runner wrapper
            self.queue.mark_job_failed(job.id, error_message=str(e))
        
        finally:
            # CRITICAL: Always release GPUs back to pool, otherwise they leak
            for gpu in gpus:
                self.pool.deallocate_gpu(gpu.id)

    def _wait_for_workers(self):
        """Joins all worker threads."""
        for t in self._threads:
            if t.is_alive() and t is not threading.current_thread():
                t.join()

    def stop(self):
        """Signals the scheduler to stop processing new jobs."""
        self._stop_event.set()