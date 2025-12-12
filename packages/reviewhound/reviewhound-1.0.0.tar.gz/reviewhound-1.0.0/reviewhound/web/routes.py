from collections import defaultdict
import csv
import io
import json
import logging
from urllib.parse import urlparse

from flask import Blueprint, render_template, request, jsonify, Response, redirect, url_for

from reviewhound.config import Config
from reviewhound.database import get_session
from reviewhound.models import Business, Review, ScrapeLog, AlertConfig, APIConfig, SentimentConfig
from reviewhound.scrapers import TrustPilotScraper, BBBScraper, GooglePlacesScraper, YelpAPIScraper
from reviewhound.services import calculate_review_stats
from reviewhound.common import get_api_config, scrape_business_sources

logger = logging.getLogger(__name__)

# Validation constants
MAX_NAME_LENGTH = 200
MAX_ADDRESS_LENGTH = 500
MAX_URL_LENGTH = 2000


def _validate_url(url: str | None, field_name: str) -> str | None:
    """Validate URL format. Returns error message or None if valid."""
    if not url:
        return None
    if len(url) > MAX_URL_LENGTH:
        return f"{field_name} exceeds maximum length of {MAX_URL_LENGTH} characters"
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return f"{field_name} must be a valid URL with scheme (http/https)"
    except Exception:
        return f"{field_name} is not a valid URL"
    return None


def _validate_string(value: str | None, field_name: str, max_length: int) -> str | None:
    """Validate string length. Returns error message or None if valid."""
    if not value:
        return None
    if len(value) > max_length:
        return f"{field_name} exceeds maximum length of {max_length} characters"
    return None


def _get_scrape_health(session, business_id: int) -> dict:
    """Calculate scrape health indicators for a business.

    Returns dict with:
        - has_issues: bool - True if there are any scrape problems
        - issue_sources: list - Sources with problems
        - issue_type: str - 'failed' or 'no_reviews' or None
    """
    # Get all scrape logs for this business, grouped by source
    logs = session.query(ScrapeLog).filter(
        ScrapeLog.business_id == business_id
    ).order_by(ScrapeLog.started_at.desc()).all()

    if not logs:
        return {'has_issues': False, 'issue_sources': [], 'issue_type': None}

    # Group logs by source
    by_source = {}
    for log in logs:
        if log.source not in by_source:
            by_source[log.source] = []
        by_source[log.source].append(log)

    issue_sources = []
    issue_type = None

    for source, source_logs in by_source.items():
        # Check last 3 scrapes for this source
        recent = source_logs[:3]

        # Check for repeated failures (2+ failures in last 3 attempts)
        recent_failures = sum(1 for log in recent if log.status == 'failed')
        if recent_failures >= 2:
            issue_sources.append(source)
            issue_type = 'failed'
            continue

        # Check if source has NEVER returned reviews (all successful scrapes = 0)
        successful = [log for log in source_logs if log.status == 'success']
        if successful:
            total_ever_found = sum(log.reviews_found or 0 for log in successful)
            if total_ever_found == 0:
                issue_sources.append(source)
                if issue_type != 'failed':  # 'failed' takes priority
                    issue_type = 'no_reviews'

    return {
        'has_issues': len(issue_sources) > 0,
        'issue_sources': issue_sources,
        'issue_type': issue_type
    }


bp = Blueprint('main', __name__)


@bp.route('/welcome')
def welcome():
    return render_template('welcome.html')


@bp.route('/')
def dashboard():
    with get_session() as session:
        businesses = session.query(Business).all()

        # Redirect first-time users to welcome page
        if not businesses:
            return redirect(url_for('main.welcome'))

        business_stats = []
        for b in businesses:
            reviews = session.query(Review).filter(Review.business_id == b.id).all()
            stats = calculate_review_stats(reviews)
            scrape_health = _get_scrape_health(session, b.id)

            business_stats.append({
                'business': b,
                'total_reviews': stats["total"],
                'avg_rating': stats["avg_rating"],
                'positive_pct': stats["positive_pct"],
                'negative_pct': stats["negative_pct"],
                'trend_direction': stats["trend_direction"],
                'trend_delta': stats["trend_delta"],
                'recent_count': stats["recent_count"],
                'last_review_date': stats["last_review_date"],
                'recent_negative_count': stats["recent_negative_count"],
                'scrape_issues': scrape_health['has_issues'],
                'scrape_issue_sources': scrape_health['issue_sources'],
                'scrape_issue_type': scrape_health['issue_type'],
            })

        # Check if API keys are configured
        has_google_api = get_api_config(session, 'google_places') is not None
        has_yelp_api = get_api_config(session, 'yelp_fusion') is not None

        return render_template('dashboard.html',
            businesses=business_stats,
            has_google_api=has_google_api,
            has_yelp_api=has_yelp_api
        )


@bp.route('/business/<int:business_id>')
def business_detail(business_id):
    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return "Business not found", 404

        reviews = session.query(Review).filter(
            Review.business_id == business_id
        ).order_by(Review.scraped_at.desc()).all()

        scrape_logs = session.query(ScrapeLog).filter(
            ScrapeLog.business_id == business_id
        ).order_by(ScrapeLog.started_at.desc()).all()

        review_stats = calculate_review_stats(reviews)
        stats = {
            'total_reviews': review_stats["total"],
            'avg_rating': review_stats["avg_rating"],
            'positive_pct': review_stats["positive_pct"],
            'negative_pct': review_stats["negative_pct"],
        }

        # Chart data - group by month
        monthly_ratings = defaultdict(list)
        for r in reviews:
            if r.rating and r.review_date:
                key = r.review_date.strftime('%Y-%m')
                monthly_ratings[key].append(r.rating)

        sorted_months = sorted(monthly_ratings.keys())[-Config.CHART_MONTHS:]
        chart_labels = sorted_months
        chart_data = [sum(monthly_ratings[m])/len(monthly_ratings[m]) for m in sorted_months]

        # Check if API keys are configured
        has_google_api = get_api_config(session, 'google_places') is not None
        has_yelp_api = get_api_config(session, 'yelp_fusion') is not None

        return render_template('business.html',
            business=business,
            reviews=reviews,
            scrape_logs=scrape_logs,
            stats=stats,
            chart_labels=json.dumps(chart_labels),
            chart_data=json.dumps(chart_data),
            has_google_api=has_google_api,
            has_yelp_api=has_yelp_api
        )


@bp.route('/business/<int:business_id>/reviews')
def business_reviews(business_id):
    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return "Business not found", 404

        page = request.args.get('page', 1, type=int)
        per_page = Config.REVIEWS_PER_PAGE
        source = request.args.get('source', '')
        sentiment = request.args.get('sentiment', '')

        query = session.query(Review).filter(Review.business_id == business_id)

        if source:
            query = query.filter(Review.source == source)
        if sentiment:
            query = query.filter(Review.sentiment_label == sentiment)

        total = query.count()
        total_pages = (total + per_page - 1) // per_page

        reviews = query.order_by(Review.scraped_at.desc()).offset((page-1)*per_page).limit(per_page).all()

        return render_template('reviews.html',
            business=business,
            reviews=reviews,
            page=page,
            total_pages=total_pages
        )


@bp.route('/business/<int:business_id>/scrape', methods=['POST'])
def trigger_scrape(business_id):
    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return jsonify({'success': False, 'error': 'Business not found'}), 404

        has_sources = business.trustpilot_url or business.bbb_url or business.yelp_url
        if not has_sources:
            return jsonify({
                'success': False,
                'error': 'No review sources configured. Edit business to add TrustPilot, BBB, or Yelp URLs.'
            }), 400

        total_new, failed_sources = scrape_business_sources(
            session, business, send_alerts=False
        )

        # Count configured sources to check if all failed
        source_count = sum([
            bool(business.trustpilot_url),
            bool(business.bbb_url),
            bool(business.yelp_url),
        ])

        if failed_sources and len(failed_sources) == source_count:
            return jsonify({
                'success': False,
                'error': f'All scrapes failed: {", ".join(failed_sources)}'
            }), 500

        return jsonify({
            'success': True,
            'new_reviews': total_new,
            'failed_sources': failed_sources if failed_sources else None
        })


@bp.route('/api/search-sources', methods=['POST'])
def api_search_sources():
    data = request.get_json()
    if not data or not data.get('query'):
        return jsonify({'success': False, 'error': 'Query is required'}), 400

    query = data['query']
    location = data.get('location')

    results = {
        'trustpilot': [],
        'bbb': [],
    }

    # Search each platform
    scrapers = [
        ('trustpilot', TrustPilotScraper()),
        ('bbb', BBBScraper()),
    ]

    for source, scraper in scrapers:
        try:
            results[source] = scraper.search(query, location)
        except Exception as e:
            logger.error(f"Search failed for {source}: {e}")
            results[source] = []

    return jsonify({'success': True, 'results': results})


@bp.route('/api/business/<int:business_id>/stats')
def api_business_stats(business_id):
    with get_session() as session:
        reviews = session.query(Review).filter(Review.business_id == business_id).all()

        monthly_ratings = defaultdict(list)
        for r in reviews:
            if r.rating and r.review_date:
                key = r.review_date.strftime('%Y-%m')
                monthly_ratings[key].append(r.rating)

        sorted_months = sorted(monthly_ratings.keys())[-Config.CHART_MONTHS:]

        return jsonify({
            'labels': sorted_months,
            'data': [sum(monthly_ratings[m])/len(monthly_ratings[m]) for m in sorted_months]
        })


@bp.route('/api/business', methods=['POST'])
def api_create_business():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'success': False, 'error': 'Name is required'}), 400

    # Validate inputs
    errors = []
    if err := _validate_string(data['name'], 'name', MAX_NAME_LENGTH):
        errors.append(err)
    elif not data['name'].strip():
        errors.append('name cannot be empty')
    if data.get('address'):
        if err := _validate_string(data['address'], 'address', MAX_ADDRESS_LENGTH):
            errors.append(err)
    if data.get('trustpilot_url'):
        if err := _validate_url(data['trustpilot_url'], 'trustpilot_url'):
            errors.append(err)
    if data.get('bbb_url'):
        if err := _validate_url(data['bbb_url'], 'bbb_url'):
            errors.append(err)
    if data.get('yelp_url'):
        if err := _validate_url(data['yelp_url'], 'yelp_url'):
            errors.append(err)

    if errors:
        return jsonify({'success': False, 'error': '; '.join(errors)}), 400

    with get_session() as session:
        business = Business(
            name=data['name'].strip(),
            address=data.get('address', '').strip() or None,
            trustpilot_url=data.get('trustpilot_url') or None,
            bbb_url=data.get('bbb_url') or None,
            yelp_url=data.get('yelp_url') or None,
        )
        session.add(business)
        session.flush()

        # Auto-scrape if any review sources are configured
        new_reviews = 0
        failed_sources = []
        has_sources = business.trustpilot_url or business.bbb_url or business.yelp_url
        if has_sources:
            new_reviews, failed_sources = scrape_business_sources(
                session, business, send_alerts=False
            )

        return jsonify({
            'success': True,
            'business': {
                'id': business.id,
                'name': business.name
            },
            'initial_scrape': {
                'new_reviews': new_reviews,
                'failed_sources': failed_sources if failed_sources else None
            } if has_sources else None
        })


@bp.route('/api/business/<int:business_id>', methods=['GET'])
def api_get_business(business_id):
    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return jsonify({'success': False, 'error': 'Business not found'}), 404

        return jsonify({
            'success': True,
            'business': {
                'id': business.id,
                'name': business.name,
                'address': business.address,
                'trustpilot_url': business.trustpilot_url,
                'bbb_url': business.bbb_url,
                'yelp_url': business.yelp_url,
                'google_place_id': business.google_place_id,
                'yelp_business_id': business.yelp_business_id,
            }
        })


@bp.route('/api/business/<int:business_id>', methods=['PUT'])
def api_update_business(business_id):
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Validate inputs
    errors = []
    if 'name' in data:
        if err := _validate_string(data['name'], 'name', MAX_NAME_LENGTH):
            errors.append(err)
        elif not data['name'] or not data['name'].strip():
            errors.append('name cannot be empty')
    if 'address' in data:
        if err := _validate_string(data['address'], 'address', MAX_ADDRESS_LENGTH):
            errors.append(err)
    if 'trustpilot_url' in data and data['trustpilot_url']:
        if err := _validate_url(data['trustpilot_url'], 'trustpilot_url'):
            errors.append(err)
    if 'bbb_url' in data and data['bbb_url']:
        if err := _validate_url(data['bbb_url'], 'bbb_url'):
            errors.append(err)
    if 'yelp_url' in data and data['yelp_url']:
        if err := _validate_url(data['yelp_url'], 'yelp_url'):
            errors.append(err)

    if errors:
        return jsonify({'success': False, 'error': '; '.join(errors)}), 400

    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return jsonify({'success': False, 'error': 'Business not found'}), 404

        if 'name' in data:
            business.name = data['name'].strip()
        if 'address' in data:
            business.address = data['address'].strip() if data['address'] else None
        if 'trustpilot_url' in data:
            business.trustpilot_url = data['trustpilot_url'] or None
        if 'bbb_url' in data:
            business.bbb_url = data['bbb_url'] or None
        if 'yelp_url' in data:
            business.yelp_url = data['yelp_url'] or None
        if 'google_place_id' in data:
            business.google_place_id = data['google_place_id'] or None
        if 'yelp_business_id' in data:
            business.yelp_business_id = data['yelp_business_id'] or None

        return jsonify({'success': True})


@bp.route('/api/business/<int:business_id>', methods=['DELETE'])
def api_delete_business(business_id):
    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return jsonify({'success': False, 'error': 'Business not found'}), 404

        session.delete(business)
        return jsonify({'success': True})


@bp.route('/api/business/<int:business_id>/alerts', methods=['GET'])
def api_list_alerts(business_id):
    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return jsonify({'success': False, 'error': 'Business not found'}), 404

        alerts = session.query(AlertConfig).filter(
            AlertConfig.business_id == business_id
        ).all()

        return jsonify({
            'success': True,
            'alerts': [{
                'id': a.id,
                'email': a.email,
                'negative_threshold': a.negative_threshold,
                'enabled': a.enabled,
            } for a in alerts]
        })


@bp.route('/api/business/<int:business_id>/alerts', methods=['POST'])
def api_create_alert(business_id):
    data = request.get_json()
    if not data or not data.get('email'):
        return jsonify({'success': False, 'error': 'Email is required'}), 400

    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return jsonify({'success': False, 'error': 'Business not found'}), 404

        existing = session.query(AlertConfig).filter(
            AlertConfig.business_id == business_id,
            AlertConfig.email == data['email']
        ).first()

        if existing:
            return jsonify({'success': False, 'error': 'Alert for this email already exists'}), 400

        alert = AlertConfig(
            business_id=business_id,
            email=data['email'],
            alert_on_negative=True,
            negative_threshold=float(data.get('negative_threshold', 3.0)),
            enabled=data.get('enabled', True),
        )
        session.add(alert)
        session.flush()

        return jsonify({
            'success': True,
            'alert': {
                'id': alert.id,
                'email': alert.email,
                'negative_threshold': alert.negative_threshold,
                'enabled': alert.enabled,
            }
        })


@bp.route('/api/alerts/<int:alert_id>', methods=['PUT'])
def api_update_alert(alert_id):
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    with get_session() as session:
        alert = session.query(AlertConfig).get(alert_id)
        if not alert:
            return jsonify({'success': False, 'error': 'Alert not found'}), 404

        if 'email' in data:
            alert.email = data['email']
        if 'negative_threshold' in data:
            alert.negative_threshold = float(data['negative_threshold'])
        if 'enabled' in data:
            alert.enabled = data['enabled']

        return jsonify({'success': True})


@bp.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
def api_delete_alert(alert_id):
    with get_session() as session:
        alert = session.query(AlertConfig).get(alert_id)
        if not alert:
            return jsonify({'success': False, 'error': 'Alert not found'}), 404

        session.delete(alert)
        return jsonify({'success': True})


@bp.route('/business/<int:business_id>/export')
def export_reviews(business_id):
    with get_session() as session:
        business = session.query(Business).get(business_id)
        if not business:
            return "Business not found", 404

        source = request.args.get('source', '')
        sentiment = request.args.get('sentiment', '')

        query = session.query(Review).filter(Review.business_id == business_id)

        if source:
            query = query.filter(Review.source == source)
        if sentiment:
            query = query.filter(Review.sentiment_label == sentiment)

        reviews = query.order_by(Review.scraped_at.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['source', 'author', 'rating', 'text', 'date', 'sentiment_score', 'sentiment_label'])

        for r in reviews:
            writer.writerow([
                r.source,
                r.author_name,
                r.rating,
                r.text,
                r.review_date,
                r.sentiment_score,
                r.sentiment_label,
            ])

        output.seek(0)
        safe_name = business.name.lower().replace(' ', '_')
        filename = f"{safe_name}_reviews.csv"

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )


# Settings Routes

def __get_sentiment_config(session):
    """Get or create sentiment config with defaults."""
    config = session.query(SentimentConfig).first()
    if not config:
        config = SentimentConfig(
            rating_weight=Config.SENTIMENT_RATING_WEIGHT,
            text_weight=Config.SENTIMENT_TEXT_WEIGHT,
            threshold=Config.SENTIMENT_THRESHOLD,
        )
        session.add(config)
        session.flush()
    return config


@bp.route('/settings')
def settings():
    with get_session() as session:
        configs = session.query(APIConfig).all()
        api_keys = {c.provider: {'enabled': c.enabled, 'key_preview': APIConfig.mask_key(c.api_key)} for c in configs}
        sentiment_config = _get_sentiment_config(session)
        return render_template('settings.html', api_keys=api_keys, sentiment_config=sentiment_config)


@bp.route('/api/settings/api-keys', methods=['GET'])
def api_get_api_keys():
    with get_session() as session:
        configs = session.query(APIConfig).all()
        return jsonify({
            'success': True,
            'api_keys': {
                c.provider: {
                    'enabled': c.enabled,
                    'key_preview': APIConfig.mask_key(c.api_key)
                } for c in configs
            }
        })


@bp.route('/api/settings/api-keys', methods=['POST'])
def api_save_api_key():
    data = request.get_json()
    if not data or not data.get('provider') or not data.get('api_key'):
        return jsonify({'success': False, 'error': 'Provider and api_key are required'}), 400

    provider = data['provider']
    if provider not in ('google_places', 'yelp_fusion'):
        return jsonify({'success': False, 'error': 'Invalid provider'}), 400

    with get_session() as session:
        config = session.query(APIConfig).filter(APIConfig.provider == provider).first()

        if config:
            config.api_key = data['api_key']
            config.enabled = data.get('enabled', True)
        else:
            config = APIConfig(
                provider=provider,
                api_key=data['api_key'],
                enabled=data.get('enabled', True)
            )
            session.add(config)

        session.flush()
        return jsonify({
            'success': True,
            'api_key': {
                'provider': config.provider,
                'enabled': config.enabled,
                'key_preview': APIConfig.mask_key(config.api_key)
            }
        })


@bp.route('/api/settings/api-keys/<provider>', methods=['DELETE'])
def api_delete_api_key(provider):
    if provider not in ('google_places', 'yelp_fusion'):
        return jsonify({'success': False, 'error': 'Invalid provider'}), 400

    with get_session() as session:
        config = session.query(APIConfig).filter(APIConfig.provider == provider).first()
        if not config:
            return jsonify({'success': False, 'error': 'API key not found'}), 404

        session.delete(config)
        return jsonify({'success': True})


@bp.route('/api/settings/api-keys/<provider>/toggle', methods=['POST'])
def api_toggle_api_key(provider):
    if provider not in ('google_places', 'yelp_fusion'):
        return jsonify({'success': False, 'error': 'Invalid provider'}), 400

    with get_session() as session:
        config = session.query(APIConfig).filter(APIConfig.provider == provider).first()
        if not config:
            return jsonify({'success': False, 'error': 'API key not found'}), 404

        config.enabled = not config.enabled
        return jsonify({
            'success': True,
            'enabled': config.enabled
        })


@bp.route('/api/settings/sentiment', methods=['GET'])
def api_get_sentiment_settings():
    """Get current sentiment analysis settings."""
    with get_session() as session:
        config = _get_sentiment_config(session)
        return jsonify({
            'success': True,
            'sentiment': {
                'rating_weight': config.rating_weight,
                'text_weight': config.text_weight,
                'threshold': config.threshold,
            }
        })


@bp.route('/api/settings/sentiment', methods=['POST'])
def api_save_sentiment_settings():
    """Save sentiment analysis settings."""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    rating_weight = data.get('rating_weight')
    text_weight = data.get('text_weight')
    threshold = data.get('threshold')

    # Validate weights are between 0 and 1
    for name, value in [('rating_weight', rating_weight), ('text_weight', text_weight), ('threshold', threshold)]:
        if value is not None and (value < 0 or value > 1):
            return jsonify({'success': False, 'error': f'{name} must be between 0 and 1'}), 400

    with get_session() as session:
        config = _get_sentiment_config(session)

        if rating_weight is not None:
            config.rating_weight = rating_weight
        if text_weight is not None:
            config.text_weight = text_weight
        if threshold is not None:
            config.threshold = threshold

        return jsonify({
            'success': True,
            'sentiment': {
                'rating_weight': config.rating_weight,
                'text_weight': config.text_weight,
                'threshold': config.threshold,
            }
        })


# API Platform Search Routes

@bp.route('/api/search-google-places', methods=['POST'])
def api_search_google_places():
    """Search Google Places API for businesses."""
    data = request.get_json()
    if not data or not data.get('query'):
        return jsonify({'success': False, 'error': 'Query is required'}), 400

    with get_session() as session:
        config = get_api_config(session, 'google_places')
        if not config:
            return jsonify({'success': False, 'error': 'Google Places API key not configured'}), 400

        scraper = GooglePlacesScraper(config.api_key)
        results = scraper.search(data['query'], data.get('location'))

        return jsonify({
            'success': True,
            'results': results
        })


@bp.route('/api/search-yelp', methods=['POST'])
def api_search_yelp():
    """Search Yelp Fusion API for businesses."""
    data = request.get_json()
    if not data or not data.get('query'):
        return jsonify({'success': False, 'error': 'Query is required'}), 400

    with get_session() as session:
        config = get_api_config(session, 'yelp_fusion')
        if not config:
            return jsonify({'success': False, 'error': 'Yelp Fusion API key not configured'}), 400

        scraper = YelpAPIScraper(config.api_key)
        results = scraper.search(data['query'], data.get('location'))

        return jsonify({
            'success': True,
            'results': results
        })
