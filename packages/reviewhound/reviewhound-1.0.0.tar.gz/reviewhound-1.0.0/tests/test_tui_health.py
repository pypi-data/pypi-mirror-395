from unittest.mock import patch, MagicMock

import pytest

from reviewhound.tui.services.health import HealthChecker, HealthStatus


class TestHealthChecker:
    def test_check_web_healthy(self):
        checker = HealthChecker()

        mock_response = MagicMock()
        mock_response.status_code = 200

        with patch("requests.get", return_value=mock_response):
            status = checker.check_web()

        assert status.healthy is True
        assert status.message == "200 OK"

    def test_check_web_unhealthy(self):
        checker = HealthChecker()

        mock_response = MagicMock()
        mock_response.status_code = 500

        with patch("requests.get", return_value=mock_response):
            status = checker.check_web()

        assert status.healthy is False

    def test_check_web_connection_error(self):
        checker = HealthChecker()

        with patch("requests.get", side_effect=Exception("Connection refused")):
            status = checker.check_web()

        assert status.healthy is False
        assert "Connection refused" in status.message

    def test_check_database(self):
        checker = HealthChecker()

        mock_session = MagicMock()
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=False)
        mock_session.query.return_value.count.return_value = 42

        with patch("reviewhound.tui.services.health.get_session", return_value=mock_session):
            status = checker.check_database()

        assert status.healthy is True
        assert "42" in status.message

    def test_get_all_status(self):
        checker = HealthChecker()

        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_session = MagicMock()
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=False)
        mock_session.query.return_value.count.return_value = 10

        with patch("requests.get", return_value=mock_response):
            with patch("reviewhound.tui.services.health.get_session", return_value=mock_session):
                all_status = checker.check_all()

        assert "web" in all_status
        assert "database" in all_status
