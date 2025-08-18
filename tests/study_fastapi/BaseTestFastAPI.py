"""Base test class for FastAPI applications."""

import copy
from abc import ABC


class BaseTestFastAPI(ABC):
    """Base class for FastAPI tests with common setup and utilities."""

    SUCCESS_STATUS = 200
    ERR_JSON_404 = {"detail": "Not Found"}
    ERR_JSON_422 = {
        "detail": [
            {
                "loc": ["tobe filled in by the test", "param_name"],
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

    def _get_err_422(self, param_type):
        response_json = copy.deepcopy(self.ERR_JSON_422)
        response_json["detail"][0]["loc"][0] = param_type
        response_json["detail"][0]["loc"][1] = "name"
        return response_json
