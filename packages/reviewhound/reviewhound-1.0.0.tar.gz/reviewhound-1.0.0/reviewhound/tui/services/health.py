from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests

from reviewhound.database import get_session
from reviewhound.models import Review, Business


@dataclass
class HealthStatus:
    """Status of a health check."""
    name: str
    healthy: bool
    message: str
    checked_at: datetime


class HealthChecker:
    """Performs health checks on services."""

    def __init__(self, web_url: str = "http://localhost:5000"):
        self.web_url = web_url

    def check_web(self, timeout: float = 2.0) -> HealthStatus:
        """Check if the web server is responding."""
        try:
            response = requests.get(self.web_url, timeout=timeout)
            healthy = response.status_code == 200
            message = f"{response.status_code} OK" if healthy else f"{response.status_code}"
        except requests.exceptions.ConnectionError:
            healthy = False
            message = "Connection refused"
        except requests.exceptions.Timeout:
            healthy = False
            message = "Timeout"
        except Exception as e:
            healthy = False
            message = str(e)

        return HealthStatus(
            name="web",
            healthy=healthy,
            message=message,
            checked_at=datetime.now(),
        )

    def check_database(self) -> HealthStatus:
        """Check database connectivity and get stats."""
        try:
            with get_session() as session:
                review_count = session.query(Review).count()
                business_count = session.query(Business).count()

            return HealthStatus(
                name="database",
                healthy=True,
                message=f"{review_count} reviews, {business_count} businesses",
                checked_at=datetime.now(),
            )
        except Exception as e:
            return HealthStatus(
                name="database",
                healthy=False,
                message=str(e),
                checked_at=datetime.now(),
            )

    def check_all(self) -> dict[str, HealthStatus]:
        """Run all health checks."""
        return {
            "web": self.check_web(),
            "database": self.check_database(),
        }
