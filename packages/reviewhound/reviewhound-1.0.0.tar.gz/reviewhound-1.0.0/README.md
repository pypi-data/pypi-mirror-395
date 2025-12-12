# 🐕 Review Hound

[![CI](https://img.shields.io/github/actions/workflow/status/jonmartin721/review-hound/ci.yml?branch=main&style=flat)](https://github.com/jonmartin721/review-hound/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776ab?style=flat)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat)](LICENSE)
[![codecov](https://img.shields.io/codecov/c/github/jonmartin721/review-hound?style=flat)](https://codecov.io/gh/jonmartin721/review-hound)

Stop checking TrustPilot, BBB, and Yelp separately. Review Hound scrapes them all, flags negative reviews, and emails you before customers start talking.

**Why?** Bad reviews spread. A 1-star complaint on Yelp can sit for days before you notice. Review Hound catches them within hours.

## Features

- **One command, three sources**: `reviewhound scrape --all` hits TrustPilot, BBB, and Yelp
- **Sentiment scoring**: Flags negative reviews automatically so you know what needs attention
- **Web dashboard**: See all your businesses, ratings, and trends in one place
- **Email alerts**: Get notified when someone leaves a bad review
- **CLI or web**: Use whichever fits your workflow
- **Scheduled scraping**: Set it and forget it—runs every few hours
- **CSV export**: Pull data out for spreadsheets or reporting

## Screenshots

### Dashboard
Track all your businesses at a glance with ratings, sentiment breakdowns, and trend indicators.

![Dashboard](docs/screenshots/dashboard.png)

### Business Detail
See individual business metrics with rating trends and quick actions.

![Business Detail](docs/screenshots/business_detail.png)

### Reviews
Browse and filter reviews by source and sentiment, with CSV export support.

![Reviews](docs/screenshots/reviews.png)

### Settings
Configure API keys for Google Places and Yelp Fusion, plus sentiment analysis tuning.

![Settings](docs/screenshots/settings.png)

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/jonmartin721/review-hound.git
cd review-hound

# Start with Docker Compose
docker-compose up -d

# Access the web dashboard
open http://localhost:5000
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/jonmartin721/review-hound.git
cd review-hound

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run the web dashboard
python -m reviewhound web
```

## CLI Usage

### Add a Business

```bash
# Add with TrustPilot URL
reviewhound add "Acme Corp" --trustpilot "https://www.trustpilot.com/review/acme.com"

# Add with multiple sources
reviewhound add "Acme Corp" \
  --trustpilot "https://www.trustpilot.com/review/acme.com" \
  --bbb "https://www.bbb.org/..." \
  --yelp "https://www.yelp.com/biz/acme-corp"
```

### Scrape Reviews

```bash
# Scrape one business
reviewhound scrape "Acme"
# → Scraped 47 reviews from 3 sources

# Scrape everything (grab coffee, this takes a minute)
reviewhound scrape --all
# → Scraped 203 reviews across 5 businesses
```

### View Reviews

```bash
# List all businesses
reviewhound list

# View reviews for a business
reviewhound reviews 1 --limit 50

# Filter by sentiment
reviewhound reviews 1 --sentiment negative

# View statistics
reviewhound stats 1
```

### Export Data

```bash
# Export to CSV
reviewhound export 1 -o acme_reviews.csv
```

### Email Alerts

```bash
# Configure alerts for negative reviews
reviewhound alert 1 alerts@company.com --threshold 3.0

# List alert configurations
reviewhound alerts
```

### Scheduled Scraping

```bash
# Run scheduler (scrapes every 6 hours by default)
reviewhound watch

# Custom interval
reviewhound watch --interval 2

# Run web dashboard with scheduler
reviewhound web --with-scheduler
```

## Configuration

Create a `.env` file in the project root:

```env
# Database
DATABASE_PATH=data/reviews.db

# Scraping
REQUEST_DELAY_MIN=2.0
REQUEST_DELAY_MAX=4.0
MAX_PAGES_PER_SOURCE=3

# Scheduler
SCRAPE_INTERVAL_HOURS=6

# Email Alerts (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=alerts@yourdomain.com

# Web Dashboard
FLASK_SECRET_KEY=change-this-in-production
FLASK_DEBUG=false
```

## Web Dashboard

The web dashboard provides:

- **Dashboard**: Overview of all businesses with sentiment bars and ratings
- **Business Detail**: Individual business stats, rating trends, and recent reviews
- **Reviews Page**: Filterable list of all reviews with pagination
- **One-Click Scraping**: Trigger scrapes directly from the UI

Access at `http://localhost:5000` after starting with `reviewhound web`.

## Project Structure

```
review-hound/
├── reviewhound/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py              # CLI commands
│   ├── config.py           # Configuration
│   ├── database.py         # Database setup
│   ├── models.py           # SQLAlchemy models
│   ├── scheduler.py        # APScheduler setup
│   ├── scrapers/
│   │   ├── base.py         # Abstract scraper
│   │   ├── trustpilot.py
│   │   ├── bbb.py
│   │   └── yelp.py
│   ├── analysis/
│   │   └── sentiment.py    # TextBlob analysis
│   ├── alerts/
│   │   └── email.py        # SMTP alerts
│   └── web/
│       ├── app.py          # Flask factory
│       ├── routes.py       # Web routes
│       ├── templates/
│       └── static/
├── tests/
├── data/                   # SQLite database
├── exports/                # CSV exports
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Development

```bash
# Run tests
pytest tests/ -v

# Run with debug mode
reviewhound web --debug
```

## What's Next?

- Set up email alerts: `reviewhound alert 1 you@email.com`
- Run the scheduler for hands-off monitoring: `reviewhound watch`
- Found a bug? [Open an issue](https://github.com/jonmartin721/review-hound/issues)

## Disclaimer

Web scraping may violate some websites' Terms of Service. Use responsibly and respect rate limits.

## License

MIT License - see LICENSE file for details.
