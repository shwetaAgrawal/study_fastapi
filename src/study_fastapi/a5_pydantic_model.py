"""Pydantic model exploration."""

from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

""" Important points about pydantic validation -
It checks for required fields.
It checks their datatypes and any additional constraints
It serializes data
"""


class Buyer(BaseModel):
    """Data model for enclosing buyer information."""

    name: str
    country: Annotated[
        str,
        StringConstraints(max_length=2, pattern=r"^[A-Z]{2}$"),
    ]
    zipcode: str


class Seller(BaseModel):
    """Data model for enclosing seller information."""

    name: str

    # ISO 3166-1 alpha-2 country code
    country: Annotated[
        str,
        StringConstraints(max_length=2, pattern=r"^[A-Z]{2}$"),
    ]

    shipping_port: str | None
    shop_description: str
    aka: str


_sellers: list[Seller] = [
    Seller(
        name="Share Exports",
        country="CN",
        shipping_port="Guangdong",
        shop_description="Electronics Seller",
        aka="Share Guangdong Exports",
    ),
    Seller(
        name="Tirupati Mills",
        country="IN",
        shipping_port="Chennai",
        shop_description="Apparels seller",
        aka="Tirupati handwoven factory",
    ),
]
_buyers: list[Buyer] = [
    Buyer(name="Shweta", country="IN", zipcode="560035"),
    Buyer(name="Bob", country="US", zipcode="99001"),
]

app = FastAPI()


@app.get("/sellers")
def get_sellers() -> list[Seller]:
    """Get the list of sellers."""
    return _sellers


@app.get("/buyers")
def get_buyers() -> list[Buyer]:
    """Get the list of buyers."""
    return _buyers
