"""Test the async endpoints."""

import re

import pytest
from BaseTestFastAPI import BaseTestFastAPI
from httpx import ASGITransport, AsyncClient

from study_fastapi.a4_fastapi_async import app


class TestAsyncEndpoints(BaseTestFastAPI):
    @pytest.mark.asyncio
    async def test_greet(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
        ) as ac:
            response = await ac.get("/hi")
            assert response.status_code == self.SUCCESS_STATUS
            body = response.json()
            assert re.fullmatch(r"Hello, World! \(waited 1\.\d{2} seconds\)", body), body
