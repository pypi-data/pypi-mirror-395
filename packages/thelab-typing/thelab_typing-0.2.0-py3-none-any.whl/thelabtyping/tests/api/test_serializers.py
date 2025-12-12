import uuid

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
import pydantic_core

from thelabtyping.abc import ListOf

from ..sampleapp.serializers import APIUser, APIUserWithCustomList


class APIObjTest(TestCase):
    def setUp(self) -> None:
        self.rfact = RequestFactory()
        self.request = self.rfact.get("/api/users/")
        self.users = [
            User.objects.create_user(
                username=str(uuid.uuid4()),
                first_name=f"joe-{i}",
                last_name=f"schmoe-{i}",
            )
            for i in range(3)
        ]

    def test_serialize_single_object(self) -> None:
        maybeobj = APIUser.from_django(self.request, self.users[0])
        assert maybeobj.is_ok
        obj = maybeobj.ok()
        self.assertIsInstance(obj, APIUser)
        self.assertEqual(
            obj.model_dump(),
            {
                "username": self.users[0].username,
                "first_name": "joe-0",
                "last_name": "schmoe-0",
            },
        )

    def test_serialize_object_list(self) -> None:
        obj_list, errs = APIUser.list_from_django(self.request, self.users)
        self.assertIsInstance(obj_list, ListOf)
        self.assertIsInstance(obj_list[0], APIUser)
        self.assertEqual(len(obj_list), len(self.users))
        self.assertEqual(len(errs), 0)
        self.assertEqual(
            obj_list.model_dump(),
            [
                {
                    "username": self.users[0].username,
                    "first_name": "joe-0",
                    "last_name": "schmoe-0",
                },
                {
                    "username": self.users[1].username,
                    "first_name": "joe-1",
                    "last_name": "schmoe-1",
                },
                {
                    "username": self.users[2].username,
                    "first_name": "joe-2",
                    "last_name": "schmoe-2",
                },
            ],
        )

    def test_serialize_object_list_custom_list_class(self) -> None:
        obj_list, errs = APIUserWithCustomList.list_from_django(
            self.request,
            self.users,
        )
        self.assertIsInstance(obj_list, APIUserWithCustomList.List)
        self.assertIsInstance(obj_list[0], APIUserWithCustomList)
        self.assertEqual(len(obj_list), len(self.users))
        self.assertEqual(len(errs), 0)
        self.assertEqual(
            obj_list.model_dump(),
            [
                {
                    "username": self.users[0].username,
                    "first_name": "joe-0",
                    "last_name": "schmoe-0",
                },
                {
                    "username": self.users[1].username,
                    "first_name": "joe-1",
                    "last_name": "schmoe-1",
                },
                {
                    "username": self.users[2].username,
                    "first_name": "joe-2",
                    "last_name": "schmoe-2",
                },
            ],
        )

    def test_catches_validation_errs(self) -> None:
        # Force a validation error by setting a first_name to an integer
        self.users[1].first_name = 42
        # Result list should omit the invalid object and include it as an error
        obj_list, errs = APIUser.list_from_django(self.request, self.users)
        self.assertIsInstance(obj_list, ListOf)
        self.assertEqual(len(obj_list), len(self.users) - 1)
        self.assertEqual(len(errs), 1)
        self.assertEqual(
            obj_list.model_dump(),
            [
                {
                    "username": self.users[0].username,
                    "first_name": "joe-0",
                    "last_name": "schmoe-0",
                },
                {
                    "username": self.users[2].username,
                    "first_name": "joe-2",
                    "last_name": "schmoe-2",
                },
            ],
        )
        self.assertIsInstance(errs[0], pydantic_core.ValidationError)
        self.assertTrue(
            str(errs[0]).startswith(
                "1 validation error for APIUser\n"
                "first_name\n"
                "  Input should be a valid string [type=string_type, input_value=42, input_type=int]"
            ),
        )
