from typing import Any, Dict

import requests
from flask import current_app as app

from app.models import AccessToken, db

JSONData = Dict[str, Any]


class Token:
    token: JSONData
    _cache: Dict[str, Any] = {}

    def __init__(self, token):
        self.token = token

    @staticmethod
    def from_code(code: str, base_url: str) -> "Token":
        data = {
            "grant_type": "authorization_code",
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "redirect_uri": base_url,
            "code": code,
        }
        response = requests.post(app.config["TOKEN_URL"], data=data)
        # TODO: check post success
        response.raise_for_status()

        token = Token(response.json())
        return token

    def get_token_info(self) -> JSONData:
        if "info" not in self._cache:
            url = f"https://api.hubapi.com/oauth/v1/access-tokens/{self.token['access_token']}"
            response = requests.get(url)
            # TODO: check post success
            response.raise_for_status()
            self._cache["info"] = response.json()
        return self._cache["info"]

    def refresh_token(self) -> None:
        url = f"https://api.hubapi.com/oauth/v1/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "refresh_token": self.token["refresh_token"],
        }
        response = requests.post(url, data=data)
        # TODO: check post success
        response.raise_for_status()
        self.token = response.json()

    def save(self) -> None:
        access_token = AccessToken(
            refresh_token=self.token["refresh_token"],
            access_token=self.token["access_token"],
            expires_in=self.token["expires_in"],
        )
        db.session.add(access_token)
        db.session.commit()
