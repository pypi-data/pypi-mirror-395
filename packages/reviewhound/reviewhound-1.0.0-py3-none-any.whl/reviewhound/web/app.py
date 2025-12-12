from flask import Flask
from reviewhound.config import Config
from reviewhound.database import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = Config.FLASK_SECRET_KEY

    with app.app_context():
        init_db()

    from reviewhound.web import routes
    app.register_blueprint(routes.bp)

    return app
