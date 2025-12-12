# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import sys

def main():
    try:
        from cuepy.core import main as cue_main
        exit_status = cue_main()
    except KeyboardInterrupt:
        # Standard Unix convention: 128 + SIGINT (2) = 130
        exit_status = 130
        print("\n\n[!] cue execution cancelled.", file=sys.stderr)

    return exit_status

if __name__ == '__main__':
    sys.exit(main())