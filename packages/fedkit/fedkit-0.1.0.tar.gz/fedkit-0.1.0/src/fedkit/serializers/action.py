from django.contrib.sites.models import Site
from rest_framework import serializers

from fedkit.models import Action

"""
    {
      "id": "https://23.social/users/andreasofthings/statuses/114737259588005180/activity",
      "type": "Announce",
      "actor": "https://23.social/users/andreasofthings",
      "published": "2025-06-24T07:54:01Z",
      "to": [
        "https://www.w3.org/ns/activitystreams#Public"
      ],
      "cc": [
        "https://mastodon.social/users/pallenberg",
        "https://23.social/users/andreasofthings/followers"
      ],
      "object": "https://mastodon.social/users/pallenberg/statuses/114737090958772616"
    }
"""


class ActionSerializer(serializers.ModelSerializer):
    """
    Action to Activity (Outbound)
    """

    def get_url(self, action):
        base = f"https://{Site.objects.get_current().domain}"

        return f"{base}{action.get_absolute_url()}"

    def get_published(self, action):
        return action.timestamp.isoformat()

    def get_to(self, action):
        if action.public:
            return ["https://www.w3.org/ns/activitystreams#Public"]
        return []

    def get_object(self, action):
        if action.action_object:
            return action.action_object.id  # get_absolute_url()
        return None

    id = serializers.SerializerMethodField("get_url")
    type = serializers.CharField(source="activity_type")
    actor = serializers.CharField(source="actor.id")
    published = serializers.SerializerMethodField("get_published")
    to = serializers.SerializerMethodField("get_to")
    object = serializers.SerializerMethodField("get_object")

    class Meta:
        model = Action
        fields = ["id", "type", "actor", "published", "to", "object"]
