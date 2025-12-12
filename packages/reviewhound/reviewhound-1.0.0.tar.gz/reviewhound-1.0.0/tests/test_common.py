"""Tests for reviewhound.common module."""

from unittest.mock import MagicMock, patch

import pytest

from reviewhound.common import (
    build_scrapers_for_business,
    get_api_config,
    scrape_business_sources,
)
from reviewhound.models import APIConfig, Business


class TestGetApiConfig:
    """Tests for get_api_config function."""

    def test_returns_none_when_no_config(self, db_session):
        """Should return None when no API config exists for provider."""
        result = get_api_config(db_session, "google_places")
        assert result is None

    def test_returns_none_when_disabled(self, db_session):
        """Should return None when API config exists but is disabled."""
        config = APIConfig(provider="google_places", api_key="test-key", enabled=False)
        db_session.add(config)
        db_session.flush()

        result = get_api_config(db_session, "google_places")
        assert result is None

    def test_returns_config_when_enabled(self, db_session, sample_api_configs):
        """Should return config when it exists and is enabled."""
        result = get_api_config(db_session, "google_places")

        assert result is not None
        assert result.provider == "google_places"
        assert result.enabled is True


class TestBuildScrapersForBusiness:
    """Tests for build_scrapers_for_business function."""

    def test_returns_empty_for_no_sources(self, db_session):
        """Should return empty list when business has no URLs configured."""
        business = Business(name="Empty Business")
        db_session.add(business)
        db_session.flush()

        scrapers = build_scrapers_for_business(db_session, business)
        assert scrapers == []

    @patch("reviewhound.common.TrustPilotScraper")
    def test_includes_trustpilot_scraper(self, mock_tp, db_session):
        """Should include TrustPilot scraper when URL is configured."""
        mock_tp.return_value = MagicMock(source="trustpilot")
        business = Business(
            name="TP Business",
            trustpilot_url="https://trustpilot.com/review/test.com",
        )
        db_session.add(business)
        db_session.flush()

        scrapers = build_scrapers_for_business(db_session, business)

        assert len(scrapers) == 1
        scraper, url = scrapers[0]
        assert url == "https://trustpilot.com/review/test.com"
        mock_tp.assert_called_once()

    @patch("reviewhound.common.BBBScraper")
    def test_includes_bbb_scraper(self, mock_bbb, db_session):
        """Should include BBB scraper when URL is configured."""
        mock_bbb.return_value = MagicMock(source="bbb")
        business = Business(
            name="BBB Business",
            bbb_url="https://bbb.org/test",
        )
        db_session.add(business)
        db_session.flush()

        scrapers = build_scrapers_for_business(db_session, business)

        assert len(scrapers) == 1
        scraper, url = scrapers[0]
        assert url == "https://bbb.org/test"
        mock_bbb.assert_called_once()

    @patch("reviewhound.common.YelpScraper")
    def test_includes_yelp_scraper_when_no_api(self, mock_yelp, db_session):
        """Should use Yelp web scraper when no API key configured."""
        mock_yelp.return_value = MagicMock(source="yelp")
        business = Business(
            name="Yelp Business",
            yelp_url="https://yelp.com/biz/test",
        )
        db_session.add(business)
        db_session.flush()

        scrapers = build_scrapers_for_business(db_session, business)

        assert len(scrapers) == 1
        scraper, url = scrapers[0]
        assert url == "https://yelp.com/biz/test"
        mock_yelp.assert_called_once()

    @patch("reviewhound.common.YelpAPIScraper")
    def test_prefers_yelp_api_over_scraper(self, mock_yelp_api, db_session, sample_api_configs):
        """Should prefer Yelp API when API key is configured."""
        mock_yelp_api.return_value = MagicMock(source="yelp")
        business = Business(
            name="Yelp API Business",
            yelp_url="https://yelp.com/biz/test",
            yelp_business_id="test-business-id",
        )
        db_session.add(business)
        db_session.flush()

        scrapers = build_scrapers_for_business(db_session, business)

        # Should use API scraper, not web scraper
        yelp_scrapers = [s for s, _ in scrapers if s.source == "yelp"]
        assert len(yelp_scrapers) == 1
        mock_yelp_api.assert_called_once_with("test-yelp-api-key-67890")

    @patch("reviewhound.common.GooglePlacesScraper")
    def test_includes_google_places_with_api(self, mock_google, db_session, sample_api_configs):
        """Should include Google Places when API key and place_id configured."""
        mock_google.return_value = MagicMock(source="google_places")
        business = Business(
            name="Google Business",
            google_place_id="ChIJtest123",
        )
        db_session.add(business)
        db_session.flush()

        scrapers = build_scrapers_for_business(db_session, business)

        assert len(scrapers) == 1
        mock_google.assert_called_once_with("test-google-api-key-12345")

    @patch("reviewhound.common.TrustPilotScraper")
    @patch("reviewhound.common.BBBScraper")
    @patch("reviewhound.common.YelpScraper")
    def test_builds_multiple_scrapers(self, mock_yelp, mock_bbb, mock_tp, db_session, sample_business):
        """Should build scrapers for all configured sources."""
        mock_tp.return_value = MagicMock(source="trustpilot")
        mock_bbb.return_value = MagicMock(source="bbb")
        mock_yelp.return_value = MagicMock(source="yelp")

        # sample_business has trustpilot, bbb, and yelp URLs
        # but also has yelp_business_id, so we need to clear API configs
        scrapers = build_scrapers_for_business(db_session, sample_business)

        # Should have trustpilot, bbb (no Yelp API configured, but has yelp_business_id)
        # Actually since sample_business has yelp_business_id but no API config,
        # it falls back to web scraping via yelp_url
        sources = [s.source for s, _ in scrapers]
        assert "trustpilot" in sources
        assert "bbb" in sources


class TestScrapeBusinessSources:
    """Tests for scrape_business_sources function."""

    @patch("reviewhound.common.build_scrapers_for_business")
    @patch("reviewhound.common.run_scraper_for_business")
    def test_returns_total_and_failures(self, mock_run, mock_build, db_session, sample_business):
        """Should return total new reviews and failed sources list."""
        mock_scraper = MagicMock(source="trustpilot")
        mock_build.return_value = [(mock_scraper, "https://example.com")]
        mock_run.return_value = (MagicMock(), 5)

        total, failures = scrape_business_sources(db_session, sample_business)

        assert total == 5
        assert failures == []

    @patch("reviewhound.common.build_scrapers_for_business")
    @patch("reviewhound.common.run_scraper_for_business")
    def test_catches_scraper_exceptions(self, mock_run, mock_build, db_session, sample_business):
        """Should catch exceptions and add source to failures."""
        mock_scraper = MagicMock(source="failing_source")
        mock_build.return_value = [(mock_scraper, "https://example.com")]
        mock_run.side_effect = Exception("Scrape failed")

        total, failures = scrape_business_sources(db_session, sample_business)

        assert total == 0
        assert "failing_source" in failures

    @patch("reviewhound.common.build_scrapers_for_business")
    @patch("reviewhound.common.run_scraper_for_business")
    def test_continues_after_single_failure(self, mock_run, mock_build, db_session, sample_business):
        """Should continue scraping other sources after one fails."""
        scraper1 = MagicMock(source="failing_source")
        scraper2 = MagicMock(source="working_source")
        mock_build.return_value = [
            (scraper1, "https://fail.com"),
            (scraper2, "https://work.com"),
        ]

        def run_side_effect(session, business, scraper, url, send_alerts=True):
            if scraper.source == "failing_source":
                raise Exception("Network error")
            return (MagicMock(), 3)

        mock_run.side_effect = run_side_effect

        total, failures = scrape_business_sources(db_session, sample_business)

        assert total == 3
        assert "failing_source" in failures
        assert "working_source" not in failures

    @patch("reviewhound.common.build_scrapers_for_business")
    def test_handles_empty_scraper_list(self, mock_build, db_session, sample_business):
        """Should handle business with no configured scrapers."""
        mock_build.return_value = []

        total, failures = scrape_business_sources(db_session, sample_business)

        assert total == 0
        assert failures == []
