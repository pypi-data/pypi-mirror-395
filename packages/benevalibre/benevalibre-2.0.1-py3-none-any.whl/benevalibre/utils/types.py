from typing import Annotated

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema
from pydantic import HttpUrl as BaseHttpUrl


def validate_http_url(value: str) -> str:
    try:
        URLValidator(schemes=["http", "https"])(value)
    except ValidationError as e:
        raise ValueError(e.message)
    return value


HttpUrl = Annotated[
    BaseHttpUrl,
    BeforeValidator(validate_http_url),
    PlainSerializer(lambda v: str(v), return_type=str),
    WithJsonSchema({"type": "string"}),
]
