import logging

from rest_framework import status
from rest_framework.response import Response

from fedkit.serializers import ActorSerializer

from .activity import ActivityBaseView

logger = logging.getLogger(__name__)


class ActorView(ActivityBaseView):
    """
    Return the actor object for a given user.
    User is identified by the slug.

    :py:class:`fedkit.models.Actor` is the model that hosts the actor object.

    Example urlconf:
        ```
        path(r'@<slug:slug>', ActorView.as_view(), name='actor-view')
        ```

    If the request header contains 'application/ld+json' or
    'application/activity+json', the response will be in Activity Streams 2.0
    JSON-LD format.
    Otherwise, the response will be in json or html.

    The actor object is a JSON-LD object that represents the user.

    .. seealso::
        `W3C Actor Objects <https://www.w3.org/TR/activitypub/#actor-objects>`_

    .. seealso::
        :py:mod:`fedkit.urls.activitypub`

    """

    template_name = "activitypub/actor.html"
    serializer_class = ActorSerializer

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if request.accepted_renderer.format == "html":
            data = {"object": object}
            return Response(
                data, template_name=self.template_name, content_type="text/html"
            )

        data = self.serializer_class(instance=object).data
        return Response(
            data, content_type="application/activity+json", status=status.HTTP_200_OK
        )  # ; profile="https://www.w3.org/ns/activitystreams"')
