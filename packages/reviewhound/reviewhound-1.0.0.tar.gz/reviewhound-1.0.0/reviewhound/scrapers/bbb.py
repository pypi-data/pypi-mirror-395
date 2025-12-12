import json
import logging
import re
from datetime import datetime, date
from urllib.parse import quote_plus

import requests

from reviewhound.scrapers.base import BaseScraper
from reviewhound.config import Config

logger = logging.getLogger(__name__)


class BBBScraper(BaseScraper):
    source = "bbb"

    def scrape(self, url: str, include_complaints: bool = False) -> list[dict]:
        reviews = []

        # Normalize the URL to get the reviews page
        reviews_url = self._normalize_url(url)
        self._current_reviews_url = reviews_url  # Store for URL construction

        try:
            soup = self.fetch(reviews_url)
            reviews.extend(self._parse_reviews(soup))

            if include_complaints:
                reviews.extend(self._parse_complaints(soup))

        except requests.RequestException as e:
            logger.warning(f"BBB scrape failed for {reviews_url}: {e}")

        return reviews

    def _normalize_url(self, url: str) -> str:
        """Normalize BBB URL to point to the customer reviews page."""
        # Remove query parameters
        url = url.split("?")[0].rstrip("/")

        # Remove /addressId/... suffix if present
        url = re.sub(r"/addressId/\d+$", "", url)

        # Remove /customer-reviews if present (we'll add it back)
        url = re.sub(r"/customer-reviews$", "", url)

        # Add /customer-reviews to get the reviews page
        return url + "/customer-reviews"

    def _parse_reviews(self, soup) -> list[dict]:
        # Try JSON-LD first (modern format)
        reviews = self._parse_json_ld_reviews(soup)
        if reviews:
            return reviews

        # Try current BBB HTML structure (li.card.bpr-review)
        reviews = self._parse_bpr_reviews(soup)
        if reviews:
            return reviews

        # Fall back to legacy HTML parsing
        reviews = []
        review_items = soup.find_all("div", class_="review-item")

        if not review_items:
            logger.debug("BBB: No review elements found, page may use different structure")

        for item in review_items:
            try:
                review = self._parse_review(item)
                if review:
                    reviews.append(review)
            except (AttributeError, ValueError):
                continue

        return reviews

    def _parse_bpr_reviews(self, soup) -> list[dict]:
        """Parse reviews from current BBB HTML structure."""
        reviews = []

        # Find li elements with both 'card' and 'bpr-review' classes
        for elem in soup.find_all("li"):
            classes = elem.get("class", [])
            if "card" in classes and "bpr-review" in classes:
                try:
                    review = self._parse_bpr_review(elem)
                    if review:
                        reviews.append(review)
                except (AttributeError, ValueError):
                    continue

        return reviews

    def _parse_bpr_review(self, item) -> dict | None:
        """Parse a single review from BBB's bpr-review card."""
        # ID from element id attribute (e.g., "1296_7039385_834877")
        review_id = item.get("id")
        if not review_id:
            return None

        # Author name from h3.bpr-review-title span
        author_name = "Anonymous"
        title_elem = item.find("h3", class_="bpr-review-title")
        if title_elem:
            # The author name is in the last span (after visually-hidden "Review from")
            spans = title_elem.find_all("span")
            for span in spans:
                classes = span.get("class", [])
                if "visually-hidden" not in classes:
                    name = span.get_text(strip=True)
                    if name:
                        # Remove any "Review from" prefix if present
                        name = name.replace("Review from", "").strip()
                        if name:
                            author_name = name
                        break

        # Date from p containing "Date:"
        review_date = None
        for p in item.find_all("p"):
            text = p.get_text(strip=True)
            if text.startswith("Date:"):
                date_str = text.replace("Date:", "").strip()
                review_date = self._parse_date(date_str)
                break

        # Rating from filled stars (data-filled attribute)
        rating = None
        star_container = item.find("div", class_="star-rating")
        if star_container:
            filled_stars = star_container.find_all("svg", attrs={"data-filled": True})
            rating = float(len(filled_stars)) if filled_stars else None

        # Review text - in a classless div element
        text = ""
        for div in item.find_all("div"):
            # Look for divs without a class attribute (or empty class)
            if not div.get("class"):
                div_text = div.get_text(strip=True)
                if div_text and len(div_text) > 10:  # Skip tiny fragments
                    text = div_text
                    break

        # BBB reviews page with anchor to specific review
        review_url = getattr(self, '_current_reviews_url', None)
        if review_url and review_id:
            review_url = f"{review_url}#{review_id}"

        return {
            "external_id": review_id,
            "review_url": review_url,
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

            items = data if isinstance(data, list) else [data]

            for item in items:
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
        review_id = data.get("id") or data.get("@id")
        if not review_id:
            # Generate ID from content hash if not provided
            text = data.get("reviewBody") or data.get("text") or ""
            if text:
                review_id = f"bbb_{hash(text) & 0xFFFFFFFF:08x}"
            else:
                return None

        author_name = "Anonymous"
        author = data.get("author")
        if isinstance(author, dict):
            author_name = author.get("name") or "Anonymous"
        elif isinstance(author, str):
            author_name = author

        rating = None
        rating_value = data.get("reviewRating")
        if isinstance(rating_value, dict):
            rating = float(rating_value.get("ratingValue", 0))
        elif rating_value is not None:
            rating = float(rating_value)

        text = data.get("reviewBody") or data.get("text") or ""

        review_date = None
        date_str = data.get("datePublished")
        if date_str:
            review_date = self._parse_iso_date(date_str)

        # BBB reviews page with anchor to specific review
        review_url = getattr(self, '_current_reviews_url', None)
        if review_url and review_id:
            review_url = f"{review_url}#{review_id}"

        return {
            "external_id": str(review_id),
            "review_url": review_url,
            "author_name": author_name,
            "rating": rating,
            "text": text,
            "review_date": review_date,
        }

    def _parse_iso_date(self, date_str: str) -> date | None:
        """Parse ISO 8601 date string."""
        try:
            if "T" in date_str:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    def _parse_review(self, item) -> dict | None:
        review_id = item.get("data-review-id")
        if not review_id:
            return None

        # Author name
        author_elem = item.find("span", class_="reviewer-name")
        author_name = author_elem.get_text(strip=True) if author_elem else "Anonymous"

        # Rating from data attribute
        rating_elem = item.find("div", class_="star-rating")
        rating = None
        if rating_elem and rating_elem.get("data-rating"):
            rating = float(rating_elem.get("data-rating"))

        # Review text
        text_elem = item.find("div", class_="review-text")
        text = ""
        if text_elem:
            p = text_elem.find("p")
            text = p.get_text(strip=True) if p else text_elem.get_text(strip=True)

        # Date
        date_elem = item.find("span", class_="review-date")
        review_date = None
        if date_elem:
            review_date = self._parse_date(date_elem.get_text(strip=True))

        # BBB reviews page with anchor to specific review
        review_url = getattr(self, '_current_reviews_url', None)
        if review_url and review_id:
            review_url = f"{review_url}#{review_id}"

        return {
            "external_id": review_id,
            "review_url": review_url,
            "author_name": author_name,
            "rating": rating,
            "text": text,
            "review_date": review_date,
        }

    def _parse_complaints(self, soup) -> list[dict]:
        complaints = []
        complaint_items = soup.find_all("div", class_="complaint-item")

        for item in complaint_items:
            try:
                complaint = self._parse_complaint(item)
                if complaint:
                    complaints.append(complaint)
            except (AttributeError, ValueError):
                continue

        return complaints

    def _parse_complaint(self, item) -> dict | None:
        complaint_id = item.get("data-complaint-id")
        if not complaint_id:
            return None

        # Complaint type as "author"
        type_elem = item.find("span", class_="complaint-type")
        complaint_type = type_elem.get_text(strip=True) if type_elem else "Complaint"

        # Complaint text
        text_elem = item.find("div", class_="complaint-text")
        text = ""
        if text_elem:
            p = text_elem.find("p")
            text = p.get_text(strip=True) if p else text_elem.get_text(strip=True)

        # Date
        date_elem = item.find("span", class_="complaint-date")
        complaint_date = None
        if date_elem:
            complaint_date = self._parse_date(date_elem.get_text(strip=True))

        # BBB reviews page with anchor to specific complaint
        review_url = getattr(self, '_current_reviews_url', None)
        if review_url and complaint_id:
            review_url = f"{review_url}#{complaint_id}"

        return {
            "external_id": complaint_id,
            "review_url": review_url,
            "author_name": complaint_type,
            "rating": Config.COMPLAINT_DEFAULT_RATING,
            "text": text,
            "review_date": complaint_date,
        }

    def _parse_date(self, text: str) -> date | None:
        # BBB uses MM/DD/YYYY format
        try:
            return datetime.strptime(text.strip(), "%m/%d/%Y").date()
        except ValueError:
            pass
        return None

    def search(self, query: str, location: str | None = None) -> list[dict]:
        """Search BBB for businesses matching the query."""
        search_url = f"https://www.bbb.org/search?find_text={quote_plus(query)}"
        if location:
            search_url += f"&find_loc={quote_plus(location)}"

        try:
            soup = self.fetch(search_url)
        except requests.RequestException as e:
            logger.warning(f"BBB search failed for '{query}': {e}")
            return []

        results = []
        cards = soup.select("div.result-card")[:5]

        for card in cards:
            try:
                result = self._parse_search_result(card)
                if result:
                    results.append(result)
            except (AttributeError, ValueError):
                continue

        return results

    def _parse_search_result(self, card) -> dict | None:
        # Get URL from the business name link
        name_heading = card.select_one("h3.result-business-name")
        if not name_heading:
            return None

        link = name_heading.find("a")
        if not link:
            return None

        url = link.get("href", "")
        if not url:
            return None

        if url.startswith("/"):
            url = f"https://www.bbb.org{url}"

        name = link.get_text(strip=True)

        # Address is in p.text-size-5 (contains street address)
        address = ""
        address_elem = card.select_one("p.text-size-5")
        if address_elem:
            address = address_elem.get_text(strip=True)

        # BBB rating is in summary.result-rating
        rating = None
        rating_elem = card.select_one("summary.result-rating")
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            match = re.search(r"BBB Rating:\s*([A-F][+-]?)", rating_text, re.IGNORECASE)
            if match:
                grade = match.group(1).upper()
                grade_map = {"A+": 5.0, "A": 4.7, "A-": 4.3, "B+": 4.0, "B": 3.7, "B-": 3.3,
                             "C+": 3.0, "C": 2.7, "C-": 2.3, "D+": 2.0, "D": 1.7, "D-": 1.3, "F": 1.0}
                rating = grade_map.get(grade)

        # BBB doesn't show review count in search results
        review_count = 0

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
