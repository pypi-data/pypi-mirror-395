import subprocess
import signal
from unittest.mock import patch, MagicMock

import pytest

from reviewhound.tui.services.process import ProcessManager, ProcessInfo, ProcessType


class TestProcessManager:
    def test_start_web_server(self):
        manager = ProcessManager()

        mock_popen = MagicMock()
        mock_popen.pid = 12345
        mock_popen.poll.return_value = None  # Still running

        with patch("subprocess.Popen", return_value=mock_popen) as mock:
            success = manager.start(ProcessType.WEB)

        assert success is True
        assert ProcessType.WEB in manager._processes
        # Verify correct command
        call_args = mock.call_args[0][0]
        assert "reviewhound" in " ".join(call_args)
        assert "web" in call_args

    def test_start_scheduler(self):
        manager = ProcessManager()

        mock_popen = MagicMock()
        mock_popen.pid = 12346
        mock_popen.poll.return_value = None

        with patch("subprocess.Popen", return_value=mock_popen) as mock:
            success = manager.start(ProcessType.SCHEDULER)

        assert success is True
        call_args = mock.call_args[0][0]
        assert "watch" in call_args

    def test_stop_process(self):
        manager = ProcessManager()

        mock_popen = MagicMock()
        mock_popen.pid = 12345
        mock_popen.poll.return_value = None

        with patch("subprocess.Popen", return_value=mock_popen):
            manager.start(ProcessType.WEB)

        success = manager.stop(ProcessType.WEB)

        assert success is True
        mock_popen.terminate.assert_called_once()
        assert ProcessType.WEB not in manager._processes

    def test_get_process_info_running(self):
        manager = ProcessManager()

        mock_popen = MagicMock()
        mock_popen.pid = 12345
        mock_popen.poll.return_value = None

        with patch("subprocess.Popen", return_value=mock_popen):
            manager.start(ProcessType.WEB)

        info = manager.get_info(ProcessType.WEB)

        assert info is not None
        assert info.pid == 12345
        assert info.running is True

    def test_get_process_info_stopped(self):
        manager = ProcessManager()

        info = manager.get_info(ProcessType.WEB)

        assert info is not None
        assert info.running is False
        assert info.pid is None

    def test_get_output(self):
        manager = ProcessManager()

        mock_popen = MagicMock()
        mock_popen.pid = 12345
        mock_popen.poll.return_value = None
        mock_popen.stdout.readline.side_effect = ["line1\n", "line2\n", ""]

        with patch("subprocess.Popen", return_value=mock_popen):
            manager.start(ProcessType.WEB)

        # Read first line
        line = manager.read_output(ProcessType.WEB)
        assert line == "line1\n"
