from typing import Any, Dict, List

import requests

from app.models import DealModel, db
from app.user import User

JSONData = Dict[str, Any]


class DealException(Exception):
    pass


class Deal:
    user_id: int
    deal_id: int
    properties: JSONData

    _BASE_URL = "https://api.hubapi.com/deals/v1/deal/{deal_id}"
    PROPERTIES = ["dealname", "dealstage", "closedate", "amount", "dealtype"]

    def __init__(self, deal_id: int, user_id: int, properties: JSONData) -> None:
        self.deal_id = deal_id
        self.user_id = user_id
        self.properties = properties

    @classmethod
    def from_api(cls, deal_id: int, user: User) -> "Deal":
        response = user.requests(cls._BASE_URL.format(deal_id=deal_id))
        if response.status_code != 200:
            raise DealException("Couldn't get deal: {deal_id}.")

        properties = {
            key: value
            for key, value in response.json()["properties"].items()
            if key in cls.PROPERTIES
        }
        deal_id = response.json()["dealId"]
        deal = cls(deal_id, user.data["user_id"], properties)
        return deal

    @classmethod
    def from_model(cls, deal_model: DealModel) -> "Deal":
        deal = cls(deal_model.deal_id, deal_model.user, deal_model.properties)
        return deal

    def save(self) -> None:
        deal_model = DealModel.query.get(self.deal_id)
        if deal_model:
            deal_model.properties = self.properties
        else:
            deal_model = DealModel(
                deal_id=self.deal_id,
                properties=self.properties,
                user=self.user_id
            )
        db.session.add(deal_model)
        db.session.commit()

    def json(self) -> JSONData:
        return {"dealId": self.deal_id, "properties": self.properties}


class Deals:
    deals: List[Deal] = []

    _BASE_URL = "https://api.hubapi.com/deals/v1/deal/paged"

    def __init__(self, deals: List[Deal]) -> None:
        self.deals = deals

    @classmethod
    def load_from_user(cls, user: User) -> "Deals":
        deal_models = DealModel.query.filter(DealModel.user == user.data["user_id"])
        deals = [Deal.from_model(deal) for deal in deal_models]
        return Deals(deals)

    @classmethod
    def fetch_from_user(cls, user: User) -> "Deals":
        # TODO: paging limit default 100
        response = user.requests(cls._BASE_URL)
        response.raise_for_status()
        deals: List[Deal] = []
        for deal in response.json()["deals"]:
            deals.append(Deal.from_api(deal["dealId"], user))
        return Deals(deals)
