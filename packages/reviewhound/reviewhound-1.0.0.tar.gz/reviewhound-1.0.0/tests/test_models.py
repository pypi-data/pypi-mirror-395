from datetime import date
import pytest
from sqlalchemy.exc import IntegrityError

from reviewhound.models import Business, Review, ScrapeLog, AlertConfig, APIConfig, utcnow


class TestBusiness:
    def test_create_business(self, db_session):
        business = Business(name="Joe's Pizza")
        db_session.add(business)
        db_session.flush()

        assert business.id is not None
        assert business.name == "Joe's Pizza"
        assert business.created_at is not None

    def test_business_with_urls(self, db_session):
        business = Business(
            name="Test Biz",
            trustpilot_url="https://trustpilot.com/review/test.com",
            bbb_url="https://bbb.org/test",
            yelp_url="https://yelp.com/biz/test",
        )
        db_session.add(business)
        db_session.flush()

        assert business.trustpilot_url == "https://trustpilot.com/review/test.com"
        assert business.bbb_url == "https://bbb.org/test"
        assert business.yelp_url == "https://yelp.com/biz/test"

    def test_business_name_required(self, db_session):
        business = Business()
        db_session.add(business)
        with pytest.raises(IntegrityError):
            db_session.flush()


class TestReview:
    def test_create_review(self, db_session):
        business = Business(name="Test Biz")
        db_session.add(business)
        db_session.flush()

        review = Review(
            business_id=business.id,
            source="trustpilot",
            external_id="tp_12345",
            author_name="John Doe",
            rating=4.5,
            text="Great service!",
            review_date=date(2024, 1, 15),
        )
        db_session.add(review)
        db_session.flush()

        assert review.id is not None
        assert review.business_id == business.id
        assert review.source == "trustpilot"
        assert review.rating == 4.5

    def test_review_external_id_unique_per_source(self, db_session):
        business = Business(name="Test Biz")
        db_session.add(business)
        db_session.flush()

        review1 = Review(
            business_id=business.id,
            source="trustpilot",
            external_id="tp_12345",
            author_name="John",
            rating=5.0,
            text="Great!",
            review_date=date(2024, 1, 1),
        )
        db_session.add(review1)
        db_session.flush()

        review2 = Review(
            business_id=business.id,
            source="trustpilot",
            external_id="tp_12345",
            author_name="Jane",
            rating=4.0,
            text="Good!",
            review_date=date(2024, 1, 2),
        )
        db_session.add(review2)
        with pytest.raises(IntegrityError):
            db_session.flush()

    def test_review_same_external_id_different_source(self, db_session):
        business = Business(name="Test Biz")
        db_session.add(business)
        db_session.flush()

        review1 = Review(
            business_id=business.id,
            source="trustpilot",
            external_id="12345",
            author_name="John",
            rating=5.0,
            text="Great!",
            review_date=date(2024, 1, 1),
        )
        review2 = Review(
            business_id=business.id,
            source="yelp",
            external_id="12345",
            author_name="Jane",
            rating=4.0,
            text="Good!",
            review_date=date(2024, 1, 2),
        )
        db_session.add_all([review1, review2])
        db_session.flush()

        assert review1.id != review2.id

    def test_review_business_relationship(self, db_session):
        business = Business(name="Test Biz")
        db_session.add(business)
        db_session.flush()

        review = Review(
            business_id=business.id,
            source="trustpilot",
            external_id="tp_001",
            author_name="Test",
            rating=3.0,
            text="OK",
            review_date=date(2024, 1, 1),
        )
        db_session.add(review)
        db_session.flush()

        assert review.business.name == "Test Biz"
        assert business.reviews[0].external_id == "tp_001"


class TestScrapeLog:
    def test_create_scrape_log(self, db_session):
        business = Business(name="Test Biz")
        db_session.add(business)
        db_session.flush()

        log = ScrapeLog(
            business_id=business.id,
            source="trustpilot",
            status="success",
            reviews_found=15,
            started_at=utcnow(),
            completed_at=utcnow(),
        )
        db_session.add(log)
        db_session.flush()

        assert log.id is not None
        assert log.status == "success"
        assert log.reviews_found == 15

    def test_scrape_log_with_error(self, db_session):
        business = Business(name="Test Biz")
        db_session.add(business)
        db_session.flush()

        log = ScrapeLog(
            business_id=business.id,
            source="yelp",
            status="failed",
            reviews_found=0,
            error_message="Connection timeout",
            started_at=utcnow(),
            completed_at=utcnow(),
        )
        db_session.add(log)
        db_session.flush()

        assert log.error_message == "Connection timeout"


class TestAlertConfig:
    def test_create_alert_config(self, db_session):
        business = Business(name="Test Biz")
        db_session.add(business)
        db_session.flush()

        alert = AlertConfig(
            business_id=business.id,
            email="owner@test.com",
        )
        db_session.add(alert)
        db_session.flush()

        assert alert.id is not None
        assert alert.alert_on_negative is True
        assert alert.negative_threshold == 3.0
        assert alert.enabled is True

    def test_alert_config_custom_threshold(self, db_session):
        business = Business(name="Test Biz")
        db_session.add(business)
        db_session.flush()

        alert = AlertConfig(
            business_id=business.id,
            email="owner@test.com",
            negative_threshold=2.5,
            alert_on_negative=True,
            enabled=False,
        )
        db_session.add(alert)
        db_session.flush()

        assert alert.negative_threshold == 2.5
        assert alert.enabled is False


class TestAPIConfig:
    def test_create_api_config(self, db_session):
        config = APIConfig(
            provider="google_places",
            api_key="test-api-key-12345",
            enabled=True,
        )
        db_session.add(config)
        db_session.flush()

        assert config.id is not None
        assert config.provider == "google_places"
        assert config.api_key == "test-api-key-12345"
        assert config.enabled is True

    def test_api_config_unique_provider(self, db_session):
        config1 = APIConfig(provider="yelp_fusion", api_key="key1")
        db_session.add(config1)
        db_session.flush()

        config2 = APIConfig(provider="yelp_fusion", api_key="key2")
        db_session.add(config2)

        with pytest.raises(IntegrityError):
            db_session.flush()

    def test_mask_key_short(self):
        assert APIConfig.mask_key("abc") == "****"
        assert APIConfig.mask_key("") == "****"
        assert APIConfig.mask_key(None) == "****"

    def test_mask_key_normal(self):
        assert APIConfig.mask_key("AIzaSyC12345678901234567890abcdef") == "AIza****cdef"
        assert APIConfig.mask_key("12345678") == "1234****5678"


class TestBusinessAPIFields:
    def test_business_with_api_ids(self, db_session):
        business = Business(
            name="Test Business",
            google_place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
            yelp_business_id="gary-danko-san-francisco",
        )
        db_session.add(business)
        db_session.flush()

        assert business.google_place_id == "ChIJN1t_tDeuEmsRUsoyG83frY4"
        assert business.yelp_business_id == "gary-danko-san-francisco"
