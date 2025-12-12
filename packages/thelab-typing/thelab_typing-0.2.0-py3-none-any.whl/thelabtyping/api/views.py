from collections.abc import Callable
from typing import Concatenate, assert_type, cast, get_args, get_origin, get_type_hints
import functools

from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, QueryDict
import pydantic
import pydantic_core

from ..result import as_result
from .requests import (
    AnyUser,
    AuthdEmptyTypedRequest,
    AuthdTypedRequest,
    AuthdTypedRequestBody,
    AuthdTypedRequestQuery,
    EmptyTypedRequest,
    TypedRequest,
    TypedRequestBody,
    TypedRequestQuery,
)
from .responses import APIResponse
from .serializers import Empty


def _prep_querydict_for_pydantic(queryDict: QueryDict) -> dict[str, str | list[str]]:
    data: dict[str, str | list[str]] = {
        key: (val_list[0] if len(val_list) == 1 else val_list)
        for key, val_list in ((key, queryDict.getlist(key)) for key in queryDict.keys())
        if len(val_list) > 0
    }
    return data


@as_result(pydantic_core.ValidationError)
def _parse_request_querystring[_QST: pydantic.BaseModel](
    model: type[_QST],
    request: HttpRequest,
) -> _QST:
    data = _prep_querydict_for_pydantic(request.GET)
    return model.model_validate(data)


@as_result(pydantic_core.ValidationError)
def _parse_request_body[_BT: pydantic.BaseModel](
    model: type[_BT],
    request: HttpRequest,
) -> _BT:
    ct = request.headers.get("Content-Type")
    if ct is not None:
        ct = ct.split(";")[0].strip()
    if ct == "application/json":
        return model.model_validate_json(request.body)
    if ct in ("multipart/form-data", "application/x-www-form-urlencoded"):
        data = _prep_querydict_for_pydantic(request.POST)
        return model.model_validate(data)
    return model.model_validate({})


def _infer_request_types[
    **P,
    R: HttpResponse,
    _QST: pydantic.BaseModel,
    _BT: pydantic.BaseModel,
    _UT: AnyUser,
](
    fn: Callable[Concatenate[TypedRequest[_QST, _BT, _UT], P], R],
) -> tuple[
    type[_QST],  # Querystring model class
    type[_BT],  # Body model class
    bool,  # Requires authenticated user?
]:
    request_type = get_type_hints(fn).get("request") or EmptyTypedRequest
    origin = get_origin(request_type)
    if origin is None:
        origin = request_type
    args = get_args(request_type)

    # Auth-required types
    if origin is AuthdEmptyTypedRequest:
        return cast(type[_QST], Empty), cast(type[_BT], Empty), True

    if origin is AuthdTypedRequestQuery:
        return cast(type[_QST], args[0]), cast(type[_BT], Empty), True

    if origin is AuthdTypedRequestBody:
        return cast(type[_QST], Empty), cast(type[_BT], args[0]), True

    if origin is AuthdTypedRequest:
        return cast(type[_QST], args[0]), cast(type[_BT], args[1]), True

    # Auth-not-required types
    if origin is EmptyTypedRequest:
        return cast(type[_QST], Empty), cast(type[_BT], Empty), False

    if origin is TypedRequestQuery:
        return cast(type[_QST], args[0]), cast(type[_BT], Empty), False

    if origin is TypedRequestBody:
        return cast(type[_QST], Empty), cast(type[_BT], args[0]), False

    if origin is TypedRequest:
        return cast(type[_QST], args[0]), cast(type[_BT], args[1]), False

    raise TypeError(f"Failed to infer request types for {fn}")


def validate[
    **P,
    R: HttpResponse,
    _QST: pydantic.BaseModel,
    _BT: pydantic.BaseModel,
    _UT: AnyUser,
]() -> Callable[
    [
        Callable[
            Concatenate[TypedRequest[_QST, _BT, _UT], P],
            R,
        ]
    ],
    Callable[
        Concatenate[HttpRequest, P],
        R | APIResponse[_QST] | APIResponse[_BT] | HttpResponseForbidden,
    ],
]:
    """
    Django view decorator which validated and transforms the incoming request
    data into a `TypedRequest` object (a subclass of HttpRequest). Infers the
    Pydantic models used for validation from the type hints on the view itself.
    For that to work correctly, the `request` param should be typed as
    `TypedRequest[Foo, Bar]` or one of the aliases to TypedRequest defined
    above.
    """

    def decorator(
        fn: Callable[Concatenate[TypedRequest[_QST, _BT, _UT], P], R],
    ) -> Callable[
        Concatenate[HttpRequest, P],
        R | APIResponse[_QST] | APIResponse[_BT] | HttpResponseForbidden,
    ]:
        # Extract validation models
        qs_model, body_model, requires_auth = _infer_request_types(fn)

        @functools.wraps(fn)
        def wrapper(
            request: HttpRequest,
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> R | APIResponse[_QST] | APIResponse[_BT] | HttpResponseForbidden:
            # Check authentication. This isn't intended as a full replacement
            # for more granular checks, like against specific model permissions.
            # It's meant to work in conjunction with those—the main job of this
            # code is to give the wrapped view a more specific type hint for
            # the `request.user` property.
            req_user: User | AnonymousUser = getattr(request, "user", AnonymousUser())
            if requires_auth:
                if req_user.is_anonymous:
                    return HttpResponseForbidden()
                assert_type(req_user, User)

            # Validate querystring
            qs_result = _parse_request_querystring(qs_model, request)
            if qs_result.is_err:
                return APIResponse(qs_result)

            # Validate body
            body_result = _parse_request_body(body_model, request)
            if body_result.is_err:
                return APIResponse(body_result)

            # Construct the typed request
            typed_req = TypedRequest[_QST, _BT, _UT](
                request=request,
                user=req_user,  # type:ignore[arg-type]
                qs=qs_result.ok(),
                body=body_result.ok(),
            )
            # Call the inner view with the new validated request data
            return fn(typed_req, *args, **kwargs)

        return wrapper

    return decorator
