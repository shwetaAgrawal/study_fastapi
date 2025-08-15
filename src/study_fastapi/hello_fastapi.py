"""hello world for FastAPI."""

from fastapi import FastAPI

# app is the top-level FastAPI object that represents the whole web application.
app = FastAPI()


def get_greeting_message(name: str | None = None) -> str:
    """Return a greeting message.

    If a name is provided, it returns a personalized greeting;
    otherwise, it returns a generic greeting.

    @params name (str): Name of the person to greet.
    @returns str: A personalized greeting message.
    """
    return f"Hello, {name}!" if name else "Hello, World!"


# decorator telling request type - GET, and url route to function mapping
@app.get("/hi", description="Get a static greeting.")
def greet_static() -> str:
    """Return a static greeting. URL to check - http://127.0.0.1:8000/hi .

    Any query parameter passed with this URL will be ignored.

    @returns str: A friendly greeting.
    """
    return get_greeting_message()


@app.get("/hi_name/{name}", description="Get a personalized greeting.")
def greet_personalized_path(name: str) -> str:
    """Return a named greeting. URL to check - http://127.0.0.1:8000/hi_name/shweta .

    If no name is provided, it will return a 404 error.
    Ex URLs - http://127.0.0.1:8000/hi_name/, http://127.0.0.1:8000/hi_name

    @params name (str): Name of the person to greet.
    @returns str: A personalized greeting message.
    """
    return get_greeting_message(name)


@app.get("/hello", description="Get a personalized greeting.")
def greet_personalized_query(name: str) -> str:
    """Return a personalized greeting. URL to check - http://127.0.0.1:8000/hello?name=shweta .

    If name is null, it will by default return "Hello, World!". Ex - http://127.0.0.1:8000/hello?name=
    If name query parameter is not provided, it will return a 422 error. Ex - http://127.0.0.1:8000/hello

    @params name (str): Name of the person to greet.
    @returns str: A personalized greeting message.
    """
    return get_greeting_message(name)


if __name__ == "__main__":
    # Demo of invoking uvicorn internally from python programs
    import uvicorn

    # Reload = True implies Uvicorn will restart the web server when code changes are detected.
    uvicorn.run("study_fastapi.hello_fastapi:app", host="127.0.0.1", port=8000, reload=True)
