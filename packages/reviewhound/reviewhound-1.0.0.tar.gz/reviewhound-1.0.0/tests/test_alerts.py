"""Tests for reviewhound.alerts.email module."""

from unittest.mock import MagicMock, patch

import pytest

from reviewhound.alerts.email import (
    check_and_send_alerts,
    format_review_alert,
    send_alert,
)
from reviewhound.models import AlertConfig, Review


class TestFormatReviewAlert:
    """Tests for format_review_alert function."""

    def test_formats_subject_with_business_name(self):
        """Should include business name and sentiment in subject."""
        subject, _ = format_review_alert(
            business_name="Test Business",
            source="trustpilot",
            rating=2.0,
            sentiment_label="negative",
            text="Bad experience",
            author="John Doe",
        )

        assert "Test Business" in subject
        assert "negative" in subject

    def test_includes_sentiment_color_positive(self):
        """Should use green color for positive sentiment."""
        _, body = format_review_alert(
            business_name="Test",
            source="yelp",
            rating=5.0,
            sentiment_label="positive",
            text="Great!",
            author="Jane",
        )

        assert "#22c55e" in body  # Green color

    def test_includes_sentiment_color_negative(self):
        """Should use red color for negative sentiment."""
        _, body = format_review_alert(
            business_name="Test",
            source="yelp",
            rating=1.0,
            sentiment_label="negative",
            text="Terrible!",
            author="Jane",
        )

        assert "#ef4444" in body  # Red color

    def test_includes_sentiment_color_neutral(self):
        """Should use yellow color for neutral sentiment."""
        _, body = format_review_alert(
            business_name="Test",
            source="yelp",
            rating=3.0,
            sentiment_label="neutral",
            text="It was okay",
            author="Jane",
        )

        assert "#eab308" in body  # Yellow color

    def test_includes_rating_stars(self):
        """Should include star rating representation."""
        _, body = format_review_alert(
            business_name="Test",
            source="bbb",
            rating=3.0,
            sentiment_label="neutral",
            text="Average",
            author="Bob",
        )

        assert "★★★" in body
        assert "☆☆" in body

    def test_handles_anonymous_author(self):
        """Should show 'Anonymous' when author is None."""
        _, body = format_review_alert(
            business_name="Test",
            source="trustpilot",
            rating=4.0,
            sentiment_label="positive",
            text="Good",
            author=None,
        )

        assert "Anonymous" in body

    def test_handles_missing_text(self):
        """Should show placeholder when text is None."""
        _, body = format_review_alert(
            business_name="Test",
            source="trustpilot",
            rating=4.0,
            sentiment_label="positive",
            text=None,
            author="Test",
        )

        assert "No text provided" in body


class TestSendAlert:
    """Tests for send_alert function."""

    @patch("reviewhound.alerts.email.Config")
    def test_returns_false_when_smtp_not_configured(self, mock_config):
        """Should return False when SMTP credentials are missing."""
        mock_config.SMTP_USER = None
        mock_config.SMTP_PASSWORD = None

        result = send_alert("test@example.com", "Test Subject", "Test Body")

        assert result is False

    @patch("reviewhound.alerts.email.Config")
    @patch("reviewhound.alerts.email.smtplib.SMTP")
    def test_sends_email_when_configured(self, mock_smtp, mock_config):
        """Should send email when SMTP is configured."""
        mock_config.SMTP_USER = "user@example.com"
        mock_config.SMTP_PASSWORD = "password"
        mock_config.SMTP_HOST = "smtp.example.com"
        mock_config.SMTP_PORT = 587
        mock_config.SMTP_FROM = "alerts@example.com"

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        result = send_alert("recipient@example.com", "Test Subject", "<p>Test Body</p>")

        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user@example.com", "password")
        mock_server.send_message.assert_called_once()

    @patch("reviewhound.alerts.email.Config")
    @patch("reviewhound.alerts.email.smtplib.SMTP")
    def test_returns_false_on_smtp_error(self, mock_smtp, mock_config):
        """Should return False when SMTP error occurs."""
        mock_config.SMTP_USER = "user@example.com"
        mock_config.SMTP_PASSWORD = "password"
        mock_config.SMTP_HOST = "smtp.example.com"
        mock_config.SMTP_PORT = 587
        mock_config.SMTP_FROM = "alerts@example.com"

        mock_smtp.return_value.__enter__.side_effect = Exception("Connection refused")

        result = send_alert("recipient@example.com", "Test Subject", "Test Body")

        assert result is False


class TestCheckAndSendAlerts:
    """Tests for check_and_send_alerts function."""

    @patch("reviewhound.alerts.email.send_alert")
    def test_sends_alert_for_negative_rating(
        self, mock_send, db_session, sample_business, sample_alert_config
    ):
        """Should send alert when review rating is below threshold."""
        mock_send.return_value = True

        review = Review(
            business_id=sample_business.id,
            source="trustpilot",
            external_id="alert_test_001",
            rating=2.0,  # Below threshold of 3.0
            sentiment_label="negative",
        )
        db_session.add(review)
        db_session.flush()

        alerts_sent = check_and_send_alerts(db_session, sample_business, review)

        assert alerts_sent == 1
        mock_send.assert_called_once()

    @patch("reviewhound.alerts.email.send_alert")
    def test_sends_alert_for_negative_sentiment(
        self, mock_send, db_session, sample_business, sample_alert_config
    ):
        """Should send alert when sentiment is negative regardless of rating."""
        mock_send.return_value = True

        review = Review(
            business_id=sample_business.id,
            source="yelp",
            external_id="alert_test_002",
            rating=4.0,  # Good rating but negative sentiment
            sentiment_label="negative",
        )
        db_session.add(review)
        db_session.flush()

        alerts_sent = check_and_send_alerts(db_session, sample_business, review)

        assert alerts_sent == 1

    @patch("reviewhound.alerts.email.send_alert")
    def test_skips_disabled_alerts(self, mock_send, db_session, sample_business):
        """Should not send alerts when config is disabled."""
        alert = AlertConfig(
            business_id=sample_business.id,
            email="disabled@example.com",
            alert_on_negative=True,
            negative_threshold=3.0,
            enabled=False,  # Disabled
        )
        db_session.add(alert)
        db_session.flush()

        review = Review(
            business_id=sample_business.id,
            source="bbb",
            external_id="alert_test_003",
            rating=1.0,
            sentiment_label="negative",
        )
        db_session.add(review)
        db_session.flush()

        alerts_sent = check_and_send_alerts(db_session, sample_business, review)

        assert alerts_sent == 0
        mock_send.assert_not_called()

    @patch("reviewhound.alerts.email.send_alert")
    def test_respects_threshold_setting(
        self, mock_send, db_session, sample_business, sample_alert_config
    ):
        """Should only alert for ratings at or below threshold."""
        mock_send.return_value = True

        # Review at exactly threshold (3.0) should trigger
        review = Review(
            business_id=sample_business.id,
            source="trustpilot",
            external_id="alert_test_004",
            rating=3.0,  # Equal to threshold
            sentiment_label="neutral",
        )
        db_session.add(review)
        db_session.flush()

        alerts_sent = check_and_send_alerts(db_session, sample_business, review)

        assert alerts_sent == 1

    @patch("reviewhound.alerts.email.send_alert")
    def test_no_alert_for_positive_review(
        self, mock_send, db_session, sample_business, sample_alert_config
    ):
        """Should not alert for positive reviews above threshold."""
        review = Review(
            business_id=sample_business.id,
            source="yelp",
            external_id="alert_test_005",
            rating=5.0,  # Above threshold
            sentiment_label="positive",
        )
        db_session.add(review)
        db_session.flush()

        alerts_sent = check_and_send_alerts(db_session, sample_business, review)

        assert alerts_sent == 0
        mock_send.assert_not_called()

    @patch("reviewhound.alerts.email.send_alert")
    def test_returns_count_of_alerts_sent(
        self, mock_send, db_session, sample_business
    ):
        """Should return accurate count of alerts sent."""
        # Create multiple alert configs
        for i in range(3):
            alert = AlertConfig(
                business_id=sample_business.id,
                email=f"user{i}@example.com",
                alert_on_negative=True,
                negative_threshold=3.0,
                enabled=True,
            )
            db_session.add(alert)
        db_session.flush()

        mock_send.return_value = True

        review = Review(
            business_id=sample_business.id,
            source="trustpilot",
            external_id="alert_test_006",
            rating=1.0,
            sentiment_label="negative",
        )
        db_session.add(review)
        db_session.flush()

        alerts_sent = check_and_send_alerts(db_session, sample_business, review)

        assert alerts_sent == 3
        assert mock_send.call_count == 3
