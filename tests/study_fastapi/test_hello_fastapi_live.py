"""Test the hello_fastapi application."""

import httpx
import pytest


@pytest.fixture(scope="module")
def httpx_client(uvicorn_server_factory):
    host, port = "127.0.0.1", "8001"
    app_module = "study_fastapi.hello_fastapi"
    uvicorn_server_factory(app_module, host=host, port=port)
    with httpx.Client(base_url=f"http://{host}:{port}") as client:
        yield client


def test_hi_success(httpx_client):
    """Test the /hi endpoint."""
    response = httpx_client.get("/hi")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


def test_hi_name_success(httpx_client):
    """Test the /hi_name/{name} endpoint."""
    response = httpx_client.get("/hi_name/shweta")
    assert response.status_code == 200
    assert response.json() == "Hello, shweta!"


def test_hi_name_error(httpx_client):
    """Test the /hi_name/{name} endpoint."""
    response = httpx_client.get("/hi_name/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_hello_success(httpx_client):
    """Test the /hello endpoint."""
    response = httpx_client.get("/hello?name=shweta")
    assert response.status_code == 200
    assert response.json() == "Hello, shweta!"


def test_hello_null_name(httpx_client):
    """Test the /hello endpoint with null name query parameter."""
    response = httpx_client.get("/hello?name=")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"


def test_hello_error(httpx_client):
    """Test the /hello endpoint with missing name query parameter."""
    response = httpx_client.get("/hello")
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


def test_hello_post_success(httpx_client):
    """Test the /hello endpoint with POST method."""
    response = httpx_client.post("/hello", json={"name": "shweta"})
    assert response.status_code == 200
    assert response.json() == "Hello, shweta!"


def test_hello_post_error(httpx_client):
    """Test the /hello endpoint with POST method."""
    response = httpx_client.post("/hello", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "Field required",
                "type": "missing",
                "input": None,
            }
        ]
    }


def test_hello_post_header_success(httpx_client):
    """Test the /hello endpoint with POST method."""
    response = httpx_client.post("/hello_header", headers={"name": "shweta"})
    assert response.status_code == 200
    assert response.json() == "Hello, shweta!"


def test_hello_post_header_error(httpx_client):
    """Test the /hello endpoint with POST method."""
    response = httpx_client.post("/hello_header", headers={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["header", "name"],
                "msg": "Field required",
                "type": "missing",
                "input": None,
            }
        ]
    }
