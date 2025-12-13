import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from relm.runner import run_project_command

def test_run_project_command_success():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        result = run_project_command(Path("/tmp/test"), "echo hello")
        assert result is True
        mock_run.assert_called_once_with(
            "echo hello",
            cwd=Path("/tmp/test"),
            shell=True,
            check=False
        )

def test_run_project_command_failure_exit_code():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        result = run_project_command(Path("/tmp/test"), "exit 1")
        assert result is False

def test_run_project_command_exception():
    with patch("subprocess.run", side_effect=Exception("Boom")):
        result = run_project_command(Path("/tmp/test"), "echo hello")
        assert result is False
