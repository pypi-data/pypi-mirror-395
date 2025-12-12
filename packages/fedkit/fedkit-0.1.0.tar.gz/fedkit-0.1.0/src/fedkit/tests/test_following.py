from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()

accept_html = "text/html"
accept_json = "application/json"
accept_ld = "application/ld+json"
accept_jsonld_profile = (
    'application/ld+json; profile="https://www.w3.org/ns/activitystreams"'
)
accept_mastodon = "application/activity+json"  # application/activity, application/ld"


class FollowersTest(TestCase):
    def setUp(self):
        """
        Setup test.
        """
        self.client = Client()
        self.user = User.objects.create_user(username="user", password="password")
        self.user.save()
        self.follower = User.objects.create(username="follower")
        self.followed = User.objects.create(username="followed")
        self.user.actor.follows.add(self.follower.actor)
        self.user.actor.followed_by.add(self.followed.actor)

    def test_followers_ld(self):
        """
        Test `/accounts/user/followers`.
        Nothing more than a simple GET request.
        """
        result = self.client.get(
            reverse("actor-followers", kwargs={"slug": "user"}),
        )
        self.assertEqual(result.status_code, 200)


class FollowingTest(TestCase):
    def setUp(self):
        """
        Setup test.
        """
        self.client = Client()
        self.user = User.objects.create_user(username="user", password="password")
        self.user.save()

    def redo_test_following_html(self):
        """
        Test `/accounts/user/following`.
        Nothing more than a simple GET request.
        """
        result = self.client.get(
            reverse("actor-following", kwargs={"slug": "user"}),
            headers={"Accept": "text/html"},
        )

        self.assertEqual(result.status_code, 200)

    def test_following_activity_json(self):
        """
        Test `/accounts/user/following`.
        Nothing more than a simple GET request.
        """
        result = self.client.get(
            reverse("actor-following", kwargs={"slug": "user"}),
            headers={"Accept": "application/ld+json"},
        )

        self.assertEqual(result.status_code, 200)
