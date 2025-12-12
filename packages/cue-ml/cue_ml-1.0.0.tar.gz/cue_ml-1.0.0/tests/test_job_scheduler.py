import pytest
import time
from unittest.mock import patch
from cuepy.scheduler import Scheduler
from cuepy.job_queue import JobQueue, Job, JobState
from cuepy.gpu_pool import GPUPool, GPU

@pytest.fixture
def scheduler_stack(tmp_path):
    pool = GPUPool()
    pool.add_gpu(GPU(id=0, name="MockGPU"))
    queue = JobQueue()
    scheduler = Scheduler(pool, queue, log_root=str(tmp_path))
    return scheduler, pool, queue

@patch("cuepy.scheduler.execute_job")
def test_scheduler_cycle(mock_exec, scheduler_stack):
    """
    Full integration test:
    1. Add Job
    2. Start Scheduler
    3. Ensure Job gets picked up + executed
    4. Ensure GPU is released
    """
    scheduler, pool, queue = scheduler_stack
    
    # Mock execution to succeed immediately
    mock_exec.return_value = (True, 0)
    
    # 1. Add Job
    job = Job(id="j1", script="run.py", args=[])
    queue.add_job(job)
    
    # 2. Start Scheduler (Non-blocking)
    scheduler.start(join=False)
    
    # Wait max 2 seconds for processing
    timeout = 2.0
    start = time.time()
    while queue.completed_count() == 0:
        if time.time() - start > timeout:
            pytest.fail("Scheduler timed out processing job")
        time.sleep(0.1)
    
    scheduler.stop()
    
    # 3. Assertions
    assert queue.get_job("j1").state == JobState.COMPLETED
    assert mock_exec.called
    
    # 4. Ensure GPU was released back to pool
    assert pool.available_count() == 1
    assert pool.get_gpu(0).state.value == "idle"

@patch("cuepy.scheduler.execute_job")
def test_scheduler_insufficient_resources(mock_exec, scheduler_stack):
    """Test that scheduler ignores jobs requesting too many GPUs."""
    scheduler, pool, queue = scheduler_stack
    
    # Job needs 2 GPUs, but pool only has 1
    job = Job(id="greedy", script="run.py", args=[], gpu_req=2)
    queue.add_job(job)
    
    scheduler.start(join=False)
    time.sleep(0.5) # Let it loop a few times
    scheduler.stop()
    
    # Job should still be queued, not run
    assert queue.get_job("greedy").state == JobState.QUEUED
    assert mock_exec.called is False