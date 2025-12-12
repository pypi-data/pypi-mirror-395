import pytest
from cuepy.gpu_pool import GPUPool, GPU, GPUState

def test_add_remove_gpu():
    pool = GPUPool()
    gpu = GPU(id=0, name="TestGPU")
    
    pool.add_gpu(gpu)
    assert pool.total_gpus() == 1
    assert pool.get_gpu(0).name == "TestGPU"
    
    pool.remove_gpu(0)
    assert pool.total_gpus() == 0

def test_allocation_single(populated_pool):
    """Test allocating 1 GPU."""
    assert populated_pool.available_count() == 2
    
    # Request 1 GPU
    gpus = populated_pool.allocate_gpus(job_id="job_1", count=1)
    
    assert len(gpus) == 1
    assert gpus[0].state == GPUState.BUSY
    assert gpus[0].assigned_job_id == "job_1"
    assert populated_pool.available_count() == 1

def test_allocation_multi(populated_pool):
    """Test allocating 2 GPUs at once."""
    gpus = populated_pool.allocate_gpus(job_id="job_multi", count=2)
    
    assert len(gpus) == 2
    assert gpus[0].assigned_job_id == "job_multi"
    assert gpus[1].assigned_job_id == "job_multi"
    assert populated_pool.available_count() == 0

def test_allocation_failure(populated_pool):
    """Test requesting more GPUs than available."""
    # Pool has 2, request 3
    gpus = populated_pool.allocate_gpus(job_id="job_greedy", count=3)
    
    # Should return empty list (atomic failure)
    assert gpus == []
    # Should not have locked any GPUs
    assert populated_pool.available_count() == 2

def test_deallocation(populated_pool):
    gpus = populated_pool.allocate_gpus("job_1", 1)
    gpu_id = gpus[0].id
    
    assert populated_pool.get_gpu(gpu_id).state == GPUState.BUSY
    
    populated_pool.deallocate_gpu(gpu_id)
    assert populated_pool.get_gpu(gpu_id).state == GPUState.IDLE
    assert populated_pool.available_count() == 2