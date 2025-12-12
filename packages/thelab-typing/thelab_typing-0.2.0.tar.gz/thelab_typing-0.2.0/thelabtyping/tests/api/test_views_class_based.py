import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from thelabtyping.api.status import Status


class ClassBasedViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="joe", password="password")
        self.client = Client()

    def test_list_users(self) -> None:
        resp = self.client.get(reverse("sampleapp:users-list"))
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(
            resp.content,
            [
                {
                    "username": "joe",
                    "first_name": "",
                    "last_name": "",
                }
            ],
        )

    def test_list_users_with_filter(self) -> None:
        resp = self.client.get(reverse("sampleapp:users-list") + "?first_name=Jim")
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(resp.content, [])

    def test_list_users_with_invalid_filter(self) -> None:
        resp = self.client.get(reverse("sampleapp:users-list") + "?id=FOO")
        self.assertEqual(resp.status_code, Status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            resp.content,
            {
                "errors": {
                    "id": {
                        "msg": "Input should be a valid integer, unable to parse string as an integer",
                        "type": "int_parsing",
                    }
                }
            },
        )

    def test_create_user(self) -> None:
        self.client.login(username="joe", password="password")
        resp = self.client.post(
            reverse("sampleapp:users-list"),
            content_type="application/json",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(
            resp.content,
            {
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )

    def test_create_user_urlencoded(self) -> None:
        self.client.login(username="joe", password="password")
        resp = self.client.post(
            reverse("sampleapp:users-list"),
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)
        self.assertJSONEqual(
            resp.content,
            {
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )

    def test_create_user_invalid_body(self) -> None:
        self.client.login(username="joe", password="password")
        resp = self.client.post(
            reverse("sampleapp:users-list"),
            content_type="application/json",
            data={
                "username": "jack",
                "first_name": "Jack",
            },
        )
        self.assertEqual(resp.status_code, Status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(
            resp.content,
            {
                "errors": {
                    "last_name": {
                        "msg": "Field required",
                        "type": "missing",
                    },
                },
            },
        )

    def test_create_user_without_login(self) -> None:
        resp = self.client.post(
            reverse("sampleapp:users-list"),
            content_type="application/json",
            data=json.dumps(
                {
                    "username": "jack",
                    "first_name": "Jack",
                    "last_name": "Jackson",
                }
            ),
        )
        self.assertEqual(resp.status_code, Status.HTTP_403_FORBIDDEN)
