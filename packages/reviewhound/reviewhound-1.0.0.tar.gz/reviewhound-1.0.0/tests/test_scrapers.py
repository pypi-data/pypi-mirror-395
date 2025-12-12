from datetime import date
from unittest.mock import patch
from pathlib import Path

import pytest
import responses

from reviewhound.scrapers.trustpilot import TrustPilotScraper
from reviewhound.scrapers.bbb import BBBScraper
from reviewhound.scrapers.yelp import YelpScraper


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


class TestTrustPilotScraper:
    @responses.activate
    def test_scrape_extracts_reviews(self):
        html = load_fixture("trustpilot_page1.html")
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com",
            body=html,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com?page=2",
            body="<html><body></body></html>",
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com?page=3",
            body="<html><body></body></html>",
            status=200,
        )

        with patch.object(TrustPilotScraper, "rate_limit"):
            scraper = TrustPilotScraper()
            reviews = scraper.scrape("https://www.trustpilot.com/review/example.com")

        assert len(reviews) == 2

        assert reviews[0]["external_id"] == "review_abc123"
        assert reviews[0]["author_name"] == "John Smith"
        assert reviews[0]["rating"] == 5.0
        assert reviews[0]["text"] == "Excellent service! Would highly recommend."
        assert reviews[0]["review_date"] == date(2024, 12, 15)

        assert reviews[1]["external_id"] == "review_def456"
        assert reviews[1]["author_name"] == "Jane Doe"
        assert reviews[1]["rating"] == 3.0

    @responses.activate
    def test_scrape_handles_http_error(self):
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com",
            status=404,
        )

        with patch.object(TrustPilotScraper, "rate_limit"):
            scraper = TrustPilotScraper()
            reviews = scraper.scrape("https://www.trustpilot.com/review/example.com")

        assert reviews == []

    @responses.activate
    def test_scrape_paginates(self):
        html = load_fixture("trustpilot_page1.html")
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com",
            body=html,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com?page=2",
            body=html,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com?page=3",
            body=html,
            status=200,
        )

        with patch.object(TrustPilotScraper, "rate_limit"):
            scraper = TrustPilotScraper()
            reviews = scraper.scrape("https://www.trustpilot.com/review/example.com")

        # 2 reviews per page * 3 pages = 6 reviews
        assert len(reviews) == 6
        # Verify all 3 pages were fetched
        assert len(responses.calls) == 3

    def test_source_is_trustpilot(self):
        scraper = TrustPilotScraper()
        assert scraper.source == "trustpilot"

    @responses.activate
    def test_scrape_json_ld_format(self):
        """Test parsing reviews from JSON-LD structured data."""
        html = load_fixture("trustpilot_jsonld.html")
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com",
            body=html,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com?page=2",
            body="<html><body></body></html>",
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.trustpilot.com/review/example.com?page=3",
            body="<html><body></body></html>",
            status=200,
        )

        with patch.object(TrustPilotScraper, "rate_limit"):
            scraper = TrustPilotScraper()
            reviews = scraper.scrape("https://www.trustpilot.com/review/example.com")

        assert len(reviews) == 2

        # First review uses standard schema.org format
        assert reviews[0]["external_id"] == "abc123def456"
        assert reviews[0]["author_name"] == "John Reviewer"
        assert reviews[0]["rating"] == 5.0
        assert reviews[0]["text"] == "Excellent product and service!"
        assert reviews[0]["review_date"] == date(2024, 12, 15)

        # Second review uses TrustPilot-specific fields
        assert reviews[1]["external_id"] == "xyz789uvw012"
        assert reviews[1]["author_name"] == "Jane Customer"
        assert reviews[1]["rating"] == 3.0
        assert "Okay experience" in reviews[1]["text"]
        assert reviews[1]["review_date"] == date(2024, 11, 20)


class TestBBBScraper:
    @responses.activate
    def test_scrape_extracts_reviews(self):
        html = load_fixture("bbb_page1.html")
        # BBB scraper normalizes URLs to /customer-reviews
        responses.add(
            responses.GET,
            "https://www.bbb.org/us/ca/los-angeles/profile/pizza/test-company-1234/customer-reviews",
            body=html,
            status=200,
        )

        with patch.object(BBBScraper, "rate_limit"):
            scraper = BBBScraper()
            reviews = scraper.scrape("https://www.bbb.org/us/ca/los-angeles/profile/pizza/test-company-1234")

        assert len(reviews) == 3

        assert reviews[0]["external_id"] == "bbb_rev_001"
        assert reviews[0]["author_name"] == "Michael Johnson"
        assert reviews[0]["rating"] == 5.0
        assert "Outstanding customer service" in reviews[0]["text"]
        assert reviews[0]["review_date"] == date(2024, 11, 20)

        assert reviews[1]["external_id"] == "bbb_rev_002"
        assert reviews[1]["author_name"] == "Sarah Williams"
        assert reviews[1]["rating"] == 2.0

        assert reviews[2]["external_id"] == "bbb_rev_003"
        assert reviews[2]["author_name"] == "Anonymous"
        assert reviews[2]["rating"] == 4.0

    @responses.activate
    def test_scrape_handles_http_error(self):
        responses.add(
            responses.GET,
            "https://www.bbb.org/us/ca/test/profile/test-1234",
            status=404,
        )

        with patch.object(BBBScraper, "rate_limit"):
            scraper = BBBScraper()
            reviews = scraper.scrape("https://www.bbb.org/us/ca/test/profile/test-1234")

        assert reviews == []

    @responses.activate
    def test_scrape_includes_complaints(self):
        html = load_fixture("bbb_page1.html")
        # BBB scraper normalizes URLs to /customer-reviews
        responses.add(
            responses.GET,
            "https://www.bbb.org/us/ca/test/profile/test-1234/customer-reviews",
            body=html,
            status=200,
        )

        with patch.object(BBBScraper, "rate_limit"):
            scraper = BBBScraper()
            reviews = scraper.scrape("https://www.bbb.org/us/ca/test/profile/test-1234", include_complaints=True)

        # 3 reviews + 1 complaint = 4 total
        assert len(reviews) == 4
        complaint = [r for r in reviews if "complaint" in r["external_id"]][0]
        assert complaint["external_id"] == "bbb_complaint_001"
        assert complaint["rating"] == 1.0  # Complaints default to 1-star

    def test_source_is_bbb(self):
        scraper = BBBScraper()
        assert scraper.source == "bbb"


class TestYelpScraper:
    @responses.activate
    def test_scrape_extracts_reviews(self):
        html = load_fixture("yelp_page1.html")
        responses.add(
            responses.GET,
            "https://www.yelp.com/biz/test-restaurant",
            body=html,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.yelp.com/biz/test-restaurant?start=10",
            body="<html><body></body></html>",
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.yelp.com/biz/test-restaurant?start=20",
            body="<html><body></body></html>",
            status=200,
        )

        with patch.object(YelpScraper, "rate_limit"):
            scraper = YelpScraper()
            reviews = scraper.scrape("https://www.yelp.com/biz/test-restaurant")

        assert len(reviews) == 3

        assert reviews[0]["external_id"] == "yelp_12345abc"
        assert reviews[0]["author_name"] == "Alex Thompson"
        assert reviews[0]["rating"] == 5.0
        assert "Amazing food and excellent service" in reviews[0]["text"]
        assert reviews[0]["review_date"] == date(2024, 11, 15)

        assert reviews[1]["external_id"] == "yelp_67890def"
        assert reviews[1]["author_name"] == "Maria Garcia"
        assert reviews[1]["rating"] == 3.0
        assert "Food was decent" in reviews[1]["text"]
        assert reviews[1]["review_date"] == date(2024, 10, 22)

        assert reviews[2]["external_id"] == "yelp_11223ghi"
        assert reviews[2]["author_name"] == "Robert Chen"
        assert reviews[2]["rating"] == 1.0

    @responses.activate
    def test_scrape_handles_http_error(self):
        responses.add(
            responses.GET,
            "https://www.yelp.com/biz/test-restaurant",
            status=404,
        )

        with patch.object(YelpScraper, "rate_limit"):
            scraper = YelpScraper()
            reviews = scraper.scrape("https://www.yelp.com/biz/test-restaurant")

        assert reviews == []

    @responses.activate
    def test_scrape_paginates(self):
        html = load_fixture("yelp_page1.html")
        responses.add(
            responses.GET,
            "https://www.yelp.com/biz/test-restaurant",
            body=html,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.yelp.com/biz/test-restaurant?start=10",
            body=html,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://www.yelp.com/biz/test-restaurant?start=20",
            body=html,
            status=200,
        )

        with patch.object(YelpScraper, "rate_limit"):
            scraper = YelpScraper()
            reviews = scraper.scrape("https://www.yelp.com/biz/test-restaurant")

        # 3 reviews per page * 3 pages = 9 reviews
        assert len(reviews) == 9
        # Verify all 3 pages were fetched
        assert len(responses.calls) == 3

    def test_source_is_yelp(self):
        scraper = YelpScraper()
        assert scraper.source == "yelp"
