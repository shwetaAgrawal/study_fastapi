import pytest
from BaseTestFastAPI import BaseTestFastAPI

from study_fastapi.a2_fastapi_header import app


@pytest.fixture(scope="class")
def app_client(app_client_factory):
    yield app_client_factory(app)


class TestFastAPIHeader(BaseTestFastAPI):
    _DEFAULT_USER_AGENT = "testclient"
    _CUSTOM_USER_AGENT_HEADER = {"User-Agent": "Dummy user agent header"}
    _SUCCESS_RESPONSE = "Hello, shweta!"

    def test_agent_default_header(self, app_client):
        """Test successful GET requests."""
        response = app_client.get("/useragent")
        self._validate_response(response, self.SUCCESS_STATUS, self._DEFAULT_USER_AGENT)

    def test_agent_custom_header(self, app_client):
        """Test failed GET requests."""
        response = app_client.get("/useragent", headers=self._CUSTOM_USER_AGENT_HEADER)
        self._validate_response(
            response, self.SUCCESS_STATUS, self._CUSTOM_USER_AGENT_HEADER["User-Agent"]
        )

    def test_get_params_path(self, app_client):
        """Test GET request with path parameters."""
        # By default for a get method it assumes query parameters
        # 404 error is returned by the below URL
        response = app_client.get("/hi/shweta")
        self._validate_response(response, 404, self.ERR_JSON_404)

    def test_get_params_query(self, app_client):
        """Test GET request with query parameters."""
        response = app_client.get("/hi?name=shweta")
        self._validate_response(response, self.SUCCESS_STATUS, self._SUCCESS_RESPONSE)

    def test_post_params_body(self, app_client):
        """Test POST request with body parameters."""
        response = app_client.post("/hi_post", json={"name": "shweta"})
        self._validate_response(response, 422, self._get_err_422("query"))

    def test_post_params_header(self, app_client):
        """Test POST request with header parameters."""
        response = app_client.post("/hi_post", headers={"name": "shweta"})
        self._validate_response(response, 422, self._get_err_422("query"))

    def test_post_params_query(self, app_client):
        """Test POST request with query parameters."""
        response = app_client.post("/hi_post?name=shweta")
        self._validate_response(response, self.SUCCESS_STATUS, self._SUCCESS_RESPONSE)
