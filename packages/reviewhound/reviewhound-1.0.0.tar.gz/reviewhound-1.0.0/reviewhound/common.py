"""Shared utilities for Review Hound.

Contains helper functions used across CLI, web, and scheduler modules.
"""

import logging

from reviewhound.models import APIConfig
from reviewhound.scrapers import (
    TrustPilotScraper, BBBScraper, YelpScraper,
    GooglePlacesScraper, YelpAPIScraper
)
from reviewhound.services import run_scraper_for_business

logger = logging.getLogger(__name__)


def get_api_config(session, provider: str):
    """Get API config for a provider if it exists and is enabled."""
    return session.query(APIConfig).filter(
        APIConfig.provider == provider,
        APIConfig.enabled == True
    ).first()


def build_scrapers_for_business(session, business) -> list[tuple]:
    """Build list of (scraper, identifier) tuples for a business.

    Returns scrapers configured based on business URLs and API availability.
    """
    scrapers = []

    # Google Places API (no web scraping fallback)
    google_config = get_api_config(session, 'google_places')
    if google_config and business.google_place_id:
        scrapers.append((
            GooglePlacesScraper(google_config.api_key),
            business.google_place_id
        ))

    # Yelp: prefer API, fall back to web scraping
    yelp_config = get_api_config(session, 'yelp_fusion')
    if yelp_config and business.yelp_business_id:
        scrapers.append((
            YelpAPIScraper(yelp_config.api_key),
            business.yelp_business_id
        ))
    elif business.yelp_url:
        scrapers.append((YelpScraper(), business.yelp_url))

    # Web scraping only sources
    if business.trustpilot_url:
        scrapers.append((TrustPilotScraper(), business.trustpilot_url))
    if business.bbb_url:
        scrapers.append((BBBScraper(), business.bbb_url))

    return scrapers


def scrape_business_sources(session, business, send_alerts: bool = False) -> tuple[int, list[str]]:
    """Run all configured scrapers for a business.

    Args:
        session: Database session
        business: Business to scrape
        send_alerts: Whether to send alerts for new reviews

    Returns:
        Tuple of (total_new_reviews, list_of_failed_sources)
    """
    scrapers = build_scrapers_for_business(session, business)

    total_new = 0
    failed_sources = []

    for scraper, identifier in scrapers:
        try:
            log, new_count = run_scraper_for_business(
                session, business, scraper, identifier, send_alerts=send_alerts
            )
            total_new += new_count
        except Exception as e:
            logger.error(f"Scraper {scraper.source} failed for {business.name}: {e}")
            failed_sources.append(scraper.source)

    return total_new, failed_sources
