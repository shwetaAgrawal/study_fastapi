"""Test the hello_fastapi application using FastAPI TestClient."""

import pytest
from BaseTestFastAPI import BaseTestFastAPI

from study_fastapi.hello_fastapi import app, get_greeting_message


@pytest.fixture(scope="class")
def app_client(app_client_factory):
    yield app_client_factory(app)


class TestHelloFastAPI(BaseTestFastAPI):
    """Test cases for the hello_fastapi application."""

    _STATIC_GREETING = "Hello, World!"
    _PERSONALIZED_GREETING = "Hello, shweta!"

    @pytest.mark.parametrize(
        "path, expected_greeting",
        [
            ("/hi", _STATIC_GREETING),
            ("/hi_name/shweta", _PERSONALIZED_GREETING),
            ("/hello?name=shweta", _PERSONALIZED_GREETING),
            ("/hello?name=", _STATIC_GREETING),
        ],
    )
    def test_get_success(self, app_client, path, expected_greeting):
        """Test successful GET requests."""
        response = app_client.get(path)
        self._validate_response(response, self.SUCCESS_STATUS, expected_greeting)

    @pytest.mark.parametrize(
        "path, request_body, request_header, expected_greeting",
        [
            ("/hello", {"name": "shweta"}, None, _PERSONALIZED_GREETING),
            ("/hello_header", None, {"name": "shweta"}, _PERSONALIZED_GREETING),
            ("/hello_header", None, {"NAME": "shweta"}, _PERSONALIZED_GREETING),
        ],
    )
    def test_post_success(self, app_client, path, request_body, request_header, expected_greeting):
        """Test successful POST requests."""
        response = app_client.post(path, json=request_body, headers=request_header)
        self._validate_response(response, self.SUCCESS_STATUS, expected_greeting)

    def test_get_greeting_message(self):
        """Test the get_greeting_message function."""
        assert get_greeting_message("shweta") == self._PERSONALIZED_GREETING
        assert get_greeting_message() == self._STATIC_GREETING

    @pytest.mark.parametrize(
        "path, expected_status",
        [
            ("/hi_name/", 404),
            ("/hello", 422),
        ],
    )
    def test_get_error(self, app_client, path, expected_status):
        response = app_client.get(path)
        expected_json = self.ERR_JSON_404 if expected_status == 404 else self._get_err_422("query")
        self._validate_response(response, expected_status, expected_json)

    def test_hello_post_error(self, app_client):
        """Test the /hello endpoint with POST method."""
        response = app_client.post("/hello", json={})
        self._validate_response(response, 422, self._get_err_422("body"))

    def test_hello_header_post_error(self, app_client):
        """Test the /hello endpoint with POST method."""
        response = app_client.post("/hello_header", headers={})
        self._validate_response(response, 422, self._get_err_422("header"))
