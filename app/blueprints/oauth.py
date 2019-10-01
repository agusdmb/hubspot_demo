from typing import Any, Dict, List

import requests
from flask import Blueprint, request
from flask_restplus import Api, Resource, abort

from app.token import Token

oauth = Blueprint("oauth", __name__)
api = Api(oauth)

JSONData = Dict[str, Any]


def list_contacts(token: Token) -> JSONData:
    headers = {
        "Authorization": f"Bearer {token.data['access_token']}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?count=1",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


@api.route("/auth_callback")
class AuthCallback(Resource):
    def get(self) -> JSONData:
        # TODO: check if not code is sent
        code = request.args["code"]

        token = Token.from_code(code, request.base_url)

        return token.data


@api.route("/tokens")
class TokenList(Resource):
    def get(self) -> List[JSONData]:
        tokens = Token.get_all()
        return [token.data for token in tokens]


@api.route("/tokens/refresh_token/<string:refresh_token>")
class TokenUpdate(Resource):
    def get(self, refresh_token) -> JSONData:
        token = Token.from_refresh_token(refresh_token)

        if token is None:
            abort(404, f"refresh_token: {refresh_token} not found")

        token = token.refresh_token()
        return token.data
