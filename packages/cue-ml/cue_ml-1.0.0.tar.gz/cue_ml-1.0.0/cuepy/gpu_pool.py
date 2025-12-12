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
from typing import Optional, List, Dict

class GPUState(Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

class GPULocation(Enum):
    LOCAL = "local"
    REMOTE = "remote"

@dataclass
class GPU:
    """Represents a single physical or simulated GPU resource."""
    id: int
    name: str
    state: GPUState = GPUState.IDLE
    location: GPULocation = GPULocation.LOCAL
    cluster_id: str = "local"
    assigned_job_id: Optional[str] = None
    last_used: Optional[float] = None
    error_message: Optional[str] = None
    
    def mark_busy(self, job_id: str) -> None:
        self.state = GPUState.BUSY
        self.assigned_job_id = job_id
    
    def mark_idle(self) -> None:
        self.state = GPUState.IDLE
        self.assigned_job_id = None
        self.last_used = time.time()
    
    def mark_error(self, error_message: str) -> None:
        self.state = GPUState.ERROR
        self.error_message = error_message
        self.assigned_job_id = None
    
    def mark_offline(self) -> None:
        self.state = GPUState.OFFLINE
        self.assigned_job_id = None
    
    def is_available(self) -> bool: 
        return self.state == GPUState.IDLE

    def __repr__(self) -> str:
        job_info = f", job={self.assigned_job_id}" if self.assigned_job_id else ""
        return f"GPU(id={self.id}, name='{self.name}', state={self.state.value}{job_info})"

class GPUPool:    
    """Manages a collection of GPU resources and handles their allocation."""
    
    def __init__(self):
        self._gpus: Dict[int, GPU] = {}
        self._cluster_map: Dict[str, List[int]] = {}
    
    def add_gpu(self, gpu: GPU) -> None:
        self._gpus[gpu.id] = gpu
        
        # Track by cluster for faster lookups
        if gpu.cluster_id not in self._cluster_map:
            self._cluster_map[gpu.cluster_id] = []
        self._cluster_map[gpu.cluster_id].append(gpu.id)
    
    def remove_gpu(self, gpu_id: int) -> None:
        if gpu_id in self._gpus:
            gpu = self._gpus[gpu_id]
            if gpu.cluster_id in self._cluster_map:
                self._cluster_map[gpu.cluster_id].remove(gpu_id)
            del self._gpus[gpu_id]
    
    def get_available_gpu(self, cluster_id: Optional[str] = None) -> Optional[GPU]:
        """Finds the first available single GPU."""
        gpus_to_check = self._gpus.values()
        
        if cluster_id:
            gpu_ids = self._cluster_map.get(cluster_id, [])
            gpus_to_check = [self._gpus[gid] for gid in gpu_ids]
        
        for gpu in gpus_to_check:
            if gpu.is_available(): 
                return gpu

        return None
    
    def allocate_gpu(self, job_id: str, cluster_id: Optional[str] = None) -> Optional[GPU]:
        """Convenience method to find and lock a single GPU."""
        gpu = self.get_available_gpu(cluster_id)
        if gpu: 
            gpu.mark_busy(job_id)
        return gpu
    
    def deallocate_gpu(self, gpu_id: int) -> bool:
        """Releases a GPU back to the IDLE pool."""
        gpu = self.get_gpu(gpu_id)
        if gpu:
            gpu.mark_idle()
            return True
        return False

    def allocate_gpus(self, job_id: str, count: int = 1, cluster_id: Optional[str] = None) -> List[GPU]:
        """
        Attempts to allocate 'count' number of GPUs atomically.
        If 'count' GPUs are not available, it returns an empty list (no partial allocation).
        """
        available = []
        
        # Filter by cluster if needed
        gpus_to_check = self._gpus.values()
        if cluster_id:
            gpu_ids = self._cluster_map.get(cluster_id, [])
            gpus_to_check = [self._gpus[gid] for gid in gpu_ids]

        # Find enough idle GPUs
        for gpu in gpus_to_check:
            if gpu.is_available():
                available.append(gpu)
                if len(available) == count:
                    break
        
        # If we found enough, mark them ALL as busy
        if len(available) == count:
            for gpu in available:
                gpu.mark_busy(job_id)
            return available
            
        return [] # Not enough resources available yet
    
    def get_gpu(self, gpu_id: int) -> Optional[GPU]: 
        return self._gpus.get(gpu_id)
    
    def get_all_gpus(self) -> List[GPU]: 
        return list(self._gpus.values())
    
    def get_idle_gpus(self) -> List[GPU]: 
        return [gpu for gpu in self._gpus.values() if gpu.state == GPUState.IDLE]
    
    def get_busy_gpus(self) -> List[GPU]: 
        return [gpu for gpu in self._gpus.values() if gpu.state == GPUState.BUSY]
    
    def get_clusters(self) -> List[str]: 
        return list(self._cluster_map.keys())
    
    def total_gpus(self) -> int: 
        return len(self._gpus)
    
    def available_count(self) -> int: 
        return len(self.get_idle_gpus())
    
    def busy_count(self) -> int: 
        return len(self.get_busy_gpus())
    
    def get_cluster_gpus(self, cluster_id: str) -> List[GPU]:
        gpu_ids = self._cluster_map.get(cluster_id, [])
        return [self._gpus[gid] for gid in gpu_ids]
    
    def get_status_summary(self) -> Dict[str, int]:
        summary = {state.value: 0 for state in GPUState}
        for gpu in self._gpus.values(): 
            summary[gpu.state.value] += 1
        return summary
    
    def __repr__(self) -> str:
        return (f"GPUPool(total={self.total_gpus()}, "
                f"idle={self.available_count()}, "
                f"busy={self.busy_count()})")