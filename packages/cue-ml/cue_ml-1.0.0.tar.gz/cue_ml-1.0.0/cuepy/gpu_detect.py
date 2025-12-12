# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import ctypes
from ctypes.util import find_library

# CUDA Driver API types
CUresult = ctypes.c_uint32
CUdevice = ctypes.c_int32

# Return code for success
CUDA_SUCCESS = 0

def load_cuda_driver():
    """Attempts to load the CUDA driver library (libcuda.so or nvcuda.dll)."""
    try:
        # standard lookup for Linux (libcuda) and MacOS
        lib_path = find_library('cuda')
        if lib_path: 
            return ctypes.CDLL(lib_path)
    except Exception: 
        pass
    return None

def setup_cuda_functions(dll):
    """Maps Python functions to the C types in the loaded DLL."""
    if not dll: return None
    
    funcs = {}
    try:
        # cuInit(flags)
        funcs['cuInit'] = dll.cuInit
        funcs['cuInit'].restype = CUresult
        funcs['cuInit'].argtypes = [ctypes.c_uint32]
        
        # cuDeviceGetCount(*count)
        funcs['cuDeviceGetCount'] = dll.cuDeviceGetCount
        funcs['cuDeviceGetCount'].restype = CUresult
        funcs['cuDeviceGetCount'].argtypes = [ctypes.POINTER(ctypes.c_int32)]
        
        # cuDeviceGet(*device, ordinal)
        funcs['cuDeviceGet'] = dll.cuDeviceGet
        funcs['cuDeviceGet'].restype = CUresult
        funcs['cuDeviceGet'].argtypes = [ctypes.POINTER(CUdevice), ctypes.c_int32]
        
        # cuDeviceGetName(name, len, device)
        funcs['cuDeviceGetName'] = dll.cuDeviceGetName
        funcs['cuDeviceGetName'].restype = CUresult
        funcs['cuDeviceGetName'].argtypes = [ctypes.POINTER(ctypes.c_char), ctypes.c_int32, CUdevice]
        
        return funcs
    except AttributeError: 
        return None

def detect_nvidia_gpus():
    """
    Scans the system for NVIDIA GPUs using the driver API.
    Returns a list of dictionaries containing ID and Name.
    """
    dll = load_cuda_driver()
    if not dll: return []
    
    funcs = setup_cuda_functions(dll)
    if not funcs: return []
    
    # 1. Initialize CUDA Driver API
    result = funcs['cuInit'](0)
    if result != CUDA_SUCCESS: return []
    
    # 2. Get device count
    count = ctypes.c_int32()
    result = funcs['cuDeviceGetCount'](ctypes.byref(count))
    if result != CUDA_SUCCESS or count.value == 0: return []
    
    # 3. Get info for each GPU
    gpus = []
    for i in range(count.value):
        device = CUdevice()
        result = funcs['cuDeviceGet'](ctypes.byref(device), i)
        if result != CUDA_SUCCESS: continue
        
        # Buffer to hold the name string
        name_buffer = ctypes.create_string_buffer(256)
        result = funcs['cuDeviceGetName'](name_buffer, 256, device)
        
        gpu_info = {
            'id': i,
            'name': name_buffer.value.decode() if result == CUDA_SUCCESS else 'Unknown',
            'success': result == CUDA_SUCCESS
        }
        gpus.append(gpu_info)
    
    return gpus

def get_gpu_count(): 
    return len(detect_nvidia_gpus())

def has_gpus(): 
    return get_gpu_count() > 0

def create_gpu_pool_from_detection():
    """Creates a GPUPool object populated with the detected hardware."""
    # Import locally to avoid circular dependencies during initialization
    from .gpu_pool import GPUPool, GPU, GPUState, GPULocation
    
    pool = GPUPool()
    detected_gpus = detect_nvidia_gpus()
    
    for gpu_info in detected_gpus:
        gpu = GPU(
            id=gpu_info['id'],
            name=gpu_info['name'],
            state=GPUState.IDLE if gpu_info['success'] else GPUState.ERROR,
            location=GPULocation.LOCAL,
            cluster_id="local",
            error_message=None if gpu_info['success'] else "Detection failed"
        )
        pool.add_gpu(gpu)
    
    return pool