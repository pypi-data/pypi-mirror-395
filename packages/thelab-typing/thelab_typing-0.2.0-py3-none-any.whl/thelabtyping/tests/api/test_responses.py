import uuid

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
import pydantic_core

from thelabtyping.api.responses import APIResponse
from thelabtyping.api.status import Status
from thelabtyping.result import Result

from ..sampleapp.serializers import APIUser


class APIResponseTest(TestCase):
    def _get_api_user(
        self,
        valid: bool = True,
    ) -> tuple[User, Result[APIUser, pydantic_core.ValidationError]]:
        request = RequestFactory().get("/")
        user = User(
            username=str(uuid.uuid4()),
            first_name="joe" if valid else 42,
            last_name="schmoe",
        )
        return user, APIUser.from_django(request, user)

    def test_accept_model(self) -> None:
        user, maybeobj = self._get_api_user(valid=True)
        assert maybeobj.is_ok
        response = APIResponse(maybeobj.ok())
        self.assertEqual(response.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(
            response.content,
            {
                "username": user.username,
                "first_name": "joe",
                "last_name": "schmoe",
            },
        )

    def test_accept_result_containing_model(self) -> None:
        user, maybeobj = self._get_api_user(valid=True)
        response = APIResponse(maybeobj)
        self.assertEqual(response.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(
            response.content,
            {
                "username": user.username,
                "first_name": "joe",
                "last_name": "schmoe",
            },
        )

    def test_accept_result_containing_errors(self) -> None:
        user, maybeobj = self._get_api_user(valid=False)
        response = APIResponse(maybeobj)
        self.assertEqual(response.status_code, Status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            response.content,
            {
                "errors": {
                    "first_name": {
                        "type": "string_type",
                        "msg": "Input should be a valid string",
                    }
                }
            },
        )
