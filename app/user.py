from typing import Any, Dict, List, Optional

import requests
from flask import current_app as app

from app.models import UserModel, db

JSONData = Dict[str, Any]


class UserException(Exception):
    pass


class User:
    data: JSONData
    _cache: Dict[str, Any] = {}

    _BASE_URL = "https://api.hubapi.com/oauth/v1"
    _TOKEN_URL = _BASE_URL + "/token"
    _INFO_TOKEN_URL = _BASE_URL + "/access-tokens/{access_token}"

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_code(cls, code: str, base_url: str) -> "User":
        data = cls._get_access_token(code, base_url)
        data.update(cls._get_user_info(data["access_token"]))
        user = cls(data)
        return user

    @classmethod
    def _get_access_token(cls, code: str, base_url: str) -> JSONData:
        data = {
            "grant_type": "authorization_code",
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "redirect_uri": base_url,
            "code": code,
        }
        response = requests.post(cls._TOKEN_URL, data=data)
        if response.status_code != 200:
            raise UserException(f"Couldn't get the access token for code {code}.")

        return response.json()

    @classmethod
    def _get_user_info(cls, access_token: str) -> JSONData:
        url = cls._INFO_TOKEN_URL.format(access_token=access_token)
        response = requests.get(url)
        if response.status_code != 200:
            raise UserException(
                f"Couldn't get the info for access_token: {access_token}."
            )
        return response.json()

    @staticmethod
    def user_from_model(user_model: UserModel) -> "User":
        data = {
            "user_id": user_model.user_id,
            "user": user_model.user,
            "refresh_token": user_model.refresh_token,
            "access_token": user_model.access_token,
        }
        return User(data)

    @classmethod
    def get_all(cls) -> List["User"]:
        users = UserModel.query.all()
        return [cls.user_from_model(user) for user in users]

    @classmethod
    def get(cls, user_id) -> Optional["User"]:
        user = UserModel.query.get(user_id)
        if user:
            return cls.user_from_model(user)
        return None

    def refresh_token(self) -> None:
        # TODO: check what error throws HubSpot if the token has expired.
        data = {
            "grant_type": "refresh_token",
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "refresh_token": self.data["refresh_token"],
        }
        response = requests.post(self._TOKEN_URL, data=data)
        if response.status_code != 200:
            raise UserException("Couldn't refresh token: {self.data['refresh_token']}")
        self.data.update(response.json())
        self.save()

    def save(self) -> None:
        user = UserModel.query.get(self.data["user_id"])
        if user:
            user.access_token = self.data["access_token"]
        else:
            user = UserModel(
                user_id=self.data["user_id"],
                user=self.data["user"],
                refresh_token=self.data["refresh_token"],
                access_token=self.data["access_token"],
            )
        db.session.add(user)
        db.session.commit()

    @property
    def header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.data['access_token']}"}

    def requests(self, url):
        response = requests.get(url, headers=self.header)
        if response.status_code == 401:
            self.refresh_token()
            response = requests.get(url, headers=self.header)

        response.raise_for_status()

        return response
