"""Explore async request handling in FastAPI."""

import asyncio
import time

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
async def greet():
    """Async endpoint that returns a greeting."""
    start_time = time.time()
    await asyncio.sleep(1)
    wait_time = time.time() - start_time
    return f"Hello, World! (waited {wait_time:.2f} seconds)"


if __name__ == "__main__":
    # Demo of invoking uvicorn internally from python programs
    import uvicorn

    # Reload = True implies Uvicorn will restart the web server when code changes are detected.
    uvicorn.run("a4_fastapi_async:app", host="127.0.0.1", port=8004, reload=True)
