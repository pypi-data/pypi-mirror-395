# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import sys
import os

from .cli import get_parser, Environment
from .config import load_and_validate
from .system import print_system_status
from .engine import run_sequence
from .gpu_detect import create_gpu_pool_from_detection, has_gpus
from .gpu_pool import GPUPool, GPU

def main():
    """Main entry point for the cue application."""
    
    # Initialize environment and parse arguments
    env = Environment()
    parser = get_parser(env)
    args = parser.parse_args()

    # 1. System Check
    # We skip system status if we are simulating, as real hardware stats aren't relevant
    if not args.dry_run and args.simulate == 0:
        try: 
            print_system_status()
        except Exception: 
            pass

    # 2. Config Loading
    try: 
        config_data, config_abs_path = load_and_validate(args.path)
    except Exception as e:
        env.log_error(f"Configuration Failed: {e}")
        return 1

    # Extract global settings (with defaults)
    conf_global = config_data.get('config', {})
    python_cmd = conf_global.get('python_cmd', sys.executable)
    log_dir = conf_global.get('log_dir', 'logs')

    # 3. GPU Detection / Simulation Logic
    pool = None

    if args.simulate > 0:
        # --- SIMULATION MODE (No real GPUs needed) ---
        pool = GPUPool()
        for i in range(args.simulate):
            # Create N fake GPUs for testing scheduler logic
            pool.add_gpu(GPU(id=i, name=f"Simulated-GPU-{i}"))
        
        print(f"\033[93m[Info] Running in SIMULATION mode with {args.simulate} fake GPUs.\033[0m")

    elif has_gpus():
        # --- REAL HARDWARE MODE ---
        pool = create_gpu_pool_from_detection()

    else:
        # --- NO HARDWARE DETECTED ---
        if args.dry_run:
            # For dry runs, we create an empty pool just to satisfy object requirements
            pool = GPUPool()
        else:
            env.log_error("No NVIDIA GPUs detected. Use --simulate N to test without GPUs.")
            return 1
    
    if args.debug:
        print(f"[Debug] Pool Created: {pool}")

    # 4. Run Engine (The Scheduler Loop)
    try:
        stats = run_sequence(
            experiments=config_data['experiments'],
            config_path=config_abs_path,
            pool=pool,
            python_cmd=python_cmd,
            log_root=log_dir,
            fail_fast=args.fail_fast,
            dry_run=args.dry_run,
            default_gpu_req=args.gpus,
        )
    except KeyboardInterrupt:
        # Engine handles the clean shutdown of scheduler, this catches the final exit
        env.log_error("Execution interrupted by user.")
        return 130
    except Exception as e:
        env.log_error(f"Engine Crash: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1

    # 5. Final Summary
    if not args.dry_run:
        print("\n[Final Summary]")
        if stats['failed'] == 0:
            print(f"\033[1;32m✓ All {stats['success']} runs completed successfully.\033[0m")
            return 0
        else:
            print(f"\033[1;31m✗ Completed: {stats['success']} | Failed: {stats['failed']}\033[0m")
            return 1
    
    return 0