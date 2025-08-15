import pytest
from BaseTestFastAPI import BaseTestFastAPI

from study_fastapi.a2_fastapi_header import app


@pytest.fixture(scope="class")
def app_client(app_client_factory):
    yield app_client_factory(app)


class TestFastAPIHeader(BaseTestFastAPI):
    _DEFAULT_USER_AGENT = "testclient"
    _CUSTOM_USER_AGENT_HEADER = {"User-Agent": "Dummy user agent header"}

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
