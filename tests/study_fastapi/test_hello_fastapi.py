"""Test the hello_fastapi application using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient

from study_fastapi.hello_fastapi import app, get_greeting_message


@pytest.fixture(scope="module")
def app_client():
    with TestClient(app) as c:
        yield c


def test_get_greeting_message():
    """Test the get_greeting_message function."""
    assert get_greeting_message("shweta") == "Hello, shweta!"
    assert get_greeting_message() == "Hello, World!"


def test_hi_success(app_client):
    """Test the /hi endpoint."""
    response = app_client.get("/hi")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


def test_hi_name_success(app_client):
    """Test the /hi_name/{name} endpoint."""
    response = app_client.get("/hi_name/shweta")
    assert response.status_code == 200
    assert response.json() == "Hello, shweta!"


def test_hi_name_error(app_client):
    """Test the /hi_name/{name} endpoint."""
    response = app_client.get("/hi_name/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_hello_success(app_client):
    """Test the /hello endpoint."""
    response = app_client.get("/hello?name=shweta")
    assert response.status_code == 200
    assert response.json() == "Hello, shweta!"


def test_hello_null_name(app_client):
    """Test the /hello endpoint with null name query parameter."""
    response = app_client.get("/hello?name=")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


def test_hello_error(app_client):
    """Test the /hello endpoint with missing name query parameter."""
    response = app_client.get("/hello")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "name"],
                "msg": "Field required",
                "type": "missing",
                "input": None,
            }
        ]
    }
