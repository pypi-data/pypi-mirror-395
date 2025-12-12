from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from reviewhound.config import Config
from reviewhound.database import get_session
from reviewhound.models import Business
from reviewhound.common import build_scrapers_for_business
from reviewhound.services import run_scraper_for_business


def scrape_all_businesses():
    """Job function to scrape all businesses."""
    print(f"[Scheduler] Starting scrape job at {datetime.now()}")

    with get_session() as session:
        businesses = session.query(Business).all()

        for business in businesses:
            _scrape_business_job(session, business)

    print(f"[Scheduler] Scrape job completed at {datetime.now()}")


def _scrape_business_job(session, business):
    """Scrape a single business (called by scheduler)."""
    print(f"[Scheduler] Scraping: {business.name}")

    scrapers = build_scrapers_for_business(session, business)

    if not scrapers:
        print(f"[Scheduler]   No sources configured for {business.name}")
        return

    for scraper, identifier in scrapers:
        source = scraper.source
        try:
            log, new_count = run_scraper_for_business(session, business, scraper, identifier)
            print(f"[Scheduler]   {source}: {new_count} new reviews")
        except Exception as e:
            print(f"[Scheduler]   {source}: Failed - {e}")


def create_scheduler(blocking: bool = True) -> BackgroundScheduler | BlockingScheduler:
    """Create and configure the scheduler.

    Args:
        blocking: If True, returns BlockingScheduler (for standalone watch command).
                  If False, returns BackgroundScheduler (for web server integration).
    """
    if blocking:
        scheduler = BlockingScheduler()
    else:
        scheduler = BackgroundScheduler()

    # Add the scrape job
    scheduler.add_job(
        scrape_all_businesses,
        'interval',
        hours=Config.SCRAPE_INTERVAL_HOURS,
        id='scrape_all',
        name='Scrape all businesses',
        next_run_time=datetime.now()  # Run immediately on start
    )

    return scheduler


def run_scheduler():
    """Run the blocking scheduler (for CLI watch command)."""
    print(f"Starting scheduler (interval: {Config.SCRAPE_INTERVAL_HOURS} hours)")
    print("Press Ctrl+C to stop")

    scheduler = create_scheduler(blocking=True)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped")
