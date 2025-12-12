# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import os
import sys
import time
from datetime import datetime
from typing import Dict, Set

from .config import resolve_script_path
from .job_queue import JobQueue, Job
from .gpu_pool import GPUPool
from .scheduler import Scheduler

def run_sequence(
    experiments: list, 
    config_path: str, 
    pool: GPUPool, 
    python_cmd: str, 
    log_root: str, 
    fail_fast: bool = False, 
    dry_run: bool = False,
    default_gpu_req: int = 1,
) -> Dict[str, int]:
    """
    Orchestrates the entire execution sequence.
    V1.0.0: Uses linear logging instead of TUI for stability.
    """
    
    # 1. Setup Environment
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(log_root, f"run_{timestamp}")
    
    if not dry_run:
        os.makedirs(run_dir, exist_ok=True)

    # 2. Build Job Queue
    queue = JobQueue()
    print(f"\n[Plan]")
    print(f"  • Config:  {config_path}")
    print(f"  • Output:  {run_dir}")
    print(f"  • Workers: {pool.total_gpus()} GPUs detected")

    job_count = 0
    for exp in experiments:
        exp_name = exp.get('name', 'unnamed')
        script_rel = exp['script']
        script_path = resolve_script_path(config_path, script_rel)
        
        # Validate Script Existence
        if not os.path.exists(script_path) and not dry_run:
            print(f"\033[91m[Error]\033[0m Script not found: {script_path}")
            return {'success': 0, 'failed': 1}

        for i, run in enumerate(exp['runs']):
            run_id = i + 1
            args = run['args']
            arg_list = args.split() if isinstance(args, str) else args
            
            # Generate ID and Log Path
            safe_exp = exp_name.replace(" ", "_").replace("/", "-")
            job_unique_id = f"{safe_exp}_{run_id}"
            log_path = os.path.join(run_dir, f"{job_unique_id}.log")

            req_gpus = run.get('gpus', default_gpu_req)

            job = Job(
                id=job_unique_id,
                script=script_path,
                args=arg_list,
                gpu_req=req_gpus,
                metadata={
                    'log_path': log_path, 
                    'exp_name': exp_name,
                    'run_id': run_id
                }
            )
            queue.add_job(job)
            job_count += 1

    print(f"  • Task:    Queued {job_count} jobs across {len(experiments)} experiments")

    # 3. Handle Dry Run
    if dry_run:
        print("\n[Dry Run] Jobs prepared but not submitted.")
        return {'success': job_count, 'failed': 0}

    # 4. User Confirmation
    try:
        sys.stdout.write("\nPress ENTER to start execution (or Ctrl+C to abort)...")
        sys.stdout.flush()
        input()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)

    # 5. Initialize & Start Scheduler
    scheduler = Scheduler(pool, queue, log_root=run_dir)
    scheduler.start(join=False)

    # 6. Monitor Loop (Linear Logging)
    print("-" * 60)
    print(f"Execution Started. Logs: {os.path.relpath(run_dir)}")
    print("-" * 60)

    # Sets to track which jobs we have already printed updates for
    printed_started: Set[str] = set()
    printed_finished: Set[str] = set()

    try:
        while True:
            # Check for newly started jobs
            for job in queue.get_running_jobs():
                if job.id not in printed_started:
                    ts = datetime.now().strftime('%H:%M:%S')
                    gpus_str = ",".join(map(str, job.gpu_ids)) if job.gpu_ids else "?"
                    print(f"[{ts}] Started:  {job.id:<25} (GPUs: {gpus_str})")
                    printed_started.add(job.id)

            # Check for newly completed jobs
            for job in queue.get_completed_jobs():
                if job.id not in printed_finished:
                    ts = datetime.now().strftime('%H:%M:%S')
                    
                    if job.exit_code == 0:
                        status_str = "\033[92mSuccess\033[0m"
                    else:
                        status_str = f"\033[91mFailed (Code {job.exit_code})\033[0m"
                    
                    duration = f"{job.duration():.1f}s" if job.duration() else "?"
                    print(f"[{ts}] Finished: {job.id:<25} -> {status_str} ({duration})")
                    printed_finished.add(job.id)

            # Exit condition
            if queue.is_empty() and queue.running_count() == 0:
                break

            # Fail-fast check
            if fail_fast:
                if any(j.state.value == 'failed' for j in queue.get_completed_jobs()):
                    print("\n[!] Fail-fast triggered. Stopping scheduler...")
                    scheduler.stop()
                    break
            
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\nStopping Scheduler...")
        scheduler.stop()
        time.sleep(1)

    # 7. Statistics
    failed_jobs = [j for j in queue.get_completed_jobs() if j.exit_code != 0]
    stats = {
        'success': queue.completed_count() - len(failed_jobs),
        'failed': len(failed_jobs)
    }
    return stats