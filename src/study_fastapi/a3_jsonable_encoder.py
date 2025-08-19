"""Exploration of json encoding of various datatypes by FastAPI."""

import json

from fastapi.encoders import jsonable_encoder


def get_fastapi_jsonencoded(obj):
    """Get encodable json object."""
    return jsonable_encoder(obj)


def get_fastapi_encoded_string(obj):
    """Get json serialized string for object."""
    return json.dumps(get_fastapi_jsonencoded(obj))


def get_json_dumps(obj):
    """Get json dump of any python object.

    This doesn't support all datatypes though. So FastAPI created a middle layer
    which converts python object to any json encodeable object.

    Basically it supports only objects with either an iterator method implementation
    or int, str, float, bool
    list and dict supported as they implement an iterator method
    Any complex object without a type iterator will return in a Type Error
    """
    return json.dumps(obj)
