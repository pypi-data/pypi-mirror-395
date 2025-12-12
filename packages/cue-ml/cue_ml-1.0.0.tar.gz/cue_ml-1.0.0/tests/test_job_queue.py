import pytest
from cuepy.job_queue import JobQueue, Job, JobState

def test_fifo_ordering():
    q = JobQueue()
    j1 = Job(id="1", script="s.py", args=[])
    j2 = Job(id="2", script="s.py", args=[])
    
    q.add_job(j1)
    q.add_job(j2)
    
    assert q.get_next_job().id == "1"
    assert q.get_next_job().id == "2"

def test_state_transitions():
    q = JobQueue()
    j1 = Job(id="1", script="s.py", args=[])
    q.add_job(j1)
    
    # --- FIX: Simulate the scheduler popping the job first ---
    popped_job = q.get_next_job()
    assert popped_job.id == "1"
    # ---------------------------------------------------------

    # 1. Mark Running
    q.mark_job_running("1", gpu_ids=[0])
    assert q.running_count() == 1
    assert q.queued_count() == 0  # Now this will pass
    assert q.get_job("1").state == JobState.RUNNING
    
    # 2. Mark Completed
    q.mark_job_completed("1", exit_code=0)
    assert q.running_count() == 0
    assert q.completed_count() == 1
    assert q.get_job("1").state == JobState.COMPLETED

def test_missing_job_handling():
    q = JobQueue()
    # Try to update a job that doesn't exist
    result = q.mark_job_completed("ghost_job", 0)
    assert result is False