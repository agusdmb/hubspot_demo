from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AccessToken(db.Model):  # type: ignore
    __tablename__ = "access_token"
    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(300))
    access_token = db.Column(db.String(300))
    expires_in = db.Column(db.Integer)
