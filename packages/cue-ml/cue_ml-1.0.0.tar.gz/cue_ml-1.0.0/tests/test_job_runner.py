import pytest
import os
from unittest.mock import patch, MagicMock
from cuepy.job_runner import execute_job
from cuepy.job_queue import Job
from cuepy.gpu_pool import GPU

@patch("subprocess.Popen")
def test_execute_job_success(mock_popen, tmp_path):
    # Setup Mock Process
    process_mock = MagicMock()
    process_mock.wait.return_value = 0 # Exit code 0 (Success)
    mock_popen.return_value = process_mock

    # Setup Inputs
    job = Job(id="test_run", script="/abs/train.py", args=["--flag"])
    gpus = [GPU(id=0, name="T4"), GPU(id=1, name="T4")]
    log_file = tmp_path / "test.log"

    # Run
    success, code = execute_job(job, gpus, str(log_file))

    # Assertions
    assert success is True
    assert code == 0
    
    # Verify Popen was called with correct Env Vars
    args, kwargs = mock_popen.call_args
    env_used = kwargs['env']
    assert env_used['CUDA_VISIBLE_DEVICES'] == "0,1"
    assert env_used['PYTHONUNBUFFERED'] == "1"
    
    # Verify Command Construction
    cmd_used = args[0]
    assert cmd_used[-2:] == ["/abs/train.py", "--flag"]

@patch("subprocess.Popen")
def test_execute_job_failure(mock_popen, tmp_path):
    # Setup Mock Process to fail
    process_mock = MagicMock()
    process_mock.wait.return_value = 1 # Exit code 1 (Error)
    mock_popen.return_value = process_mock

    job = Job(id="fail_run", script="s.py", args=[])
    gpus = [GPU(id=0, name="T4")]
    
    success, code = execute_job(job, gpus, str(tmp_path / "fail.log"))
    
    assert success is False
    assert code == 1