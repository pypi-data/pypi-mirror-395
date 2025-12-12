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
import textwrap
import argparse
from typing import TextIO
from dataclasses import dataclass

from cuepy.__version__ import __version__

@dataclass
class Environment:
    """Captures the I/O environment to allow easier testing of CLI outputs."""
    stdin: TextIO = sys.stdin
    stdout: TextIO = sys.stdout
    stderr: TextIO = sys.stderr
    is_terminal: bool = sys.stdout.isatty()

    def log_error(self, message: str):
       self.stderr.write(f"\033[91m[Error]\033[0m {message}\n")

class CueArgumentParser(argparse.ArgumentParser):
    """Custom parser to handle environment-specific printing and post-validation."""
    
    def __init__(self, env: Environment = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = env or Environment()

    def parse_args(self, args=None, namespace=None):
        # 1. Standard parsing handled by the parent class
        parsed_args = super().parse_args(args, namespace)
        
        # 2. Post-processing logic (validation that requires file system access)
        self._validate_path(parsed_args)
        self._process_verbosity(parsed_args)
        
        return parsed_args

    def _validate_path(self, args):
        # Ensure the config file actually exists before we try to process it
        if not os.path.exists(args.path):
            self.error(f"Configuration file not found: '{args.path}'")

    def _process_verbosity(self, args):
        # If debug is on, verbose should automatically be on
        if args.debug:
            args.verbose = True

    # Override error to use our custom environment printer instead of default sys.stderr
    def error(self, message):
        self.print_usage(self.env.stderr)
        self.env.log_error(message)
        sys.exit(2)

def get_parser(env: Environment = None) -> CueArgumentParser:
    """Constructs the argument parser with all available flags."""
    
    parser = CueArgumentParser(
        env=env,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
            Cue: Lightweight GPU Job Scheduler
            ---------------------------------------------------------------
            Runs a sequence of experiments defined in a YAML/JSON file,
            managing logs, errors, and resources automatically.
        """)
    )

    # -- Group: Essential Inputs --
    source_group = parser.add_argument_group(title="Source")
    source_group.add_argument(
        "-p", "--path",
        metavar="FILE",
        required=True,
        help="Path to the experiment configuration file"
    )

    # -- Group: Execution Control --
    exec_group = parser.add_argument_group(title="Execution Control")
    exec_group.add_argument(
        "--fail-fast",
        action="store_true",
        default=False,
        help="Stop the entire queue immediately if a single run fails."
    )
    exec_group.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Simulate the execution plan without running any scripts."
    )
    
    # Simulation mode for testing on non-GPU machines
    exec_group.add_argument(
        "--simulate",
        type=int,
        default=0,
        metavar="N",
        help="Run in simulation mode with N fake GPUs (for testing on non-CUDA machines)."
    )

    exec_group.add_argument(
        "--gpus",
        type=int,
        default=1,
        metavar="N",
        help="Default number of GPUs required per job (default: 1). Can be overridden in config."
    )

    # -- Group: Troubleshooting & Info --
    debug_group = parser.add_argument_group(title="Troubleshooting")
    debug_group.add_argument(
        "--debug",
        action="store_true",
        help="Print detailed diagnostic information for bug reports."
    )
    debug_group.add_argument(
        "-v", "--version",
        action="version",
        version=f"cue {__version__}",
        help="Show version and exit."
    )

    return parser