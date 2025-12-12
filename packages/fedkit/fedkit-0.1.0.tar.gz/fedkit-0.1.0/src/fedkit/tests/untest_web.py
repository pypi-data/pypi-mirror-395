from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from fedkit.models import Like


class WebLikeTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.username = "andreas"
        self.password = "password"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

    def test_like_create_anonymous(self):
        response = self.client.get(reverse("like-create"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/web/like/")
        self.assertEqual(Like.objects.count(), 0)

    def test_like_create_authenticated(self):
        self.client.login(username=self.username, password="password")
        response = self.client.get(reverse("like-create"))
        self.assertEqual(response.status_code, 200)
        actor = self.user.profile.actor
        response = self.client.post(
            reverse("like-create"),
            data={"actor": actor, "object": "https://pramari.de"},
        )
        like = Like.objects.get()
        self.assertEqual(Like.objects.count(), 1)
        self.assertRedirects(response, reverse("like-detail", kwargs={"pk": like.id}))

    def test_like_list(self):
        self.client.login(username=self.username, password=self.password)
        slug = self.user.profile.slug
        response = self.client.get(reverse("like-list", kwargs={"slug": slug}))
        self.assertEqual(response.status_code, 200)

    def test_like_detail(self):
        self.client.login(username=self.username, password=self.password)
        like = Like.objects.create(
            actor=self.user.profile.actor, object="http://pramari.de"
        )
        response = self.client.get(reverse("like-detail", kwargs={"pk": like.id}))
        self.assertEqual(response.status_code, 200)

    def test_like_delete(self):
        self.client.login(username=self.username, password=self.password)
        like = Like.objects.create(
            actor=self.user.profile.actor, object="http://pramari.de"
        )
        response = self.client.get(reverse("like-delete", kwargs={"pk": like.id}))
        self.assertEqual(response.status_code, 200)
        self.client.post(reverse("like-delete", kwargs={"pk": like.pk}))
        self.assertEqual(Like.objects.count(), 0)
