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
import subprocess
from datetime import datetime
from typing import Tuple, List

# Type hinting imports
from .job_queue import Job
from .gpu_pool import GPU

def execute_job(
    job: Job, 
    gpus: List[GPU], 
    log_path: str, 
    python_cmd: str = sys.executable
) -> Tuple[bool, int]:
    """
    Executes a single job on the assigned GPU(s) using a subprocess.
    
    Args:
        job: The Job object containing script and arguments.
        gpus: A list of GPU objects assigned to this job.
        log_path: Absolute path where the log file should be written.
        python_cmd: Path to the python interpreter (defaults to sys.executable).
        
    Returns:
        Tuple[bool, int]: (Success boolean, Exit Code)
    """
    
    # 1. Prepare Command
    # job.script is the absolute path (resolved by engine/loader)
    cmd = [python_cmd, job.script] + job.args

    # 2. Setup Environment
    # This is crucial for GPU isolation: we only expose the assigned IDs to the script
    env = os.environ.copy()
    gpu_ids_str = ",".join(str(g.id) for g in gpus)
    env['CUDA_VISIBLE_DEVICES'] = gpu_ids_str
    
    # Ensure logs are written immediately, not buffered in memory
    env['PYTHONUNBUFFERED'] = '1'

    # 3. Execution
    try:
        # Create directory for log if it doesn't exist
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, 'w') as f:
            _write_log_header(f, job, gpus, cmd)

            # Start Process
            # We redirect stderr to stdout so all output is captured in one file
            process = subprocess.Popen(
                cmd,
                stdout=f,       # Write directly to file
                stderr=subprocess.STDOUT, 
                env=env,
                text=True,
                bufsize=1       # Line buffered
            )

            # Wait for completion
            # This blocks the worker thread, but that is intended behavior 
            # as the scheduler spawns a specific thread for this job.
            exit_code = process.wait()

            _write_log_footer(f, exit_code)

            return (exit_code == 0), exit_code

    except Exception as e:
        # If we can't even start the process or write the log, return failure
        # In a real scenario, we might want to print this to stderr of the main process
        return False, -1


def _write_log_header(f, job, gpus, cmd):
    """Helper to write clean informational headers to the top of log files."""
    f.write("=" * 60 + "\n")
    f.write(f"Job ID:   {job.id}\n")
    f.write(f"Date:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    gpu_names = ", ".join([f"ID:{g.id} ({g.name})" for g in gpus])
    f.write(f"GPU(s):   {gpu_names}\n")
    
    f.write(f"Script:   {job.script}\n")
    f.write(f"Command:  {' '.join(cmd)}\n")
    f.write("=" * 60 + "\n\n")
    f.flush()

def _write_log_footer(f, exit_code):
    """Helper to write exit status footer."""
    f.write("\n\n" + "-" * 60 + "\n")
    f.write(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Exit Code: {exit_code}\n")
    
    status = "SUCCESS" if exit_code == 0 else "FAILED"
    f.write(f"Status:    {status}\n")
    f.write("-" * 60 + "\n")
    f.flush()