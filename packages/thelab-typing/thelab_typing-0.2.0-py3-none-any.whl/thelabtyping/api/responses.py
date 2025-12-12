from typing import TypedDict, assert_never
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import pydantic
import pydantic_core

from ..result import Err, Ok
from .status import Status


class APIValidationError(TypedDict):
    """Structure for a single API validation error."""

    type: str
    msg: str


class APIValidationErrors(TypedDict):
    """Structure for API validation error response."""

    errors: dict[str, APIValidationError]


def _build_errors(exc: pydantic_core.ValidationError) -> APIValidationErrors:
    """Convert a Pydantic validation error to structured API error format."""
    errors = exc.errors(
        include_url=False,
        include_context=False,
        include_input=False,
    )
    resp: APIValidationErrors = {
        "errors": {
            (".".join(str(seg) for seg in err["loc"])): {
                "type": err["type"],
                "msg": err["msg"],
            }
            for err in errors
        }
    }
    return resp


class APIResponse[T: pydantic.BaseModel](HttpResponse):
    """
    An HTTP response class that accepts a Pydantic model object and sends it as
    JSON.
    """

    def __init__(
        self,
        # Accept either a model, or a Result which might contain a model.
        maybe_obj: T | Ok[T] | Err[pydantic_core.ValidationError] | Err[Exception],
        # Other response kwargs to pass through
        content_type: str = "application/json",
        status: int | None = None,
        reason: str | None = None,
        charset: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        """Create an API response from a Pydantic model or Result type."""
        data: str = ""
        if isinstance(maybe_obj, pydantic.BaseModel):
            obj = maybe_obj
            data = obj.model_dump_json()
        elif isinstance(maybe_obj, Ok):
            obj = maybe_obj.ok()
            data = obj.model_dump_json()
        elif isinstance(maybe_obj, Err):
            exc = maybe_obj.err()
            # If not a validation error, raise the error and let Django handle it
            if not isinstance(exc, pydantic_core.ValidationError):
                raise exc
            data = json.dumps(
                _build_errors(exc),
                indent=True,
                cls=DjangoJSONEncoder,
            )
            status = Status.HTTP_400_BAD_REQUEST
            reason = None
        else:
            assert_never(maybe_obj)  # pragma: no cover
        super().__init__(
            content=data,
            content_type=content_type,
            status=status,
            reason=reason,
            charset=charset,
            headers=headers,
        )
