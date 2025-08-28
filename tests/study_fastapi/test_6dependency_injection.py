"""Tests for FastAPI dependency injection examples.

### Proposed Test Cases
- GET /di/hello uses a dependency to read optional query param `name` and returns greeting
  - no name -> "Hello, World!"
  - name provided -> "Hello, <name>!"
- GET /di/secure requires header dependency `X-Token`
  - missing header -> 422 with header/x-token location
  - present header -> 200 and ok: true
- GET /di/items uses a dependency that parses pagination from query with validation
  - valid cases (parametrized): returns items range and echoes limit/offset
  - invalid cases (parametrized): 422 for limit<=0 or offset<0 with correct error locations
"""

from typing import Any

import pytest
from BaseTestFastAPI import BaseTestFastAPI

from study_fastapi.a6_dependency_injection import app


@pytest.fixture(scope="class")
def app_client(app_client_factory):
    yield app_client_factory(app)


class TestDependencyInjection(BaseTestFastAPI):
    def test_hello_dependency_default(self, app_client):
        response = app_client.get("/di/hello")
        self._validate_response(response, self.SUCCESS_STATUS, "Hello, World!")

    def test_hello_dependency_with_name(self, app_client):
        response = app_client.get("/di/hello?name=shweta")
        self._validate_response(response, self.SUCCESS_STATUS, "Hello, shweta!")

    def test_secure_missing_header(self, app_client):
        response = app_client.get("/di/secure")
        # Expect a 422 because required header is missing
        assert response.status_code == 422
        body = response.json()
        assert isinstance(body, dict)
        assert body.get("detail")
        first = body["detail"][0]
        # Ensure the validation error points to header/x-token
        assert first["loc"][0] == "header"
        assert first["loc"][-1] == "x-token"  # normalized header name

    def test_secure_with_header(self, app_client):
        response = app_client.get("/di/secure", headers={"X-Token": "secrettoken"})
        assert response.status_code == self.SUCCESS_STATUS
        body = response.json()
        assert isinstance(body, dict)
        assert body.get("ok") is True

    @pytest.mark.parametrize(
        "limit,offset",
        [
            (1, 0),
            (3, 2),
            (5, 5),
        ],
        ids=["limit1_off0", "limit3_off2", "limit5_off5"],
    )
    def test_items_pagination_valid(self, app_client, limit: int, offset: int):
        response = app_client.get(f"/di/items?limit={limit}&offset={offset}")
        assert response.status_code == self.SUCCESS_STATUS
        body: dict[str, Any] = response.json()
        assert body["limit"] == limit
        assert body["offset"] == offset
        assert isinstance(body["items"], list)
        assert len(body["items"]) == limit
        assert body["items"][0] == offset
        # spot check last element
        assert body["items"][-1] == offset + limit - 1

    @pytest.mark.parametrize(
        "query,loc_name",
        [
            ("limit=0&offset=0", "limit"),
            ("limit=-1&offset=0", "limit"),
            ("limit=10&offset=-1", "offset"),
        ],
        ids=["limit0", "limit-1", "offset-1"],
    )
    def test_items_pagination_invalid(self, app_client, query: str, loc_name: str):
        response = app_client.get(f"/di/items?{query}")
        assert response.status_code == 422
        body = response.json()
        assert body["detail"][0]["loc"][0] == "query"
        assert body["detail"][0]["loc"][1] == loc_name
