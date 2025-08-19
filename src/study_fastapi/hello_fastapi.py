"""hello world for FastAPI."""

from fastapi import Body, FastAPI, Header

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
    Even though get_greeting_message returns a string, FastAPI wraps it in the json
    and we need to decode it

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


@app.post("/hello", description="Get a personalized greeting.")
def greet_personalized_body(name: str = Body(embed=True)) -> str:
    """Return a personalized greeting. URL to check - http://127.0.0.1:8000/hello .

    NOTE: same path can be mapped to multiple functions, each handling different request methods.
    URL remains same however the request method is POST.
    Body(embed=True) signifies that name key will be present in the request body as JSON.
    Body is expected to be like {"name": "shweta"}

    @params name (str): Name of the person to greet.
    @returns str: A personalized greeting message.
    """
    return get_greeting_message(name)


@app.post("/hello_header", description="Get a personalized greeting.")
def greet_personalized_header(name: str = Header()) -> str:
    """Return a personalized greeting. URL to check - http://127.0.0.1:8000/hello_header .

    NOTE: we can't use /hello path again because we already mapped post method to
    greet_personalized_body
    Header is expected to be like {"name": "shweta"}

    @params name (str): Name of the person to greet.
    @returns str: A personalized greeting message.
    """
    return get_greeting_message(name)


if __name__ == "__main__":
    # Demo of invoking uvicorn internally from python programs
    import uvicorn

    # Reload = True implies Uvicorn will restart the web server when code changes are detected.
    uvicorn.run("hello_fastapi:app", host="127.0.0.1", port=8000, reload=True)
