import logging

from django.conf import settings
from rest_framework import status

from fedkit.models import Actor
from fedkit.signals import action
from fedkit.tasks import fetchRemoteActor

from .base import BaseActivity

logger = logging.getLogger(__name__)


class Accept(BaseActivity):
    """
    Received an Accept.

    Remember the accept-id in the database.
    So we can later delete the follow request.

    :param target: The target of the activity
    :param activity: The :py:class:fedkit.activity.Activityobject`
    """

    def respond(self):
        """
        Accept the Follow activity.
        Remember the accept-id in the database.
        So we can later delete the follow request.
        """
        from fedkit.models import Follow

        assert self.target is self.activity.actor

        follow = Follow.objects.get(actor=self.activity.actor)
        follow.accepted = self.activity.id  # remember the accept-id
        follow.save()

        """
        .. todo::
            Check the actual message that needs to be returned.
        """

        return {"status": "accepted."}, status.HTTP_200_OK


class Follow(BaseActivity):
    def respond(self):
        """
        .. example:: Follow Activity {
            '@context': 'https://www.w3.org/ns/activitystreams',
            'id': 'https://neumeier.org/o/ca357ba56dc24554bfb7646a1db2c67f',
            'type': 'Follow',
            'actor': 'https://neumeier.org',
            'object': 'https://pramari.de/accounts/andreas/'
        }
        """

        logger.error(
            f"Activity: {self.activity.actor} wants to follow {self.activity.object}"
        )

        assert self.activity.actor is not None
        assert self.actor is self.activity.actor

        # Step 1:
        # Create the actor profile in the database
        # and establish the follow relationship
        remoteActor = fetchRemoteActor(self.activity.actor)
        remoteActorObject = Actor.objects.get(id=remoteActor.get("id"))
        localActorObject = Actor.objects.get(id=self.activity.object)
        remoteActorObject.follows.add(localActorObject)

        # Step 2:
        # Confirm the follow request to message.actor
        from fedkit.tasks.activitypub import acceptFollow

        """
        .. todo::
            - Check if the signature is valid
            - Store the follow request in the database
            - Defer the task to the background
        """
        action_id = action.send(
            sender=localActorObject, verb="Accept", action_object=remoteActorObject
        )

        if settings.DEBUG:
            acceptFollow(remoteActor.get("inbox"), self.activity, action_id[0][1].id)
        else:
            acceptFollow.delay(
                remoteActor.get("inbox"), self.activity, action_id[0][1].id
            )

        return {
            "status": f"OK: {self.activity.actor} followed {self.activity.object}"
        }, status.HTTP_200_OK
