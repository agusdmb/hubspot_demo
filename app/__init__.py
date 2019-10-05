from typing import Any, Dict

from flask import Flask
from flask_migrate import Migrate

from app.blueprints import ACTIVE
from app.models import db


def create_app(config: Dict[str, Any] = None) -> Flask:
    app = Flask(__name__)

    app.config.from_object("app.config")
    if config:
        app.config.update(config)

    for url, blueprint in ACTIVE:
        app.register_blueprint(blueprint, url_prefix=url)

    db.init_app(app)
    Migrate(app, db)

    return app
