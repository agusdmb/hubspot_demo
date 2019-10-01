from typing import Any, Dict, List, Optional

import requests
from flask import current_app as app

from app.models import AccessToken, db

JSONData = Dict[str, Any]


class Token:
    data: JSONData
    _cache: Dict[str, Any] = {}

    _BASE_URL = "https://api.hubapi.com/oauth/v1"
    _TOKEN_URL = _BASE_URL + "/token"
    _INFO_TOKEN_URL = _BASE_URL + "/access-tokens/{access_token}"

    def __init__(self, data):
        self.data = data

    @staticmethod
    def from_code(code: str, base_url: str) -> "Token":
        data = {
            "grant_type": "authorization_code",
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "redirect_uri": base_url,
            "code": code,
        }
        response = requests.post(Token._TOKEN_URL, data=data)
        # TODO: check post success
        response.raise_for_status()

        token = Token(response.json()).save()
        return token

    @staticmethod
    def from_access_token(access_token: AccessToken) -> "Token":
        data = {
            "refresh_token": access_token.refresh_token,
            "access_token": access_token.access_token,
            "expires_in": access_token.expires_in,
            "last_updated": str(access_token.last_updated),
        }
        token = Token(data)
        return token

    @staticmethod
    def from_refresh_token(refresh_token: str) -> Optional["Token"]:
        access_token = AccessToken.query.get(refresh_token)
        if access_token:
            return Token.from_access_token(access_token)
        return None

    @staticmethod
    def get_all() -> List["Token"]:
        return [
            Token.from_access_token(access_token)
            for access_token in AccessToken.query.all()
        ]

    def get_token_info(self) -> JSONData:
        if "info" not in self._cache:
            url = self._INFO_TOKEN_URL.format(access_token=self.data["access_token"])
            response = requests.get(url)
            # TODO: check post success
            response.raise_for_status()
            self._cache["info"] = response.json()
        return self._cache["info"]

    def refresh_token(self) -> "Token":
        data = {
            "grant_type": "refresh_token",
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "refresh_token": self.data["refresh_token"],
        }
        response = requests.post(self._TOKEN_URL, data=data)
        # TODO: check post success
        response.raise_for_status()
        self.data = response.json()
        token = self.save()
        return token

    def save(self) -> "Token":
        access_token = AccessToken.query.get(self.data["refresh_token"])
        if access_token:
            access_token.access_token = self.data["access_token"]
            access_token.expires_in = self.data["expires_in"]
        else:
            access_token = AccessToken(
                refresh_token=self.data["refresh_token"],
                access_token=self.data["access_token"],
                expires_in=self.data["expires_in"],
            )
        db.session.add(access_token)
        db.session.commit()
        return Token.from_access_token(access_token)
