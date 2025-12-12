from django.test import TestCase

from thelabtyping.api.status import Status


class HttpStatusTest(TestCase):
    def test_statuses(self) -> None:
        self.assertEqual(Status.HTTP_200_OK.is_informational, False)
        self.assertEqual(Status.HTTP_200_OK.is_success, True)
        self.assertEqual(Status.HTTP_200_OK.is_redirect, False)
        self.assertEqual(Status.HTTP_200_OK.is_client_error, False)
        self.assertEqual(Status.HTTP_200_OK.is_server_error, False)

        self.assertEqual(Status.HTTP_403_FORBIDDEN.is_informational, False)
        self.assertEqual(Status.HTTP_403_FORBIDDEN.is_success, False)
        self.assertEqual(Status.HTTP_403_FORBIDDEN.is_redirect, False)
        self.assertEqual(Status.HTTP_403_FORBIDDEN.is_client_error, True)
        self.assertEqual(Status.HTTP_403_FORBIDDEN.is_server_error, False)
