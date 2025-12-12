#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
ActivityPub views to drive social interactions in pramari.de.

See::
    https://paul.kinlan.me/adding-activity-pub-to-your-static-site/
"""

import logging
from urllib.parse import urlparse

from rest_framework import status
from rest_framework.response import Response

from fedkit.activity import ActivityObject
# from fedkit.models import Actor
from fedkit.serializers import ActorSerializer
from fedkit.signature import SignatureChecker

from .activity import ActivityBaseView

logger = logging.getLogger(__name__)


class InboxView(ActivityBaseView):
    """
    .. py:class:: webapp.views.InboxView

    The inbox is discovered through the inbox property of an
    :py:class:webapp.models.activitypub.Actor's profile. The
    inbox **MUST** be an `OrderedCollection`.

    .. seealso::
        `ActivityPub Inbox <https://www.w3.org/TR/activitypub/#inbox>_`

    """

    serializer_class = ActorSerializer
    template_name = "activitypub/inbox.html"

    def post(self, request, *args, **kwargs):
        """
        Process the incoming activity.

        First:
            - Parse the incoming request & Verify the signature
            - Get the actor for which the activity is intended

        Second:
            Dispatch to the appropriate method based on the activity type.
        """
        # Process the incoming activity

        signature = SignatureChecker().validate(request)
        target = self.get_object()

        activity = ActivityObject(request.data)
        logger.debug(f"Signature: {signature}")
        logger.error(f"INBOX: Error with Activity: {activity}")
        logger.error(f"INBOX: Type of activity: {type(activity)}")

        if not signature:
            """
            ActivitPub allows actors to interact with each other by sending activities to their inboxes, even without a signature.
            """
            logger.error(f"Error in {request.path}")
            logger.error("InboxView: No Signature")
            logger.error(f"InboxView: Activity {activity}")
            logger.error(f"InboxView: Raw {request.data}")

        logger.error(f"INBOX: Type of activity: {type(activity)}")
        logger.error(f"INBOX: Activity details: {activity}")
        assert isinstance(activity, ActivityObject)
        assert target is not None
        assert request.path == urlparse(target.inbox).path

        if not signature:
            """
            ActivitPub allows actors to interact with each other by sending activities to their inboxes, even without a signature.
            """
            logger.error(f"Error in {request.path}")
            logger.error("InboxView: No Signature")
            logger.error(f"InboxView: Activity {activity}")
            logger.error(f"InboxView: Raw {request.data}")

        from fedkit.activities import create, delete, echorequest, like, undo

        match activity.type.lower():  # alphabetical
            case "accept":
                from fedkit.activities import Accept

                result, status = Accept(
                    target=target, activity=activity, signature=signature
                ).respond()

            case "follow":
                from fedkit.activities import Follow

                result, status = Follow(
                    target=target, activity=activity, signature=signature
                ).respond()
            case "create":
                raise NotImplementedError("Create activity is not implemented yet.")
                result, status = create(target=target.actor, activity=activity)
            case "delete":
                raise NotImplementedError("Delete activity is not implemented yet.")
                result, status = delete(target=target.actor, activity=activity)
            case "echorequest":
                raise NotImplementedError(
                    "EchoRequest activity is not implemented yet."
                )
                result = echorequest(activity=activity, signature=signature)
            case "like":
                raise NotImplementedError("Like activity is not implemented yet.")
                result = like(target=target.actor, activity=activity)
            case "undo":
                raise NotImplementedError("Undo activity is not implemented yet.")
                result = undo(target=target.actor, activity=activity)
            case _:
                error = f"InboxView: Unsupported activity: {activity.type}"
                logger.error(f"Actvity error: {error}")
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        # Return a success response. Unclear, why.

        return Response(
            data=result,
            status=status,
            content_type="application/activity+json",
        )

    def get(self, request, *args, **kwargs):
        """
        Return an `py:class`:`fedkit.models.Actor` Inbox.

        :py:meth:`webapp.tests.inbox.InboxTest.test_user_inbox` tests it.
        """

        actor = self.get_object()

        assert request.method == "GET"
        assert request.path == urlparse(actor.inbox).path

        if request.accepted_renderer.format == "html":
            data = {"object": actor}
            return Response(
                data, template_name=self.template_name, content_type="text/html"
            )

        data = self.serializer_class(instance=actor).data
        return Response(
            data,
            content_type="application/activity+json",
            status=status.HTTP_404_NOT_FOUND,
        )  # ; profile="https://www.w3.org/ns/activitystreams"')
