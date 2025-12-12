"""Tests for reviewhound.scheduler module."""

from unittest.mock import MagicMock, patch

import pytest
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from reviewhound.scheduler import (
    _scrape_business_job,
    create_scheduler,
    scrape_all_businesses,
)


class TestCreateScheduler:
    """Tests for create_scheduler function."""

    def test_creates_blocking_scheduler(self):
        """Should create BlockingScheduler when blocking=True."""
        scheduler = create_scheduler(blocking=True)

        assert isinstance(scheduler, BlockingScheduler)

    def test_creates_background_scheduler(self):
        """Should create BackgroundScheduler when blocking=False."""
        scheduler = create_scheduler(blocking=False)

        assert isinstance(scheduler, BackgroundScheduler)

    def test_adds_scrape_job(self):
        """Should add scrape_all job to scheduler."""
        scheduler = create_scheduler(blocking=False)

        job = scheduler.get_job("scrape_all")

        assert job is not None
        assert job.name == "Scrape all businesses"


class TestScrapeAllBusinesses:
    """Tests for scrape_all_businesses function."""

    @patch("reviewhound.scheduler.get_session")
    @patch("reviewhound.scheduler._scrape_business_job")
    def test_scrapes_all_businesses_in_database(self, mock_scrape_job, mock_get_session):
        """Should call _scrape_business_job for each business."""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        mock_business1 = MagicMock(name="Business 1")
        mock_business2 = MagicMock(name="Business 2")
        mock_session.query.return_value.all.return_value = [mock_business1, mock_business2]

        scrape_all_businesses()

        assert mock_scrape_job.call_count == 2
        mock_scrape_job.assert_any_call(mock_session, mock_business1)
        mock_scrape_job.assert_any_call(mock_session, mock_business2)

    @patch("reviewhound.scheduler.get_session")
    @patch("reviewhound.scheduler._scrape_business_job")
    def test_handles_empty_database(self, mock_scrape_job, mock_get_session):
        """Should handle case with no businesses."""
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.all.return_value = []

        scrape_all_businesses()

        mock_scrape_job.assert_not_called()


class TestScrapeBusinessJob:
    """Tests for _scrape_business_job function."""

    @patch("reviewhound.scheduler.build_scrapers_for_business")
    @patch("reviewhound.scheduler.run_scraper_for_business")
    def test_scrapes_with_configured_sources(self, mock_run, mock_build):
        """Should run scrapers for all configured sources."""
        mock_session = MagicMock()
        mock_business = MagicMock()
        mock_business.name = "Test Business"

        mock_scraper = MagicMock(source="trustpilot")
        mock_build.return_value = [(mock_scraper, "https://example.com")]
        mock_run.return_value = (MagicMock(), 5)

        _scrape_business_job(mock_session, mock_business)

        mock_run.assert_called_once_with(
            mock_session, mock_business, mock_scraper, "https://example.com"
        )

    @patch("reviewhound.scheduler.build_scrapers_for_business")
    @patch("reviewhound.scheduler.run_scraper_for_business")
    def test_handles_no_sources(self, mock_run, mock_build):
        """Should handle business with no configured sources."""
        mock_session = MagicMock()
        mock_business = MagicMock()
        mock_business.name = "Empty Business"

        mock_build.return_value = []

        _scrape_business_job(mock_session, mock_business)

        mock_run.assert_not_called()

    @patch("reviewhound.scheduler.build_scrapers_for_business")
    @patch("reviewhound.scheduler.run_scraper_for_business")
    def test_continues_on_individual_failure(self, mock_run, mock_build):
        """Should continue scraping other sources when one fails."""
        mock_session = MagicMock()
        mock_business = MagicMock()
        mock_business.name = "Test Business"

        mock_scraper1 = MagicMock(source="failing_source")
        mock_scraper2 = MagicMock(source="working_source")
        mock_build.return_value = [
            (mock_scraper1, "https://fail.com"),
            (mock_scraper2, "https://work.com"),
        ]

        def run_side_effect(session, business, scraper, url):
            if scraper.source == "failing_source":
                raise Exception("Network error")
            return (MagicMock(), 3)

        mock_run.side_effect = run_side_effect

        # Should not raise exception
        _scrape_business_job(mock_session, mock_business)

        # Both scrapers should have been attempted
        assert mock_run.call_count == 2

    @patch("reviewhound.scheduler.build_scrapers_for_business")
    @patch("reviewhound.scheduler.run_scraper_for_business")
    def test_scrapes_multiple_sources(self, mock_run, mock_build):
        """Should scrape all sources for a business."""
        mock_session = MagicMock()
        mock_business = MagicMock()
        mock_business.name = "Multi Source Business"

        mock_scrapers = [
            (MagicMock(source="trustpilot"), "https://tp.com"),
            (MagicMock(source="bbb"), "https://bbb.com"),
            (MagicMock(source="yelp"), "https://yelp.com"),
        ]
        mock_build.return_value = mock_scrapers
        mock_run.return_value = (MagicMock(), 2)

        _scrape_business_job(mock_session, mock_business)

        assert mock_run.call_count == 3
