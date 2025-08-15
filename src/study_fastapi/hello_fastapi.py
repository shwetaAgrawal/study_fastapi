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
@app.get("/hi")
def greet_hi() -> str:
    """Return a static greeting. URL to check - http://127.0.0.1:8000/hi .

    Any query parameter passed with this URL will be ignored.

    @returns str: A friendly greeting.
    """
    return get_greeting_message()


@app.get("/hi_name/{name}")
def greet_hi_name(name: str) -> str:
    """Return a named greeting. URL to check - http://127.0.0.1:8000/hi_name/shweta .

    @params name (str): Name of the person to greet.
    @returns str: A personalized greeting message.
    """
    return get_greeting_message(name)


@app.get("/hello")
def greet_hello(name: str) -> str:
    """Return a personalized greeting. URL to check - http://127.0.0.1:8000/hello?name=shweta .

    @params name (str): Name of the person to greet.
    @returns str: A personalized greeting message.
    """
    return get_greeting_message(name)
