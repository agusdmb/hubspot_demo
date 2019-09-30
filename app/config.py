import os
from pathlib import Path

DEBUG = True

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"

BASE_DIR = Path(".").absolute()

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app", "token.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER_NAME = "localhost:8080"
