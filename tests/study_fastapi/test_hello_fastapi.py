"""Test the hello_fastapi application using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient

from study_fastapi.hello_fastapi import app, get_greeting_message


@pytest.fixture(scope="module")
def app_client():
    with TestClient(app) as c:
        yield c


class TestHelloFastAPI:
    """Test cases for the hello_fastapi application."""

    STATIC_GREETING = "Hello, World!"
    PERSONALIZED_GREETING = "Hello, shweta!"
    SUCCESS_STATUS = 200
    ERR_JSON_404 = {"detail": "Not Found"}
    ERR_JSON_422 = {
        "detail": [
            {
                "loc": ["tobe filled in by the test", "name"],
                "msg": "Field required",
                "type": "missing",
                "input": None,
            }
        ]
    }

    def _validate_response(self, response, expected_status, expected_json):
        """Helper method to validate response."""
        assert response.status_code == expected_status
        assert response.json() == expected_json
        assert response.headers["content-type"] == "application/json"

    def test_get_greeting_message(self):
        """Test the get_greeting_message function."""
        assert get_greeting_message("shweta") == self.PERSONALIZED_GREETING
        assert get_greeting_message() == self.STATIC_GREETING

    def test_hi_success(self, app_client):
        """Test the /hi endpoint."""
        response = app_client.get("/hi")
        self._validate_response(response, self.SUCCESS_STATUS, self.STATIC_GREETING)

    def test_hi_name_success(self, app_client):
        """Test the /hi_name/{name} endpoint."""
        response = app_client.get("/hi_name/shweta")
        self._validate_response(response, self.SUCCESS_STATUS, self.PERSONALIZED_GREETING)

    def test_hi_name_error(self, app_client):
        """Test the /hi_name/{name} endpoint."""
        response = app_client.get("/hi_name/")
        self._validate_response(response, 404, self.ERR_JSON_404)

    def test_hello_success(self, app_client):
        """Test the /hello endpoint."""
        response = app_client.get("/hello?name=shweta")
        self._validate_response(response, self.SUCCESS_STATUS, self.PERSONALIZED_GREETING)

    def test_hello_null_name(self, app_client):
        """Test the /hello endpoint with null name query parameter."""
        response = app_client.get("/hello?name=")
        self._validate_response(response, self.SUCCESS_STATUS, self.STATIC_GREETING)

    def test_hello_error(self, app_client):
        """Test the /hello endpoint with missing name query parameter."""
        response = app_client.get("/hello")
        response_json = self.ERR_JSON_422.copy()
        response_json["detail"][0]["loc"][0] = "query"
        self._validate_response(response, 422, response_json)

    def test_hello_post_success(self, app_client):
        """Test the /hello endpoint with POST method."""
        response = app_client.post("/hello", json={"name": "shweta"})
        self._validate_response(response, self.SUCCESS_STATUS, self.PERSONALIZED_GREETING)

    def test_hello_post_error(self, app_client):
        """Test the /hello endpoint with POST method."""
        response = app_client.post("/hello", json={})
        response_json = self.ERR_JSON_422.copy()
        response_json["detail"][0]["loc"][0] = "body"
        self._validate_response(response, 422, response_json)

    def test_hello_header_post_success(self, app_client):
        """Test the /hello endpoint with POST method."""
        response = app_client.post("/hello_header", headers={"name": "shweta"})
        self._validate_response(response, self.SUCCESS_STATUS, self.PERSONALIZED_GREETING)

    def test_hello_header_post_error(self, app_client):
        """Test the /hello endpoint with POST method."""
        response = app_client.post("/hello_header", headers={})
        response_json = self.ERR_JSON_422.copy()
        response_json["detail"][0]["loc"][0] = "header"
        self._validate_response(response, 422, response_json)
