"""Shared business logic for Review Hound."""

import logging
from datetime import datetime, timezone, timedelta

from reviewhound.config import Config
from reviewhound.models import Review, ScrapeLog, Business, SentimentConfig
from reviewhound.analysis import analyze_review
from reviewhound.alerts import check_and_send_alerts

logger = logging.getLogger(__name__)


def _normalize_review_date(review) -> datetime:
    """Get a datetime for a review, using review_date or scraped_at as fallback."""
    if review.review_date:
        return datetime.combine(review.review_date, datetime.min.time(), tzinfo=timezone.utc)
    return review.scraped_at


def get_sentiment_weights(session) -> tuple[float, float, float]:
    """Get sentiment weights from database or defaults.

    Returns:
        Tuple of (rating_weight, text_weight, threshold)
    """
    config = session.query(SentimentConfig).first()
    if config:
        return config.rating_weight, config.text_weight, config.threshold
    return Config.SENTIMENT_RATING_WEIGHT, Config.SENTIMENT_TEXT_WEIGHT, Config.SENTIMENT_THRESHOLD


def _process_reviews(
    session,
    business: Business,
    source: str,
    reviews_data: list[dict],
    send_alerts: bool,
) -> int:
    """Process and save reviews to the database.

    Args:
        session: Database session
        business: Business the reviews belong to
        source: Source name (e.g., 'trustpilot', 'bbb', 'yelp')
        reviews_data: List of review dicts from scraper
        send_alerts: Whether to check and send alerts for new reviews

    Returns:
        Number of new reviews saved
    """
    new_count = 0
    rating_weight, text_weight, threshold = get_sentiment_weights(session)

    for review_data in reviews_data:
        existing = session.query(Review).filter(
            Review.source == source,
            Review.external_id == review_data["external_id"],
        ).first()

        if existing:
            continue

        rating = review_data.get("rating")
        score, label = analyze_review(
            review_data.get("text", ""),
            rating,
            rating_weight=rating_weight,
            text_weight=text_weight,
            threshold=threshold,
        )

        review = Review(
            business_id=business.id,
            source=source,
            external_id=review_data["external_id"],
            review_url=review_data.get("review_url"),
            author_name=review_data.get("author_name"),
            rating=rating,
            text=review_data.get("text"),
            review_date=review_data.get("review_date"),
            sentiment_score=score,
            sentiment_label=label,
        )
        session.add(review)
        new_count += 1

        if send_alerts:
            session.flush()
            check_and_send_alerts(session, business, review)

    return new_count


def save_scraped_reviews(
    session,
    business: Business,
    source: str,
    reviews_data: list[dict],
    send_alerts: bool = True,
) -> tuple[ScrapeLog, int]:
    """Save scraped reviews to the database.

    Args:
        session: Database session
        business: Business the reviews belong to
        source: Source name (e.g., 'trustpilot', 'bbb', 'yelp')
        reviews_data: List of review dicts from scraper
        send_alerts: Whether to check and send alerts for new reviews

    Returns:
        Tuple of (ScrapeLog, new_review_count)
    """
    log = ScrapeLog(
        business_id=business.id,
        source=source,
        status="running",
        started_at=datetime.now(timezone.utc),
    )
    session.add(log)
    session.flush()

    new_count = _process_reviews(session, business, source, reviews_data, send_alerts)

    log.status = "success"
    log.reviews_found = new_count
    log.completed_at = datetime.now(timezone.utc)

    return log, new_count


def run_scraper_for_business(
    session,
    business: Business,
    scraper,
    url: str,
    send_alerts: bool = True,
) -> tuple[ScrapeLog, int]:
    """Run a scraper and save results.

    Args:
        session: Database session
        business: Business to scrape
        scraper: Scraper instance with .source and .scrape() method
        url: URL to scrape
        send_alerts: Whether to send alerts for new reviews

    Returns:
        Tuple of (ScrapeLog, new_review_count)
    """
    source = scraper.source

    log = ScrapeLog(
        business_id=business.id,
        source=source,
        status="running",
        started_at=datetime.now(timezone.utc),
    )
    session.add(log)
    session.flush()

    try:
        reviews_data = scraper.scrape(url)
        new_count = _process_reviews(session, business, source, reviews_data, send_alerts)

        log.status = "success"
        log.reviews_found = new_count
        log.completed_at = datetime.now(timezone.utc)

        return log, new_count

    except Exception as e:
        logger.exception(f"Scrape failed for {business.name} from {source}: {e}")
        log.status = "failed"
        log.error_message = str(e)
        log.completed_at = datetime.now(timezone.utc)
        raise


def calculate_review_stats(reviews: list[Review]) -> dict:
    """Calculate statistics for a list of reviews.

    Args:
        reviews: List of Review objects

    Returns:
        Dict with keys: total, avg_rating, positive, negative, neutral,
        positive_pct, negative_pct, neutral_pct, by_source,
        trend_direction, trend_delta, recent_count, last_review_date,
        recent_negative_count
    """
    total = len(reviews)
    now = datetime.now(timezone.utc)
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)
    sixty_days_ago = now - timedelta(days=60)

    if total == 0:
        return {
            "total": 0,
            "avg_rating": 0.0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "positive_pct": 0.0,
            "negative_pct": 0.0,
            "neutral_pct": 0.0,
            "by_source": {},
            "trend_direction": None,
            "trend_delta": 0.0,
            "recent_count": 0,
            "last_review_date": None,
            "recent_negative_count": 0,
        }

    rated_reviews = [r for r in reviews if r.rating is not None]
    avg_rating = sum(r.rating for r in rated_reviews) / len(rated_reviews) if rated_reviews else 0.0

    positive = len([r for r in reviews if r.sentiment_label == "positive"])
    negative = len([r for r in reviews if r.sentiment_label == "negative"])
    neutral = len([r for r in reviews if r.sentiment_label == "neutral"])

    by_source = {}
    for r in reviews:
        by_source[r.source] = by_source.get(r.source, 0) + 1

    # Calculate trend: compare last 30 days vs previous 30 days
    recent_rated = [r for r in rated_reviews if _normalize_review_date(r) >= thirty_days_ago]
    previous_rated = [r for r in rated_reviews
                      if sixty_days_ago <= _normalize_review_date(r) < thirty_days_ago]

    trend_direction = None
    trend_delta = 0.0
    if recent_rated and previous_rated:
        recent_avg = sum(r.rating for r in recent_rated) / len(recent_rated)
        previous_avg = sum(r.rating for r in previous_rated) / len(previous_rated)
        trend_delta = recent_avg - previous_avg
        if trend_delta > Config.TREND_STABILITY_THRESHOLD:
            trend_direction = "up"
        elif trend_delta < -Config.TREND_STABILITY_THRESHOLD:
            trend_direction = "down"
        else:
            trend_direction = "stable"

    # Recent activity: reviews in last 7 days
    recent_reviews = [r for r in reviews if _normalize_review_date(r) >= seven_days_ago]
    recent_count = len(recent_reviews)

    # Most recent review date
    if reviews:
        last_review_date = max(_normalize_review_date(r) for r in reviews)
    else:
        last_review_date = None

    # Negative reviews in last 7 days
    recent_negative_count = len([r for r in recent_reviews if r.sentiment_label == "negative"])

    return {
        "total": total,
        "avg_rating": avg_rating,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_pct": (positive / total * 100) if total else 0.0,
        "negative_pct": (negative / total * 100) if total else 0.0,
        "neutral_pct": (neutral / total * 100) if total else 0.0,
        "by_source": by_source,
        "trend_direction": trend_direction,
        "trend_delta": trend_delta,
        "recent_count": recent_count,
        "last_review_date": last_review_date,
        "recent_negative_count": recent_negative_count,
    }
