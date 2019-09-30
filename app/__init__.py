from flask import Flask

from app.blueprints import ACTIVE


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config")

    for url, blueprint in ACTIVE:
        app.register_blueprint(blueprint, url_prefix=url)

    return app
