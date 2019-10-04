from typing import Any, Dict, List

from flask import Blueprint, abort
from flask_restplus import Api, Resource

# from app.user import User
from app.deal import Deals
from app.user import User

deals = Blueprint("deals", __name__)
api = Api(deals)

JSONData = Dict[str, Any]


@api.route("deals/<string:user_id>")
class DealsList(Resource):
    def get(self, user_id: str) -> List[JSONData]:
        user = User.get(user_id)
        if user:
            deals = Deals.load_from_user(user)
            return [deal.json() for deal in deals.deals]
        abort(404, "User not found")


@api.route("deals/<string:user_id>/fetch")
class DealsFetch(Resource):
    def get(self, user_id: str) -> List[JSONData]:
        user = User.get(user_id)
        if user:
            deals = Deals.fetch_from_user(user)
            for deal in deals.deals:
                deal.save()
            return [deal.json() for deal in deals.deals]
        abort(404, "User not found")
