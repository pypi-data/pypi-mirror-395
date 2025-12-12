import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class Config:
    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/reviews.db")

    # Scraping
    REQUEST_DELAY_MIN = float(os.getenv("REQUEST_DELAY_MIN", "2.0"))
    REQUEST_DELAY_MAX = float(os.getenv("REQUEST_DELAY_MAX", "4.0"))
    MAX_PAGES_PER_SOURCE = int(os.getenv("MAX_PAGES_PER_SOURCE", "3"))

    # Email Alerts
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM = os.getenv("SMTP_FROM", "alerts@example.com")

    # Web
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-key-change-in-production")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # Scheduler
    SCRAPE_INTERVAL_HOURS = int(os.getenv("SCRAPE_INTERVAL_HOURS", "6"))

    # UI Display
    REVIEW_TEXT_PREVIEW_LENGTH = 200
    REVIEWS_PER_PAGE = 20
    CHART_MONTHS = 12

    # BBB Complaints
    COMPLAINT_DEFAULT_RATING = 1.0

    # Sentiment Analysis Defaults
    SENTIMENT_RATING_WEIGHT = 0.7  # Weight for star rating (0.0-1.0)
    SENTIMENT_TEXT_WEIGHT = 0.3   # Weight for text analysis (0.0-1.0)
    SENTIMENT_THRESHOLD = 0.1     # Threshold for positive/negative classification

    # Rating conversion (1-5 stars to -1.0 to 1.0 score)
    RATING_SCALE_CENTER = 3       # Center point of 1-5 star scale
    RATING_SCALE_DIVISOR = 2      # Divisor to normalize to -1.0 to 1.0

    # Trend analysis
    TREND_STABILITY_THRESHOLD = 0.1  # Threshold for up/down/stable trend detection

    @classmethod
    def get_database_url(cls) -> str:
        db_path = cls.DATABASE_PATH
        if not db_path.startswith(":"):
            path = Path(db_path)
            if not path.is_absolute():
                path = Path.cwd() / path
            path.parent.mkdir(parents=True, exist_ok=True)
            db_path = str(path)
        return f"sqlite:///{db_path}"
