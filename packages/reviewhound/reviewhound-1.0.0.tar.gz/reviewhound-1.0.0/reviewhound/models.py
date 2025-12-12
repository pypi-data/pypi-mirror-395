from datetime import datetime, date, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, Date, Boolean,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def utcnow():
    return datetime.now(timezone.utc)


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(500))
    trustpilot_url = Column(String(500))
    bbb_url = Column(String(500))
    yelp_url = Column(String(500))
    # API-based platform IDs
    google_place_id = Column(String(100))
    yelp_business_id = Column(String(100))
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    reviews = relationship("Review", back_populates="business", cascade="all, delete-orphan")
    scrape_logs = relationship("ScrapeLog", back_populates="business", cascade="all, delete-orphan")
    alert_configs = relationship("AlertConfig", back_populates="business", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_source_external_id"),
    )

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    source = Column(String(50), nullable=False)
    external_id = Column(String(255), nullable=False)
    review_url = Column(String(500))
    author_name = Column(String(255))
    rating = Column(Float)
    text = Column(Text)
    review_date = Column(Date)
    sentiment_score = Column(Float)
    sentiment_label = Column(String(20))
    scraped_at = Column(DateTime, default=utcnow)

    business = relationship("Business", back_populates="reviews")


class ScrapeLog(Base):
    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    source = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    reviews_found = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    business = relationship("Business", back_populates="scrape_logs")


class AlertConfig(Base):
    __tablename__ = "alert_configs"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    email = Column(String(255), nullable=False)
    alert_on_negative = Column(Boolean, default=True)
    negative_threshold = Column(Float, default=3.0)
    enabled = Column(Boolean, default=True)

    business = relationship("Business", back_populates="alert_configs")


class APIConfig(Base):
    __tablename__ = "api_configs"

    id = Column(Integer, primary_key=True)
    provider = Column(String(50), unique=True, nullable=False)  # 'google_places', 'yelp_fusion'
    api_key = Column(String(500), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    @staticmethod
    def mask_key(key: str) -> str:
        """Return masked version of API key for display."""
        if not key or len(key) < 8:
            return "****"
        return f"{key[:4]}****{key[-4:]}"


class SentimentConfig(Base):
    __tablename__ = "sentiment_configs"

    id = Column(Integer, primary_key=True)
    # Weight for star rating component (0.0 to 1.0)
    rating_weight = Column(Float, default=0.7)
    # Weight for text analysis component (0.0 to 1.0)
    text_weight = Column(Float, default=0.3)
    # Threshold for positive/negative classification
    threshold = Column(Float, default=0.1)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
