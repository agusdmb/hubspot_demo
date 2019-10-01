from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AccessToken(db.Model):  # type: ignore
    __tablename__ = "access_token"
    refresh_token = db.Column(db.String(300), primary_key=True)
    access_token = db.Column(db.String(300))
    expires_in = db.Column(db.Integer)
    last_updated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(db.Model):  # type: ignore
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128))
