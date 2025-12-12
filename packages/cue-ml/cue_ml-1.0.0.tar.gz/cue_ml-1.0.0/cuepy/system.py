# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import platform
from cuepy.gpu_detect import detect_nvidia_gpus

def print_system_status():
    """Displays the host OS information and detected hardware accelerators."""
    
    # Identify Operating System and Architecture (e.g., Linux x86_64)
    print("  • Platform:      " + platform.system() + " " + platform.machine())
    
    # Check for available NVIDIA GPUs using the detection module
    gpus = detect_nvidia_gpus()
    
    if gpus:
        print(f"  • Accelerator:   Detected {len(gpus)} NVIDIA GPU(s):")
        for gpu in gpus: 
            print(f"    - [{gpu['id']}] {gpu['name']}")
    else: 
        print("  • Accelerator:   None (Running on CPU)")