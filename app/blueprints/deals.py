from typing import Any, Dict

import requests
from flask import Blueprint
from flask import request
from flask_restplus import Api, Resource

from app.token import Token

deals = Blueprint("deals", __name__)
api = Api(deals)

JSONData = Dict[str, Any]


@api.route("/")
class DealsList(Resource):
    def get(self):

        return {"msg": "ok"}
