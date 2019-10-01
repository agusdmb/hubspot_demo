from typing import Any, Dict

import requests
from flask import Blueprint, abort, request
from flask_restplus import Api, Resource

from app.token import Token
from app.deal import Deal

deals = Blueprint("deals", __name__)
api = Api(deals)

JSONData = Dict[str, Any]


@api.route("/<string:refresh_token>")
class DealsList(Resource):
    def get(self, refresh_token) -> JSONData:
        # TODO: autorefresh token when expired
        token = Token.from_refresh_token(refresh_token)

        if token is None:
            abort(404, f"refresh_token: {refresh_token} not found")

        deal = Deal(token)

        return deal.data
