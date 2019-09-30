from flask import Flask

from app.blueprints import ACTIVE
from app.models import db
from flask_migrate import Migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config")

    for url, blueprint in ACTIVE:
        app.register_blueprint(blueprint, url_prefix=url)

    db.init_app(app)
    Migrate(app, db)

    return app
