from typing import Any, Dict

from flask import Blueprint, request
from flask_restplus import Api, Resource

from app.user import User

oauth = Blueprint("oauth", __name__)
api = Api(oauth)

JSONData = Dict[str, Any]


@api.route("/auth_callback")
class AuthCallback(Resource):
    def get(self) -> JSONData:
        """
        Callback endpoint for HubSpot integration.
        """
        # TODO: check if not code is sent
        code = request.args["code"]

        user = User.from_code(code, request.base_url)
        user.save()

        return {"msg": "App installed correctly."}
