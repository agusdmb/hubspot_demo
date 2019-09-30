import os


DEBUG = True

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"

SQLALCHEMY_DATABASE_URI = "sqlite:///app/token.db"

