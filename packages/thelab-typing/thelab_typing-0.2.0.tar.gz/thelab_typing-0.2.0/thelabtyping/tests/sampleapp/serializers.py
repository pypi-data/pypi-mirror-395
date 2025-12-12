from typing import Self

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest
import pydantic
import pydantic_core

from thelabtyping.abc import ListOf
from thelabtyping.api.serializers import APIObj
from thelabtyping.result import Ok, Result, as_result


class UserSearchQuery(pydantic.BaseModel):
    id: int | None = None
    first_name: str | None = None

    def get_queryset(self) -> QuerySet[User]:
        qs = User.objects.all()
        if self.id:
            qs = qs.filter(id=self.id)
        if self.first_name:
            qs = qs.filter(first_name=self.first_name)
        return qs


class APIUser(APIObj[User]):
    """
    Example of an API serializer for the User model
    """

    username: str
    first_name: str
    last_name: str

    @classmethod
    @as_result(pydantic_core.ValidationError)
    def from_django(cls, request: HttpRequest, obj: User) -> Self:
        return cls(
            username=obj.username,
            first_name=obj.first_name,
            last_name=obj.last_name,
        )

    def create(self, request: HttpRequest) -> Result[User, Exception]:
        user = User.objects.create_user(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        return Ok(user)


class APIUserWithCustomList(APIUser):
    class List(ListOf["APIUserWithCustomList"]):
        pass
