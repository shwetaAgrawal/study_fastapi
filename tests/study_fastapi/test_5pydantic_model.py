"""Explore pydantic model validations."""

from copy import deepcopy
from typing import Any

import pytest
from BaseTestFastAPI import BaseTestFastAPI
from pydantic_core import ValidationError

from study_fastapi.a5_pydantic_model import Buyer, Seller, app


@pytest.fixture(scope="class")
def app_client(app_client_factory):
    yield app_client_factory(app)


class TestPydanticModel(BaseTestFastAPI):
    _BUYERS_RESPONSE = [
        {"name": "Shweta", "country": "IN", "zipcode": "560035"},
        {"name": "Bob", "country": "US", "zipcode": "99001"},
    ]
    _SELLERS_RESPONSE = [
        {
            "name": "Share Exports",
            "country": "CN",
            "shipping_port": "Guangdong",
            "shop_description": "Electronics Seller",
            "aka": "Share Guangdong Exports",
        },
        {
            "name": "Tirupati Mills",
            "country": "IN",
            "shipping_port": "Chennai",
            "shop_description": "Apparels seller",
            "aka": "Tirupati handwoven factory",
        },
    ]

    def _validation_error_val(self, fields: dict[str, Any]) -> list[dict[str, Any]]:
        error_dict = {
            "type": "missing",
            "loc": ("name",),
            "msg": "Field required",
            "input": {},
        }
        error_list = []
        for field in fields:
            error = deepcopy(error_dict)
            error["loc"] = (field,)
            field_dict = fields[field]
            if "type" in field_dict:
                error["type"] = field_dict["type"]
            if "msg" in field_dict:
                error["msg"] = field_dict["msg"]
            if "input" in field_dict:
                error["input"] = field_dict["input"]
            if "ctx" in field_dict:
                error["ctx"] = field_dict["ctx"]
            error_list.append(error)
        return error_list

    def _validate_error(self, expected_error_count: int, expected_errors: list[Any], exc):
        assert exc.value.error_count() == expected_error_count
        for idx, error in enumerate(exc.value.errors()):
            for field in expected_errors[idx]:
                assert field in error
                assert error[field] == expected_errors[idx][field]

    def test_sellers_success(self, app_client):
        """Test successful GET requests for /seller."""
        response = app_client.get("/sellers")
        self._validate_response(response, self.SUCCESS_STATUS, self._SELLERS_RESPONSE)

    def test_buyers_success(self, app_client):
        """Test successful GET requests for /buyer."""
        response = app_client.get("/buyers")
        self._validate_response(response, self.SUCCESS_STATUS, self._BUYERS_RESPONSE)

    def test_buyer_model_error(self):
        """Testing pydantic error for buyer model"""
        with pytest.raises(ValidationError) as exc:
            _ = Buyer()
        expected_errors = self._validation_error_val({"name": {}, "country": {}, "zipcode": {}})
        self._validate_error(3, expected_errors, exc)

    def test_seller_model_error(self):
        """Testing pydantic error for buyer model"""
        with pytest.raises(ValidationError) as exc:
            _ = Seller()
        expected_errors = self._validation_error_val(
            {"name": {}, "country": {}, "shipping_port": {}, "shop_description": {}, "aka": {}}
        )
        self._validate_error(5, expected_errors, exc)

    def test_buyer_constr_error(self):
        """Testing pydantic error for buyer model - string pattern not matching."""
        with pytest.raises(ValidationError) as exc:
            _ = Buyer(name="Shweta", country="India", zipcode="560035")

        expected_errors = self._validation_error_val(
            {
                "country": {
                    "type": "string_too_long",
                    "msg": "String should have at most 2 characters",
                    "input": "India",
                    "ctx": {"max_length": 2},
                }
            }
        )
        self._validate_error(1, expected_errors, exc)

    def test_seller_constr_error(self):
        """Testing pydantic error for buyer model - string pattern not matching."""
        with pytest.raises(ValidationError) as exc:
            _ = Seller(
                name="Share Exports",
                country="China",
                shipping_port="Guangdong",
                shop_description="Electronics Seller",
                aka="Share Guangdong Exports",
            )
        expected_errors = self._validation_error_val(
            {
                "country": {
                    "type": "string_too_long",
                    "msg": "String should have at most 2 characters",
                    "input": "China",
                    "ctx": {"max_length": 2},
                }
            }
        )
        self._validate_error(1, expected_errors, exc)

    def test_buyer_field_missing_error(self):
        """Testing pydantic error for buyer model - string pattern not matching."""
        with pytest.raises(ValidationError) as exc:
            _ = Buyer(country="IN", zipcode="560035")
        expected_errors = self._validation_error_val(
            {
                "name": {
                    "type": "missing",
                    "msg": "Field required",
                    "input": {"country": "IN", "zipcode": "560035"},
                }
            }
        )
        self._validate_error(1, expected_errors, exc)

    def test_seller_field_missing_error(self):
        """Testing pydantic error for buyer model - string pattern not matching."""
        with pytest.raises(ValidationError) as exc:
            _ = Seller(
                name="Share Exports",
                country="CN",
                shipping_port="Guangdong",
                shop_description="Electronics Seller",
            )
        expected_errors = self._validation_error_val(
            {
                "aka": {
                    "type": "missing",
                    "msg": "Field required",
                    "input": {
                        "name": "Share Exports",
                        "country": "CN",
                        "shipping_port": "Guangdong",
                        "shop_description": "Electronics Seller",
                    },
                }
            }
        )
        self._validate_error(1, expected_errors, exc)

    def test_buyer_typemismatch_error(self):
        """Testing pydantic error for buyer model - string pattern not matching."""
        with pytest.raises(ValidationError) as exc:
            _ = Buyer(name="Shweta", country="IN", zipcode=560035)
        expected_errors = self._validation_error_val(
            {
                "zipcode": {
                    "type": "string_type",
                    "msg": "Input should be a valid string",
                    "input": 560035,
                }
            }
        )
        self._validate_error(1, expected_errors, exc)

    def test_seller_typemismatch_error(self):
        """Testing pydantic error for buyer model - string pattern not matching."""
        with pytest.raises(ValidationError) as exc:
            _ = Seller(
                name="Share Exports",
                country="CN",
                shipping_port="Guangdong",
                shop_description=12,
                aka="Share Guangdong Exports",
            )
        expected_errors = self._validation_error_val(
            {
                "shop_description": {
                    "type": "string_type",
                    "msg": "Input should be a valid string",
                    "input": 12,
                }
            }
        )
        self._validate_error(1, expected_errors, exc)
