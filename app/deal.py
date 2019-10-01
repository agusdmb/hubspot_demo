from typing import Any, Dict, List

import requests
from flask import current_app as app

JSONData = Dict[str, Any]


class Deal:
    data: JSONData

    _BASE_URL = "https://api.hubapi.com/deals/v1/deal/paged"

    def __init__(self, token):
        headers = {
            "Authorization": f"Bearer {token.data['access_token']}",
            "Content-Type": "application/json",
        }
        # TODO: paging limit default 100
        response = requests.get(self._BASE_URL, headers=headers)
        response.raise_for_status()
        self.data = response.json()
