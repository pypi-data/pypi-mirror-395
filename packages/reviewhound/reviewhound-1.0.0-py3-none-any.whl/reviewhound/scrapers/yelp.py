import re
from datetime import datetime, date
from urllib.parse import quote_plus

import requests

from reviewhound.scrapers.base import BaseScraper
from reviewhound.config import Config


class YelpScraper(BaseScraper):
    source = "yelp"

    def scrape(self, url: str) -> list[dict]:
        reviews = []
        base_url = url.split("?")[0]
        self._current_base_url = base_url  # Store for URL construction

        for page in range(Config.MAX_PAGES_PER_SOURCE):
            page_url = base_url if page == 0 else f"{base_url}?start={page * 10}"

            try:
                soup = self.fetch(page_url)
                page_reviews = self._parse_reviews(soup)
                reviews.extend(page_reviews)
            except requests.RequestException:
                break

        return reviews

    def _parse_reviews(self, soup) -> list[dict]:
        reviews = []
        review_items = soup.find_all("li", attrs={"data-review-id": True})

        for item in review_items:
            try:
                review = self._parse_review(item)
                if review:
                    reviews.append(review)
            except (AttributeError, ValueError):
                continue

        return reviews

    def _parse_review(self, item) -> dict | None:
        review_id = item.get("data-review-id")
        if not review_id:
            return None

        author_elem = item.select_one(".user-passport-info span.fs-block")
        author_name = author_elem.get_text(strip=True) if author_elem else "Anonymous"

        rating_elem = item.find(attrs={"aria-label": re.compile(r"\d+ star rating")})
        rating = None
        if rating_elem:
            aria_label = rating_elem.get("aria-label", "")
            match = re.search(r"(\d+) star rating", aria_label)
            if match:
                rating = float(match.group(1))

        text_elem = item.select_one("span.raw__09f24__T4Ezm")
        text = text_elem.get_text(strip=True) if text_elem else ""

        date_elem = item.select_one("span.css-chan6m")
        review_date = None
        if date_elem:
            date_text = date_elem.get_text(strip=True)
            review_date = self._parse_date(date_text)

        # Yelp review URL with hrid parameter to highlight specific review
        base_url = getattr(self, '_current_base_url', None)
        review_url = f"{base_url}?hrid={review_id}" if base_url and review_id else None

        return {
            "external_id": review_id,
            "review_url": review_url,
            "author_name": author_name,
            "rating": rating,
            "text": text,
            "review_date": review_date,
        }

    def _parse_date(self, text: str) -> date | None:
        try:
            return datetime.strptime(text, "%b %d, %Y").date()
        except ValueError:
            return None

    def search(self, query: str, location: str | None = None) -> list[dict]:
        """Search Yelp for businesses matching the query."""
        search_url = f"https://www.yelp.com/search?find_desc={quote_plus(query)}"
        if location:
            search_url += f"&find_loc={quote_plus(location)}"

        try:
            soup = self.fetch(search_url)
        except requests.RequestException:
            return []

        results = []
        # Yelp search results are in divs with data-testid containing "serp-ia-card"
        cards = soup.select("div[data-testid*='serp-ia-card'], div.container__09f24__FeTO6")[:5]

        for card in cards:
            try:
                result = self._parse_search_result(card)
                if result:
                    results.append(result)
            except (AttributeError, ValueError):
                continue

        return results

    def _parse_search_result(self, card) -> dict | None:
        # Find the business link
        link = card.select_one("a[href*='/biz/']")
        if not link:
            return None

        href = link.get("href", "")
        url = f"https://www.yelp.com{href}" if href.startswith("/") else href

        # Remove query params from URL for cleaner links
        url = url.split("?")[0]

        name = link.get_text(strip=True)

        # Address
        address_elem = card.select_one("span.raw__09f24__T4Ezm, p.css-1e4fdj9")
        address = address_elem.get_text(strip=True) if address_elem else ""

        # Rating
        rating = None
        rating_elem = card.find(attrs={"aria-label": re.compile(r"[\d.]+ star rating")})
        if rating_elem:
            aria_label = rating_elem.get("aria-label", "")
            match = re.search(r"([\d.]+) star rating", aria_label)
            if match:
                rating = float(match.group(1))

        # Review count
        review_count = 0
        count_elem = card.select_one("span.css-chan6m")
        if count_elem:
            count_text = count_elem.get_text(strip=True)
            match = re.search(r"(\d+)", count_text)
            if match:
                review_count = int(match.group(1))

        # Thumbnail
        img_elem = card.select_one("img.css-xlzvdl, img[src*='bphoto']")
        thumbnail_url = img_elem.get("src") if img_elem else None

        return {
            "name": name,
            "address": address,
            "rating": rating,
            "review_count": review_count,
            "url": url,
            "thumbnail_url": thumbnail_url,
        }
