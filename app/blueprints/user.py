from typing import Any, Dict

from flask import Blueprint
from flask_restplus import Api, Resource, abort

from app.user import User, UserException

user = Blueprint("user", __name__)
api = Api(user)

JSONData = Dict[str, Any]


@api.route("/user")
class UserList(Resource):
    def get(self) -> JSONData:
        """
        Retrieve all users.
        """
        users = User.get_all()
        return {"users": [user.data for user in users]}


@api.route("/user/<string:user_id>")
class UserResource(Resource):
    def get(self, user_id: str) -> JSONData:  # type: ignore
        """
        Retrieve a user by its id.
        """
        user = User.get(user_id)
        if user:
            return user.data
        abort(404, "User not found")


@api.route("/user/<string:user_id>/refresh")
class UserRefresh(Resource):
    def get(self, user_id: str) -> JSONData:  # type: ignore
        """
        Refresh a user token.
        """
        user = User.get(user_id)
        if user:
            try:
                user.refresh_token()
                return user.data
            except UserException:
                abort(500, "Couldn't refresh token")
        abort(404, "User not found")
