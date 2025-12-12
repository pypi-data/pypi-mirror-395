from typing import Literal, assert_type

from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.test import RequestFactory, TestCase

from thelabtyping.api.requests import (
    AuthdEmptyTypedRequest,
    AuthdTypedRequest,
    AuthdTypedRequestBody,
    AuthdTypedRequestQuery,
    EmptyTypedRequest,
    TypedRequest,
    TypedRequestBody,
)
from thelabtyping.api.responses import APIResponse
from thelabtyping.api.serializers import Empty
from thelabtyping.api.status import Status
from thelabtyping.api.views import validate

from ..sampleapp.serializers import APIUser, UserSearchQuery


class FunctionalViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="joe", password="password")

    def test_typed_request(self) -> None:
        @validate()
        def view(
            request: TypedRequest[UserSearchQuery, APIUser],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[UserSearchQuery, APIUser])
            assert_type(request.user, User | AnonymousUser)
            assert_type(request.validated_querystring, UserSearchQuery)
            assert_type(request.validated_body, APIUser)
            return APIResponse(Empty())

        req = RequestFactory().post(
            "/",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_typed_request_body(self) -> None:
        @validate()
        def view(
            request: TypedRequestBody[APIUser],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[Empty, APIUser])
            assert_type(request.user, User | AnonymousUser)
            assert_type(request.validated_querystring, Empty)
            assert_type(request.validated_body, APIUser)
            return APIResponse(Empty())

        req = RequestFactory().post(
            "/",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_empty_request(self) -> None:
        @validate()
        def view(
            request: EmptyTypedRequest,
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[Empty, Empty])
            assert_type(request.user, User | AnonymousUser)
            assert_type(request.validated_querystring, Empty)
            assert_type(request.validated_body, Empty)
            return APIResponse(Empty())

        req = RequestFactory().get("/")
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_authd_typed_request(self) -> None:
        @validate()
        def view(
            request: AuthdTypedRequest[UserSearchQuery, APIUser],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[UserSearchQuery, APIUser, User])
            assert_type(request.user, User)
            assert_type(request.user.is_authenticated, Literal[True])
            assert_type(request.user.is_anonymous, Literal[False])
            assert_type(request.validated_querystring, UserSearchQuery)
            assert_type(request.validated_body, APIUser)
            return APIResponse(Empty())

        req = RequestFactory().post(
            "/",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        req.user = self.user
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_authd_typed_request_query(self) -> None:
        @validate()
        def view(
            request: AuthdTypedRequestQuery[UserSearchQuery],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[UserSearchQuery, Empty, User])
            assert_type(request.user, User)
            assert_type(request.user.is_authenticated, Literal[True])
            assert_type(request.user.is_anonymous, Literal[False])
            assert_type(request.validated_querystring, UserSearchQuery)
            assert_type(request.validated_body, Empty)
            return APIResponse(Empty())

        req = RequestFactory().get("/")
        req.user = self.user
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_authd_typed_request_body(self) -> None:
        @validate()
        def view(
            request: AuthdTypedRequestBody[APIUser],
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[Empty, APIUser, User])
            assert_type(request.user, User)
            assert_type(request.user.is_authenticated, Literal[True])
            assert_type(request.user.is_anonymous, Literal[False])
            assert_type(request.validated_querystring, Empty)
            assert_type(request.validated_body, APIUser)
            return APIResponse(Empty())

        req = RequestFactory().post(
            "/",
            data={
                "username": "jack",
                "first_name": "Jack",
                "last_name": "Jackson",
            },
        )
        req.user = self.user
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_authd_typed_request_empty(self) -> None:
        @validate()
        def view(
            request: AuthdEmptyTypedRequest,
        ) -> APIResponse[Empty]:
            # Some assertions to prove the `validate` decorator is doing what it's
            # supposed to
            assert_type(request, TypedRequest[Empty, Empty, User])
            assert_type(request.user, User)
            assert_type(request.user.is_authenticated, Literal[True])
            assert_type(request.user.is_anonymous, Literal[False])
            assert_type(request.validated_querystring, Empty)
            assert_type(request.validated_body, Empty)
            return APIResponse(Empty())

        req = RequestFactory().get("/")
        req.user = self.user
        resp = view(req)
        self.assertEqual(resp.status_code, Status.HTTP_200_OK)

    def test_invalid_request_type(self) -> None:
        with self.assertRaises(TypeError):

            @validate()
            def view(
                request: HttpRequest,
            ) -> APIResponse[Empty]:
                # Some assertions to prove the `validate` decorator is doing what it's
                # supposed to
                assert_type(request, HttpRequest)
                assert_type(request.user, User | AnonymousUser)
                return APIResponse(Empty())
