import logging
from datetime import datetime, date

import requests

from reviewhound.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class GooglePlacesScraper(BaseScraper):
    """Scraper that uses Google Places API to fetch reviews."""

    source = "google"
    BASE_URL = "https://maps.googleapis.com/maps/api/place"

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def scrape(self, place_id: str) -> list[dict]:
        """Fetch reviews for a Google Place ID.

        Args:
            place_id: Google Place ID (e.g., 'ChIJN1t_tDeuEmsRUsoyG83frY4')

        Returns:
            List of review dicts
        """
        self._current_place_id = place_id  # Store for URL construction
        url = f"{self.BASE_URL}/details/json"
        params = {
            "place_id": place_id,
            "fields": "reviews",
            "key": self.api_key,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "OK":
                logger.warning(f"Google Places API error: {data.get('status')} - {data.get('error_message', '')}")
                return []

            reviews_data = data.get("result", {}).get("reviews", [])
            return [self._parse_review(r) for r in reviews_data if r]

        except requests.RequestException as e:
            logger.warning(f"Google Places API request failed: {e}")
            return []

    def _parse_review(self, data: dict) -> dict:
        """Parse a single review from Google Places API response."""
        # Google uses Unix timestamp
        review_date = None
        if data.get("time"):
            try:
                review_date = datetime.fromtimestamp(data["time"]).date()
            except (ValueError, OSError):
                pass

        # Google doesn't provide individual review URLs, link to reviews page
        place_id = getattr(self, '_current_place_id', None)
        review_url = f"https://search.google.com/local/reviews?placeid={place_id}" if place_id else None

        return {
            "external_id": f"google_{data.get('time', '')}_{hash(data.get('author_name', ''))}",
            "review_url": review_url,
            "author_name": data.get("author_name", "Anonymous"),
            "rating": float(data.get("rating", 0)) if data.get("rating") else None,
            "text": data.get("text", ""),
            "review_date": review_date,
        }

    def search(self, query: str, location: str | None = None) -> list[dict]:
        """Search for places matching the query.

        Args:
            query: Business name to search for
            location: Optional location to narrow results

        Returns:
            List of place dicts with id, name, address, rating
        """
        url = f"{self.BASE_URL}/textsearch/json"
        search_query = f"{query} {location}" if location else query
        params = {
            "query": search_query,
            "key": self.api_key,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "OK":
                logger.warning(f"Google Places search error: {data.get('status')}")
                return []

            results = []
            for place in data.get("results", [])[:5]:
                results.append({
                    "name": place.get("name", ""),
                    "address": place.get("formatted_address", ""),
                    "rating": place.get("rating"),
                    "review_count": place.get("user_ratings_total", 0),
                    "place_id": place.get("place_id"),
                    "url": None,  # Google doesn't provide direct URLs in API
                    "thumbnail_url": None,
                })

            return results

        except requests.RequestException as e:
            logger.warning(f"Google Places search failed: {e}")
            return []
