"""Exploration of header parameters in FastAPI."""

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/useragent")
def get_user_agent(user_agent: str = Header()):
    """Get the User-Agent header. URL = http://127.0.0.1:8002/useragent .

    FastAPI converts HTTP header keys to lowercase,
    and converts a hyphen (-) to an underscore (_). So to get User-Agent header,
    json key is user_agent. Try "curl http://127.0.0.1:8002/useragent" to check default
    useragent for curl.

    @params user_agent: The User-Agent string from the request headers.
    @returns: A JSON response containing the User-Agent string.
    """
    return user_agent


@app.get("/hi", description="Method to test where does it search for parameters")
def greet(name: str) -> str:
    """Return a friendly greeting. URL = http://127.0.0.1:8002/hi .

    @returns: A friendly greeting message.
    """
    return f"Hello, {name}!"


@app.post("/hi_post", description="Method to test where does it search for parameters")
def greet_post(name: str) -> str:
    """Return a friendly greeting. URL = http://127.0.0.1:8002/hi .

    @returns: A friendly greeting message.
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    # Demo of invoking uvicorn internally from python programs
    import uvicorn

    # Reload = True implies Uvicorn will restart the web server when code changes are detected.
    uvicorn.run("study_fastapi.2fastapi_header:app", host="127.0.0.1", port=8002, reload=True)
