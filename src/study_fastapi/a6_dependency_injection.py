"""FastAPI dependency injection examples.

This module demonstrates:
- Injecting query parameters via Depends for greeting
- Injecting and requiring a header via Depends
- Parsing and validating pagination params via a dependency
"""

from typing import Annotated

from fastapi import Depends, FastAPI, Header, Query

app = FastAPI()


def get_name(name: Annotated[str | None, Query()] = None) -> str | None:
    """Dependency to retrieve optional name from query params."""
    return name


@app.get("/di/hello")
def hello(name: Annotated[str | None, Depends(get_name)] = None) -> str:
    """Return a greeting using a dependency-injected name param."""
    return f"Hello, {name}!" if name else "Hello, World!"


def get_token(x_token: Annotated[str, Header()]):
    """Require an X-Token header via dependency.

    Using parameter name `x_token` ensures the header validation location
    appears as header/x-token when missing.
    """
    return x_token


@app.get("/di/secure")
def secure(_: Annotated[str, Depends(get_token)]):
    """Return OK only when the required header is present."""
    return {"ok": True}


def get_pagination(
    limit: Annotated[int, Query(gt=0)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    """Dependency to parse and validate pagination parameters."""
    return {"limit": limit, "offset": offset}


@app.get("/di/items")
def list_items(pagination: Annotated[dict[str, int], Depends(get_pagination)]):
    """List items using pagination parsed via dependency.

    Returns a synthetic range of integers to illustrate the behavior.
    """
    limit = pagination["limit"]
    offset = pagination["offset"]
    items = list(range(offset, offset + limit))
    return {"limit": limit, "offset": offset, "items": items}
