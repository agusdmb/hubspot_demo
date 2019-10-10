from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class UserModel(db.Model):  # type: ignore
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128))
    refresh_token = db.Column(db.String(300), unique=True)
    access_token = db.Column(db.String(300))
    deals = relationship("DealModel")


class DealModel(db.Model):  # type: ignore
    __tablename__ = "deal"
    deal_id = db.Column(db.Integer, primary_key=True)
    properties = db.Column(db.JSON)
    user = db.Column(db.Integer, db.ForeignKey("user.user_id"))
