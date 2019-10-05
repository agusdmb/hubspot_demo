from typing import Any, Dict

from flask import Blueprint, request
from flask_restplus import Api, Resource, abort

from app.user import User, UserException

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

        try:
            user = User.from_code(code, request.base_url)
            user.save()
        except UserException:
            abort(500, "Couldn't get access token.")

        return {"msg": "App installed correctly."}
