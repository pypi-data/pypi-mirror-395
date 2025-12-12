import logging
from datetime import datetime, date

import requests

from reviewhound.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class YelpAPIScraper(BaseScraper):
    """Scraper that uses Yelp Fusion API to fetch reviews."""

    source = "yelp"
    BASE_URL = "https://api.yelp.com/v3"

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def _get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}"}

    def scrape(self, business_id: str) -> list[dict]:
        """Fetch reviews for a Yelp business ID.

        Args:
            business_id: Yelp business ID or alias (e.g., 'gary-danko-san-francisco')

        Returns:
            List of review dicts
        """
        self._current_business_id = business_id  # Store for URL construction
        url = f"{self.BASE_URL}/businesses/{business_id}/reviews"

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            data = response.json()

            reviews_data = data.get("reviews", [])
            return [self._parse_review(r) for r in reviews_data if r]

        except requests.RequestException as e:
            logger.warning(f"Yelp Fusion API request failed: {e}")
            return []

    def _parse_review(self, data: dict) -> dict:
        """Parse a single review from Yelp Fusion API response."""
        review_date = None
        if data.get("time_created"):
            try:
                review_date = datetime.strptime(
                    data["time_created"], "%Y-%m-%d %H:%M:%S"
                ).date()
            except ValueError:
                pass

        # Yelp API may include review URL, or construct one
        review_url = data.get("url")
        if not review_url:
            business_id = getattr(self, '_current_business_id', None)
            review_id = data.get("id")
            if business_id and review_id:
                review_url = f"https://www.yelp.com/biz/{business_id}?hrid={review_id}"

        return {
            "external_id": data.get("id", ""),
            "review_url": review_url,
            "author_name": data.get("user", {}).get("name", "Anonymous"),
            "rating": float(data.get("rating", 0)) if data.get("rating") else None,
            "text": data.get("text", ""),
            "review_date": review_date,
        }

    def search(self, query: str, location: str | None = None) -> list[dict]:
        """Search for businesses matching the query.

        Args:
            query: Business name to search for
            location: Location to search in (required by Yelp API)

        Returns:
            List of business dicts with id, name, address, rating
        """
        url = f"{self.BASE_URL}/businesses/search"
        params = {
            "term": query,
            "location": location or "United States",
            "limit": 5,
        }

        try:
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            results = []
            for biz in data.get("businesses", []):
                location_parts = []
                loc = biz.get("location", {})
                if loc.get("address1"):
                    location_parts.append(loc["address1"])
                if loc.get("city"):
                    location_parts.append(loc["city"])
                if loc.get("state"):
                    location_parts.append(loc["state"])

                results.append({
                    "name": biz.get("name", ""),
                    "address": ", ".join(location_parts),
                    "rating": biz.get("rating"),
                    "review_count": biz.get("review_count", 0),
                    "business_id": biz.get("id"),
                    "url": biz.get("url"),
                    "thumbnail_url": biz.get("image_url"),
                })

            return results

        except requests.RequestException as e:
            logger.warning(f"Yelp Fusion search failed: {e}")
            return []
