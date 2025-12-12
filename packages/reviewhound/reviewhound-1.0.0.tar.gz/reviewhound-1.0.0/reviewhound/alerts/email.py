import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from reviewhound.config import Config

logger = logging.getLogger(__name__)


def send_alert(to_email: str, subject: str, body: str) -> bool:
    """Send an email alert.

    Returns True if sent successfully, False otherwise.
    """
    if not Config.SMTP_USER or not Config.SMTP_PASSWORD:
        logger.debug("SMTP not configured, skipping alert")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = Config.SMTP_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)

        return True
    except Exception as e:
        logger.error(f"Failed to send alert to {to_email}: {e}")
        return False


def format_review_alert(business_name: str, source: str, rating: float,
                        sentiment_label: str, text: str, author: str) -> tuple[str, str]:
    """Format a review alert email.

    Returns (subject, body) tuple.
    """
    subject = f"🚨 New {sentiment_label} review for {business_name}"

    sentiment_color = {
        'positive': '#22c55e',
        'negative': '#ef4444',
        'neutral': '#eab308'
    }.get(sentiment_label, '#6b7280')

    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #4f46e5; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">🐕 Review Hound Alert</h1>
        </div>

        <div style="padding: 20px; background: #f9fafb;">
            <h2 style="color: #1f2937;">New Review for {business_name}</h2>

            <div style="background: white; border-radius: 8px; padding: 16px; margin: 16px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span style="color: #6b7280;">Source:</span>
                    <strong>{source.title()}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span style="color: #6b7280;">Rating:</span>
                    <strong>{'★' * int(rating)}{'☆' * (5 - int(rating))} ({rating}/5)</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span style="color: #6b7280;">Sentiment:</span>
                    <span style="background: {sentiment_color}; color: white; padding: 2px 8px; border-radius: 4px;">{sentiment_label.title()}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <span style="color: #6b7280;">Author:</span>
                    <strong>{author or 'Anonymous'}</strong>
                </div>
            </div>

            <div style="background: white; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h3 style="color: #1f2937; margin-top: 0;">Review Text</h3>
                <p style="color: #4b5563; line-height: 1.6;">{text or 'No text provided'}</p>
            </div>
        </div>

        <div style="background: #1f2937; color: #9ca3af; padding: 16px; text-align: center; font-size: 12px;">
            Sent by Review Hound • <a href="#" style="color: #9ca3af;">Manage alerts</a>
        </div>
    </body>
    </html>
    """

    return subject, body


def check_and_send_alerts(session, business, review) -> int:
    """Check if review triggers any alerts and send them.

    Returns number of alerts sent.
    """
    from reviewhound.models import AlertConfig

    alerts_sent = 0

    configs = session.query(AlertConfig).filter(
        AlertConfig.business_id == business.id,
        AlertConfig.enabled == True
    ).all()

    for config in configs:
        should_alert = False

        # Check negative review threshold
        if config.alert_on_negative and review.rating:
            if review.rating <= config.negative_threshold:
                should_alert = True

        # Also alert on negative sentiment regardless of rating
        if config.alert_on_negative and review.sentiment_label == 'negative':
            should_alert = True

        if should_alert:
            subject, body = format_review_alert(
                business_name=business.name,
                source=review.source,
                rating=review.rating or 0,
                sentiment_label=review.sentiment_label or 'neutral',
                text=review.text or '',
                author=review.author_name
            )

            if send_alert(config.email, subject, body):
                alerts_sent += 1

    return alerts_sent
