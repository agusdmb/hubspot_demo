from app.models import UserModel


def test_oauth(client, requests_mock):
    requests_mock.post(
        "https://api.hubapi.com/oauth/v1/token", json={"access_token": "access_token"}
    )
    requests_mock.get(
        "https://api.hubapi.com/oauth/v1/access-tokens/access_token",
        json={
            "user_id": 1,
            "user": "agus",
            "refresh_token": "abc123",
            "access_token": "access_token",
        },
    )
    users = UserModel.query.all()
    assert len(users) == 0

    response = client.get("/oauth/auth_callback?code=abc123")
    assert response.status_code == 200

    users = UserModel.query.all()
    assert len(users) == 1
    assert users[0].user == "agus"
