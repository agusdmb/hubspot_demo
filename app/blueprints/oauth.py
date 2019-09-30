import requests
from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_restplus import Api, Resource

oauth = Blueprint("oauth", __name__)
api = Api(oauth)


@api.route("/auth_callback")
class AuthCallback(Resource):
    def get(self):
        # TODO: check if not code is sent
        code = request.args["code"]
        data = {
            "grant_type": "authorization_code",
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "redirect_uri": request.base_url,
            "code": code,
        }
        # TODO: check post success
        response = requests.post(app.config["TOKEN_URL"], data=data)
        print(response.json())
        response.raise_for_status()
        return {"msg": "ok"}
