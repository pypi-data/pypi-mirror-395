import subprocess
from unittest.mock import patch, MagicMock

import pytest

from reviewhound.tui.services.docker import DockerManager, ContainerStatus


class TestDockerManager:
    def test_get_container_status_running(self):
        manager = DockerManager()
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "running"

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            status = manager.get_container_status("reviewhound")

        assert status == ContainerStatus.RUNNING
        mock_run.assert_called_once()

    def test_get_container_status_stopped(self):
        manager = DockerManager()
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch("subprocess.run", return_value=mock_result):
            status = manager.get_container_status("reviewhound")

        assert status == ContainerStatus.STOPPED

    def test_get_container_status_docker_not_available(self):
        manager = DockerManager()

        with patch("subprocess.run", side_effect=FileNotFoundError):
            status = manager.get_container_status("reviewhound")

        assert status == ContainerStatus.UNKNOWN

    def test_start_container(self):
        manager = DockerManager()
        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            success = manager.start()

        assert success is True
        # Should call docker-compose up -d
        call_args = mock_run.call_args[0][0]
        assert "docker-compose" in call_args or "docker" in call_args

    def test_stop_container(self):
        manager = DockerManager()
        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            success = manager.stop()

        assert success is True

    def test_get_logs(self):
        manager = DockerManager()
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "log line 1\nlog line 2\n"
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            logs = manager.get_logs(tail=10)

        assert "log line 1" in logs
        assert "log line 2" in logs
