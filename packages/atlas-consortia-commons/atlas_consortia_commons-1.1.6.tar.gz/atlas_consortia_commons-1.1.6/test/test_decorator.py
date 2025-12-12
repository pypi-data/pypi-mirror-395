from unittest.mock import MagicMock, patch

import pytest
from flask import Flask, Response, jsonify

from atlas_consortia_commons.decorator import (
    User,
    require_data_admin,
    require_json,
    require_valid_token,
)


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.update(
        {
            "TESTING": True,
            "APP_CLIENT_ID": "test_client_id",
            "APP_CLIENT_SECRET": "test_client_secret",
        }
    )
    yield app


@pytest.fixture()
def auth_helper():
    mock = MagicMock()
    with patch(
        "hubmap_commons.hm_auth.AuthHelper.configured_instance", return_value=mock
    ):
        yield mock


def test_require_json_success(app):
    """Test that the require json decorator allows only json."""

    @app.route("/test", methods=["POST"])
    @require_json()
    def test_route(body: dict):
        return jsonify(body), 200

    body = {"key": "value"}
    with app.test_client() as client:
        res = client.post("/test", json=body)
        assert res.status_code == 200
        assert res.json == body


def test_require_json_unsuccess_content(app):
    """Test that the require json decorator doesn't allow other content types."""

    @app.route("/test", methods=["POST"])
    @require_json()
    def test_route(body: dict):
        return jsonify(body), 200

    body = {"key": "value"}
    with app.test_client() as client:
        res = client.post("/test", data=body)
        assert res.status_code == 400


def test_require_json_unsuccess_obj_type(app):
    """Test that the require json decorator doesn't allow other json object types."""

    @app.route("/test", methods=["POST"])
    @require_json()
    def test_route(body: dict):
        return jsonify(body), 200

    body = ["item1", "item2"]
    with app.test_client() as client:
        res = client.post("/test", json=body)
        assert res.status_code == 400


def test_require_valid_token_success(app, auth_helper):
    """Test that the require valid token decorator allows valid tokens."""

    token = "valid_token"
    user_id = "8cb9cda5-1930-493a-8cb9-df6742e0fb42"

    auth_helper.has_data_admin_privs.return_value = False
    auth_helper.getUserTokenFromRequest.return_value = token
    auth_helper.getUserInfo.return_value = {
        "sub": user_id,
        "email": "TESTUSER@example.com",
        "hmgroupids": ["60b692ac-8f6d-485f-b965-36886ecc5a26"],
    }

    @app.route("/test")
    @require_valid_token()
    def test_route(token: str, user: User):
        return jsonify({"token": token, "uuid": user_id}), 200

    with app.test_client() as client:
        res = client.get("/test", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert res.json.get("token") == token
        assert res.json.get("uuid") == user_id


@pytest.mark.parametrize("token", [None, "", "invalid_token"])
def test_require_valid_token_unsuccess(app, auth_helper, token):
    """Test that the require valid token decorator disallows invalid tokens."""

    auth_helper.getUserTokenFromRequest.return_value = Response()

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    @app.route("/test")
    @require_valid_token()
    def test_route(token: str, user: User):
        return jsonify({"token": token, "uuid": user}), 200

    with app.test_client() as client:
        res = client.get("/test", headers=headers)
        assert res.status_code == 401


def test_require_data_admin_success(app, auth_helper):
    """Test that the require data admin decorator allows data admin tokens."""

    token = "valid_token"
    user_id = "8cb9cda5-1930-493a-8cb9-df6742e0fb42"

    auth_helper.has_data_admin_privs.return_value = True
    auth_helper.getUserTokenFromRequest.return_value = token
    auth_helper.getUserInfo.return_value = {
        "sub": user_id,
        "email": "TESTUSER@example.com",
        "hmgroupids": ["60b692ac-8f6d-485f-b965-36886ecc5a26"],
    }

    @app.route("/test")
    @require_data_admin()
    def test_route(token: str, user: User):
        return jsonify({"token": token, "uuid": user_id}), 200

    with app.test_client() as client:
        res = client.get("/test", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert res.json.get("token") == token
        assert res.json.get("uuid") == user_id


def test_require_data_admin_unsuccess(app, auth_helper):
    """Test that the require data admin decorator disallows non data admin tokens."""

    token = "valid_token_not_data_admin"
    user_id = "8cb9cda5-1930-493a-8cb9-df6742e0fb42"

    auth_helper.getUserTokenFromRequest.return_value = token
    auth_helper.has_data_admin_privs.return_value = False

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    @app.route("/test")
    @require_valid_token()
    def test_route(token: str, user: User):
        return jsonify({"token": token, "uuid": user_id}), 200

    with app.test_client() as client:
        res = client.get("/test", headers=headers)
        assert res.status_code == 401
