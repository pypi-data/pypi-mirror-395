"""Tests for reviewhound.services module."""

from datetime import date, datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest

from reviewhound.models import Business, Review, ScrapeLog, SentimentConfig
from reviewhound.services import (
    calculate_review_stats,
    get_sentiment_weights,
    run_scraper_for_business,
    save_scraped_reviews,
)


class TestGetSentimentWeights:
    """Tests for get_sentiment_weights function."""

    def test_returns_defaults_when_no_config(self, db_session):
        """Should return default weights when no SentimentConfig exists."""
        rating_weight, text_weight, threshold = get_sentiment_weights(db_session)

        assert rating_weight == 0.7
        assert text_weight == 0.3
        assert threshold == 0.1

    def test_returns_custom_weights_from_database(self, db_session, sample_sentiment_config):
        """Should return custom weights when SentimentConfig exists."""
        rating_weight, text_weight, threshold = get_sentiment_weights(db_session)

        assert rating_weight == 0.6
        assert text_weight == 0.4
        assert threshold == 0.15


class TestCalculateReviewStats:
    """Tests for calculate_review_stats function."""

    def test_empty_reviews_returns_zeros(self):
        """Should return zero values for empty review list."""
        stats = calculate_review_stats([])

        assert stats["total"] == 0
        assert stats["avg_rating"] == 0.0
        assert stats["positive"] == 0
        assert stats["negative"] == 0
        assert stats["neutral"] == 0
        assert stats["by_source"] == {}
        assert stats["trend_direction"] is None
        assert stats["recent_count"] == 0

    def test_calculates_average_rating(self, db_session, sample_business, sample_reviews):
        """Should calculate correct average rating."""
        stats = calculate_review_stats(sample_reviews)

        # (5.0 + 1.0 + 3.0) / 3 = 3.0
        assert stats["avg_rating"] == 3.0

    def test_calculates_sentiment_counts(self, db_session, sample_business, sample_reviews):
        """Should count reviews by sentiment label."""
        stats = calculate_review_stats(sample_reviews)

        assert stats["total"] == 3
        assert stats["positive"] == 1
        assert stats["negative"] == 1
        assert stats["neutral"] == 1

    def test_calculates_sentiment_percentages(self, db_session, sample_business, sample_reviews):
        """Should calculate correct sentiment percentages."""
        stats = calculate_review_stats(sample_reviews)

        assert abs(stats["positive_pct"] - 33.33) < 0.1
        assert abs(stats["negative_pct"] - 33.33) < 0.1
        assert abs(stats["neutral_pct"] - 33.33) < 0.1

    def test_groups_by_source(self, db_session, sample_business, sample_reviews):
        """Should group review counts by source."""
        stats = calculate_review_stats(sample_reviews)

        assert stats["by_source"]["trustpilot"] == 1
        assert stats["by_source"]["bbb"] == 1
        assert stats["by_source"]["yelp"] == 1

    def test_calculates_recent_count(self, db_session, sample_business, sample_reviews):
        """Should count reviews from last 7 days."""
        stats = calculate_review_stats(sample_reviews)

        # All sample reviews are from today
        assert stats["recent_count"] == 3

    def test_calculates_recent_negative_count(self, db_session, sample_business, sample_reviews):
        """Should count negative reviews from last 7 days."""
        stats = calculate_review_stats(sample_reviews)

        assert stats["recent_negative_count"] == 1

    def test_handles_reviews_without_rating(self, db_session, sample_business):
        """Should handle reviews with no rating."""
        review = Review(
            business_id=sample_business.id,
            source="trustpilot",
            external_id="no_rating_001",
            text="No rating provided",
            review_date=date.today(),
            sentiment_label="neutral",
        )
        db_session.add(review)
        db_session.flush()

        stats = calculate_review_stats([review])

        assert stats["total"] == 1
        assert stats["avg_rating"] == 0.0  # No rated reviews

    def test_trend_direction_up(self, db_session, sample_business):
        """Should detect upward trend when recent ratings are higher."""
        now = datetime.now(timezone.utc)
        reviews = []

        # Old reviews (31-60 days ago) with low ratings
        for i in range(3):
            r = Review(
                business_id=sample_business.id,
                source="trustpilot",
                external_id=f"old_{i}",
                rating=2.0,
                review_date=(now - timedelta(days=45)).date(),
                sentiment_label="negative",
            )
            reviews.append(r)

        # Recent reviews (last 30 days) with high ratings
        for i in range(3):
            r = Review(
                business_id=sample_business.id,
                source="trustpilot",
                external_id=f"new_{i}",
                rating=5.0,
                review_date=(now - timedelta(days=15)).date(),
                sentiment_label="positive",
            )
            reviews.append(r)

        db_session.add_all(reviews)
        db_session.flush()

        stats = calculate_review_stats(reviews)

        assert stats["trend_direction"] == "up"
        assert stats["trend_delta"] == 3.0  # 5.0 - 2.0

    def test_trend_direction_down(self, db_session, sample_business):
        """Should detect downward trend when recent ratings are lower."""
        now = datetime.now(timezone.utc)
        reviews = []

        # Old reviews with high ratings
        for i in range(3):
            r = Review(
                business_id=sample_business.id,
                source="trustpilot",
                external_id=f"old_{i}",
                rating=5.0,
                review_date=(now - timedelta(days=45)).date(),
                sentiment_label="positive",
            )
            reviews.append(r)

        # Recent reviews with low ratings
        for i in range(3):
            r = Review(
                business_id=sample_business.id,
                source="trustpilot",
                external_id=f"new_{i}",
                rating=2.0,
                review_date=(now - timedelta(days=15)).date(),
                sentiment_label="negative",
            )
            reviews.append(r)

        db_session.add_all(reviews)
        db_session.flush()

        stats = calculate_review_stats(reviews)

        assert stats["trend_direction"] == "down"
        assert stats["trend_delta"] == -3.0


class TestSaveScrapedReviews:
    """Tests for save_scraped_reviews function."""

    @patch("reviewhound.services.analyze_review")
    @patch("reviewhound.services.check_and_send_alerts")
    def test_saves_new_reviews(self, mock_alerts, mock_analyze, db_session, sample_business):
        """Should save new reviews to database."""
        mock_analyze.return_value = (0.8, "positive")

        reviews_data = [
            {
                "external_id": "new_001",
                "author_name": "New Reviewer",
                "rating": 4.5,
                "text": "Great product!",
                "review_date": date.today(),
            }
        ]

        log, new_count = save_scraped_reviews(
            db_session, sample_business, "trustpilot", reviews_data, send_alerts=False
        )

        assert new_count == 1
        assert log.status == "success"
        assert log.reviews_found == 1

        # Verify review was saved
        saved = db_session.query(Review).filter_by(external_id="new_001").first()
        assert saved is not None
        assert saved.author_name == "New Reviewer"
        assert saved.sentiment_label == "positive"

    @patch("reviewhound.services.analyze_review")
    @patch("reviewhound.services.check_and_send_alerts")
    def test_skips_duplicate_reviews(self, mock_alerts, mock_analyze, db_session, sample_business, sample_reviews):
        """Should skip reviews that already exist."""
        mock_analyze.return_value = (0.8, "positive")

        # Try to add a review with existing external_id
        reviews_data = [
            {
                "external_id": "tp_001",  # Already exists in sample_reviews
                "author_name": "Duplicate",
                "rating": 5.0,
                "text": "Duplicate review",
                "review_date": date.today(),
            }
        ]

        log, new_count = save_scraped_reviews(
            db_session, sample_business, "trustpilot", reviews_data, send_alerts=False
        )

        assert new_count == 0

    @patch("reviewhound.services.analyze_review")
    @patch("reviewhound.services.check_and_send_alerts")
    def test_sends_alerts_when_enabled(self, mock_alerts, mock_analyze, db_session, sample_business):
        """Should call alert check when send_alerts is True."""
        mock_analyze.return_value = (-0.5, "negative")

        reviews_data = [
            {
                "external_id": "alert_001",
                "author_name": "Angry Customer",
                "rating": 1.0,
                "text": "Terrible!",
                "review_date": date.today(),
            }
        ]

        save_scraped_reviews(
            db_session, sample_business, "trustpilot", reviews_data, send_alerts=True
        )

        mock_alerts.assert_called_once()

    @patch("reviewhound.services.analyze_review")
    @patch("reviewhound.services.check_and_send_alerts")
    def test_creates_scrape_log(self, mock_alerts, mock_analyze, db_session, sample_business):
        """Should create ScrapeLog entry."""
        mock_analyze.return_value = (0.5, "positive")

        reviews_data = [{"external_id": "log_001", "rating": 4.0}]

        log, _ = save_scraped_reviews(
            db_session, sample_business, "bbb", reviews_data, send_alerts=False
        )

        assert log.business_id == sample_business.id
        assert log.source == "bbb"
        assert log.status == "success"
        assert log.started_at is not None
        assert log.completed_at is not None


class TestRunScraperForBusiness:
    """Tests for run_scraper_for_business function."""

    @patch("reviewhound.services.analyze_review")
    @patch("reviewhound.services.check_and_send_alerts")
    def test_successful_scrape(self, mock_alerts, mock_analyze, db_session, sample_business, mock_scraper):
        """Should run scraper and save results."""
        mock_analyze.return_value = (0.7, "positive")

        log, new_count = run_scraper_for_business(
            db_session, sample_business, mock_scraper, "https://example.com", send_alerts=False
        )

        mock_scraper.scrape.assert_called_once_with("https://example.com")
        assert log.status == "success"
        assert new_count == 1

    @patch("reviewhound.services.analyze_review")
    def test_failed_scrape_sets_error(self, mock_analyze, db_session, sample_business):
        """Should set error message on scrape failure."""
        scraper = MagicMock()
        scraper.source = "failing_source"
        scraper.scrape.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Network error"):
            run_scraper_for_business(
                db_session, sample_business, scraper, "https://example.com"
            )

        # Check that a failed log was created
        log = db_session.query(ScrapeLog).filter_by(
            business_id=sample_business.id,
            source="failing_source"
        ).first()
        assert log is not None
        assert log.status == "failed"
        assert "Network error" in log.error_message
