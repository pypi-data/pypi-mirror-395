import random
import time
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from reviewhound.config import Config

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


class BaseScraper(ABC):
    source: str = ""

    def __init__(self):
        self.session = requests.Session()

    def get_headers(self) -> dict:
        return {"User-Agent": random.choice(USER_AGENTS)}

    def rate_limit(self):
        delay = random.uniform(Config.REQUEST_DELAY_MIN, Config.REQUEST_DELAY_MAX)
        time.sleep(delay)

    def fetch(self, url: str) -> BeautifulSoup:
        self.rate_limit()
        response = self.session.get(url, headers=self.get_headers(), timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    @abstractmethod
    def scrape(self, url: str) -> list[dict]:
        """Return list of review dicts with keys:
        external_id, author_name, rating, text, review_date
        """
        pass

    def search(self, query: str, location: str | None = None) -> list[dict]:
        """Search for businesses on this platform.

        Args:
            query: Business name to search for
            location: Optional location to narrow results

        Returns:
            List of dicts with keys:
            name, address, rating, review_count, url, thumbnail_url
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support search")
