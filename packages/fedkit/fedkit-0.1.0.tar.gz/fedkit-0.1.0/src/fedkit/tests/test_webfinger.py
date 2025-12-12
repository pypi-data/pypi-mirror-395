import logging

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

logger = logging.getLogger(__name__)


class WebfingerTests(TestCase):
    """
    Test the webfinger endpoint
    """

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="andreas", email="andreas@neumeier.org"
        )
        user.set_password("password")
        if created:
            user.save()

    def test_webfinger_get_no_query_parameter(self):
        """
        Test that a GET request to /.well-known/webfinger returns a 400

        This will be the case if the resource query parameter is missing or empty.
        """
        response = self.client.get("/.well-known/webfinger")

        self.assertEqual(
            response.status_code, 400
        )  # asuming 404 is the correct status code
        self.assertEqual(response["Content-Type"], "application/jrd+json")
        self.assertEqual(response.json(), {"detail": "Missing resource parameter"})

    def test_webfinger_get_resource(self):
        """
        Test that a GET request to /.well-known/webfinger with a resource query parameter returns a 200
        """
        response = self.client.get(
            "/.well-known/webfinger",
            query_params={"resource": "acct:andreas@example.com"},
            headers={"accept": "application/jrd+json"},
        )
        self.assertEqual(response["Content-Type"], "application/jrd+json")
        self.assertEqual(type(response.json()), type({}))
        self.assertEqual(response.status_code, 200)
