from __future__ import annotations

from collections.abc import Iterable
from typing import Self
import logging

from django.http import HttpRequest
import pydantic
import pydantic_core

from ..abc import ListOf
from ..result import Result, partition_results


class Empty(pydantic.BaseModel):
    """
    An empty Pydantic model. User in cases where a model must be provided, but
    we don't want to actually validate anything.
    """

    pass


class APIObj[_DjangoType](pydantic.BaseModel):
    """Base class for creating API serializers from Django models."""

    @classmethod
    def get_list_model(cls) -> type[ListOf[Self]]:
        """Get or create a ListOf type for this model."""
        # Use custom List class if its defined
        ListCls = getattr(cls, "List", None)
        if ListCls:
            if not issubclass(ListCls, ListOf):
                raise TypeError(f"{ListCls} must be a subclass of {ListOf}")
            return ListCls  # type:ignore[no-any-return]

        # No custom list type was defined, so construct one.
        ListCls = pydantic.create_model(
            f"{cls.__name__}_List",
            __base__=ListOf,
        )
        cls.List = ListCls  # type:ignore[attr-defined]
        return ListCls

    @classmethod
    def from_django(
        cls,
        request: HttpRequest,
        obj: _DjangoType,
    ) -> Result[Self, pydantic_core.ValidationError]:
        """Convert a Django model instance to this API model."""
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def list_from_django(
        cls,
        request: HttpRequest,
        rows: Iterable[_DjangoType],
    ) -> tuple[
        ListOf[Self],
        list[pydantic_core.ValidationError],
    ]:
        """Convert a collection of Django models to a typed list, partitioning successes and errors."""
        oks, errs = partition_results(cls.from_django(request, row) for row in rows)
        if len(errs) > 0:
            logging.info(
                "Dropped %d objects from list due to validation errors: %s",
                len(errs),
                errs[0],
            )
        APIList = cls.get_list_model()
        return APIList(oks), errs
