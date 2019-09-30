from typing import Dict

import requests
from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_restplus import Api, Resource

oauth = Blueprint("oauth", __name__)
api = Api(oauth)

JSONData = Dict[str, str]


def get_token(code: str) -> JSONData:
    data = {
        "grant_type": "authorization_code",
        "client_id": app.config["CLIENT_ID"],
        "client_secret": app.config["CLIENT_SECRET"],
        "redirect_uri": request.base_url,
        "code": code,
    }
    response = requests.post(app.config["TOKEN_URL"], data=data)
    # TODO: check post success
    response.raise_for_status()

    return response.json()


def list_contacts(access_token: str) -> JSONData:
    headers = {
        "Authorization": f"Bearer {access_token}",
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
    def get(self):
        # TODO: check if not code is sent
        print(request.args)
        code = request.args["code"]

        token = get_token(code)
        print(list_contacts(token["access_token"]))

        return {"msg": "ok"}
