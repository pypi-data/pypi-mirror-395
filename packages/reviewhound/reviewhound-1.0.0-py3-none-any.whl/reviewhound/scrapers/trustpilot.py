import json
import logging
import re
from datetime import datetime, date
from urllib.parse import quote_plus

import requests

from reviewhound.scrapers.base import BaseScraper
from reviewhound.config import Config

logger = logging.getLogger(__name__)


class TrustPilotScraper(BaseScraper):
    source = "trustpilot"

    def scrape(self, url: str) -> list[dict]:
        reviews = []
        base_url = url.split("?")[0]

        for page in range(1, Config.MAX_PAGES_PER_SOURCE + 1):
            page_url = base_url if page == 1 else f"{base_url}?page={page}"
            try:
                soup = self.fetch(page_url)
                page_reviews = self._parse_reviews(soup)
                reviews.extend(page_reviews)
            except requests.RequestException as e:
                logger.warning(f"TrustPilot scrape failed for {page_url}: {e}")
                break

        return reviews

    def _parse_reviews(self, soup) -> list[dict]:
        # Try Next.js __NEXT_DATA__ first (TrustPilot's current format)
        reviews = self._parse_next_data_reviews(soup)
        if reviews:
            return reviews

        # Try JSON-LD as fallback
        reviews = self._parse_json_ld_reviews(soup)
        if reviews:
            return reviews

        # Fall back to HTML parsing for backwards compatibility with tests
        reviews = []
        articles = soup.find_all("article", attrs={"data-review-id": True})

        for article in articles:
            try:
                review = self._parse_review(article)
                if review:
                    reviews.append(review)
            except (AttributeError, ValueError):
                continue

        return reviews

    def _parse_next_data_reviews(self, soup) -> list[dict]:
        """Parse reviews from Next.js __NEXT_DATA__ script."""
        script = soup.find("script", id="__NEXT_DATA__")
        if not script:
            return []

        try:
            data = json.loads(script.string)
            review_list = data.get("props", {}).get("pageProps", {}).get("reviews", [])
        except (json.JSONDecodeError, TypeError, AttributeError):
            return []

        reviews = []
        for item in review_list:
            review = self._parse_next_data_review(item)
            if review:
                reviews.append(review)

        return reviews

    def _parse_next_data_review(self, data: dict) -> dict | None:
        """Parse a single review from Next.js data."""
        review_id = data.get("id")
        if not review_id:
            return None

        # Author name from consumer object
        author_name = "Anonymous"
        consumer = data.get("consumer", {})
        if isinstance(consumer, dict):
            author_name = consumer.get("displayName") or "Anonymous"

        # Rating (integer 1-5)
        rating = data.get("rating")
        if rating is not None:
            rating = float(rating)

        # Text - combine title and text if both present
        title = data.get("title", "")
        text = data.get("text", "")
        if title and text:
            text = f"{title}\n\n{text}"
        elif title:
            text = title

        # Date from dates object
        review_date = None
        dates = data.get("dates", {})
        date_str = dates.get("publishedDate")
        if date_str:
            review_date = self._parse_iso_date(date_str)

        return {
            "external_id": str(review_id),
            "review_url": f"https://www.trustpilot.com/reviews/{review_id}",
            "author_name": author_name,
            "rating": rating,
            "text": text,
            "review_date": review_date,
        }

    def _parse_json_ld_reviews(self, soup) -> list[dict]:
        """Parse reviews from JSON-LD structured data."""
        reviews = []

        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
            except (json.JSONDecodeError, TypeError):
                continue

            # Handle both single objects and arrays
            items = data if isinstance(data, list) else [data]

            for item in items:
                # Look for Review type or review arrays
                if item.get("@type") == "Review":
                    review = self._parse_json_ld_review(item)
                    if review:
                        reviews.append(review)
                elif "review" in item:
                    for review_data in item.get("review", []):
                        review = self._parse_json_ld_review(review_data)
                        if review:
                            reviews.append(review)

        return reviews

    def _parse_json_ld_review(self, data: dict) -> dict | None:
        """Parse a single review from JSON-LD data."""
        review_id = data.get("id")
        if not review_id:
            return None

        # Author name from nested author object or consumer object
        author_name = "Anonymous"
        author = data.get("author") or data.get("consumer")
        if isinstance(author, dict):
            author_name = author.get("displayName") or author.get("name") or "Anonymous"
        elif isinstance(author, str):
            author_name = author

        # Rating
        rating = None
        rating_value = data.get("rating") or data.get("reviewRating")
        if isinstance(rating_value, dict):
            rating = float(rating_value.get("ratingValue", 0))
        elif rating_value is not None:
            rating = float(rating_value)

        # Text - combine title and text if both present
        title = data.get("title", "")
        text = data.get("text", "") or data.get("reviewBody", "")
        if title and text:
            text = f"{title}\n\n{text}"
        elif title:
            text = title

        # Date - try multiple fields
        review_date = None
        date_str = data.get("publishedDate") or data.get("datePublished")
        if date_str:
            review_date = self._parse_iso_date(date_str)

        return {
            "external_id": str(review_id),
            "review_url": f"https://www.trustpilot.com/reviews/{review_id}",
            "author_name": author_name,
            "rating": rating,
            "text": text,
            "review_date": review_date,
        }

    def _parse_review(self, article) -> dict | None:
        review_id = article.get("data-review-id")
        if not review_id:
            return None

        # Author name
        author_elem = article.select_one("aside a span")
        author_name = author_elem.get_text(strip=True) if author_elem else "Anonymous"

        # Rating
        rating_elem = article.find(attrs={"data-service-review-rating": True})
        rating = float(rating_elem.get("data-service-review-rating", 0)) if rating_elem else None

        # Review text
        text_elem = article.find(attrs={"data-service-review-text-typography": True})
        text = ""
        if text_elem:
            p = text_elem.find("p")
            text = p.get_text(strip=True) if p else text_elem.get_text(strip=True)

        # Date
        date_elem = article.find(attrs={"data-service-review-date-of-experience-typography": True})
        review_date = None
        if date_elem:
            p = date_elem.find("p")
            date_text = p.get_text(strip=True) if p else date_elem.get_text(strip=True)
            review_date = self._parse_date(date_text)

        return {
            "external_id": review_id,
            "review_url": f"https://www.trustpilot.com/reviews/{review_id}",
            "author_name": author_name,
            "rating": rating,
            "text": text,
            "review_date": review_date,
        }

    def _parse_date(self, text: str) -> date | None:
        match = re.search(r"(\w+ \d{1,2}, \d{4})", text)
        if match:
            try:
                return datetime.strptime(match.group(1), "%B %d, %Y").date()
            except ValueError:
                pass
        return None

    def _parse_iso_date(self, date_str: str) -> date | None:
        """Parse ISO 8601 date string."""
        try:
            # Handle formats like "2025-12-02T02:01:43.000Z"
            if "T" in date_str:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    def search(self, query: str, location: str | None = None) -> list[dict]:
        """Search TrustPilot for businesses matching the query."""
        search_url = f"https://www.trustpilot.com/search?query={quote_plus(query)}"

        try:
            soup = self.fetch(search_url)
        except requests.RequestException as e:
            logger.warning(f"TrustPilot search failed for '{query}': {e}")
            return []

        results = []
        cards = soup.select("a[name='business-unit-card']")[:5]

        for card in cards:
            try:
                result = self._parse_search_result(card)
                if result:
                    results.append(result)
            except (AttributeError, ValueError):
                continue

        return results

    def _parse_search_result(self, card) -> dict | None:
        href = card.get("href", "")
        if not href:
            return None

        url = f"https://www.trustpilot.com{href}" if href.startswith("/") else href

        # Find name - look for p tag with heading class
        name = ""
        for p in card.find_all("p"):
            classes = p.get("class", [])
            if any("heading" in c.lower() for c in classes):
                name = p.get_text(strip=True)
                break

        # Find location - in businessLocation div
        address = ""
        location_div = card.select_one("div[class*='businessLocation']")
        if location_div:
            p = location_div.find("p")
            address = p.get_text(strip=True) if p else ""

        # Find rating - look for trustScore span
        rating = None
        rating_span = card.select_one("span[class*='trustScore']")
        if rating_span:
            inner_span = rating_span.find("span")
            if inner_span:
                try:
                    rating = float(inner_span.get_text(strip=True))
                except ValueError:
                    pass

        # Find review count - has data attribute
        review_count = 0
        count_elem = card.select_one("span[data-business-unit-review-count]")
        if count_elem:
            count_text = count_elem.get_text(strip=True)
            match = re.search(r"([\d,]+)\s*reviews?", count_text)
            if match:
                review_count = int(match.group(1).replace(",", ""))

        img_elem = card.select_one("img")
        thumbnail_url = img_elem.get("src") if img_elem else None

        return {
            "name": name,
            "address": address,
            "rating": rating,
            "review_count": review_count,
            "url": url,
            "thumbnail_url": thumbnail_url,
        }
