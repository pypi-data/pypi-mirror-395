import logging

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.dispatch import Signal

from fedkit.models import Note

User = get_user_model()

logger = logging.getLogger(__name__)


class OutboxTest(TestCase):
    def setUp(self):
        from fedkit.models import Actor
        self.client = Client()  # A client for all tests.
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="andreas",
            email="andreas@neumeier.org",
            password="top_secret",
        )
        if created:
            user.save()
        actor = Actor.objects.get(user=user)
        self.assertTrue(isinstance(actor, Actor))

    def test_outbox_html(self):
        """
        Test whether the outbox is reachable.

        .. todo::
            Implement test_outbox_content with `reverse`.
        """
        result = self.client.get(
            "/@andreas/outbox",
            headers={"Accept": "text/html"},
        )
        logger.debug(f"result: {result.content}")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content_type, "text/html")

    def test_outbox_activity(self):
        """
        Test whether the outbox is reachable.

        .. todo::
            Implement test_outbox_content with `reverse`.
        """
        result = self.client.get(
            "/@andreas/outbox",
            accept="application/ld+json; profile=https://www.w3.org/ns/activitystreams",
        )
        logger.debug(f"result: {result.content}")
        self.assertEqual(result.status_code, 200)
        self.assertIn(result.content_type, "application/activity+json")
        self.assertContains(result, "OrderedCollection")

    def test_outbox_page_one(self):
        """
        Test whether the outbox is reachable.

        .. todo::
            Implement test_outbox_content with `reverse`.
        """
        result = self.client.get(
            "/@andreas/outbox?page1",
            accept="application/ld+json; profile=https://www.w3.org/ns/activitystreams",
        )
        logger.debug(f"result: {result.content}")
        self.assertEqual(result.status_code, 200)

    def test_outbox_content(self):
        """
        Test whether the outbox is reachable.
        This time when the outbox is not empty.
        """

        n = Note.objects.create(content="Hello, World!")
        n.save()
        u = User.objects.get(username="andreas")
        Signal().send(sender=Note, instance=n, actor=u, verb="Create")
        result = self.client.get(
            "/@andreas/outbox",
        )
        logger.debug(f"result: {result.content}")
        self.assertEqual(result.status_code, 200)
