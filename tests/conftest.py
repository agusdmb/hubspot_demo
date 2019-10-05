import pytest
from flask import Flask

from app import create_app
from app.models import db


@pytest.fixture  # type: ignore
def client() -> Flask:
    app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite://"})
    with app.app_context():
        db.create_all()
        yield app.test_client()


@pytest.fixture(autouse=True)
def use_requests_mock(requests_mock):
    pass
