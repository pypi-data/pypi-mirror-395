from textblob import TextBlob

from reviewhound.config import Config


def analyze_review(
    text: str,
    rating: float | None = None,
    rating_weight: float | None = None,
    text_weight: float | None = None,
    threshold: float | None = None,
) -> tuple[float, str]:
    """Analyze sentiment using weighted combination of rating and text.

    Args:
        text: Review text to analyze
        rating: Star rating (1-5)
        rating_weight: Weight for rating component (0.0-1.0), defaults to config
        text_weight: Weight for text component (0.0-1.0), defaults to config
        threshold: Threshold for positive/negative classification, defaults to config

    Returns:
        tuple of (score, label) where:
        - score: float from -1.0 (negative) to 1.0 (positive)
        - label: 'positive', 'negative', or 'neutral'
    """
    # Use defaults from config if not specified
    if rating_weight is None:
        rating_weight = Config.SENTIMENT_RATING_WEIGHT
    if text_weight is None:
        text_weight = Config.SENTIMENT_TEXT_WEIGHT
    if threshold is None:
        threshold = Config.SENTIMENT_THRESHOLD

    # Calculate rating score (convert 1-5 to -1.0 to 1.0)
    rating_score = None
    if rating is not None:
        rating_score = (rating - Config.RATING_SCALE_CENTER) / Config.RATING_SCALE_DIVISOR

    # Calculate text score using TextBlob
    text_score = None
    if text and text.strip():
        blob = TextBlob(text)
        text_score = blob.sentiment.polarity

    # Combine scores based on what's available
    if rating_score is not None and text_score is not None:
        # Both available - use weighted combination
        # Normalize weights in case they don't sum to 1
        total_weight = rating_weight + text_weight
        if total_weight > 0:
            norm_rating_weight = rating_weight / total_weight
            norm_text_weight = text_weight / total_weight
            score = (rating_score * norm_rating_weight) + (text_score * norm_text_weight)
        else:
            score = rating_score  # Fallback to rating if weights are zero
    elif rating_score is not None:
        # Only rating available
        score = rating_score
    elif text_score is not None:
        # Only text available
        score = text_score
    else:
        # Neither available
        return 0.0, "neutral"

    # Classify based on threshold
    if score > threshold:
        label = "positive"
    elif score < -threshold:
        label = "negative"
    else:
        label = "neutral"

    return score, label


def rating_to_score(rating: float | None) -> float:
    """Convert 1-5 star rating to -1.0 to 1.0 score."""
    if rating is None:
        return 0.0
    return (rating - Config.RATING_SCALE_CENTER) / Config.RATING_SCALE_DIVISOR


def text_to_score(text: str | None) -> float:
    """Analyze text and return polarity score from -1.0 to 1.0."""
    if not text or not text.strip():
        return 0.0
    blob = TextBlob(text)
    return blob.sentiment.polarity
