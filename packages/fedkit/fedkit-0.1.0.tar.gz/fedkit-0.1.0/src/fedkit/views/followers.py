from django.core.paginator import Paginator
from django.http import Http404
from rest_framework.response import Response

from fedkit.views.activity import ActivityBaseView


class FollowersView(ActivityBaseView):
    """
    Provide a list of followers for a given profile.

    Every actor SHOULD have a followers collection. This is a list of everyone
    who has sent a Follow activity for the actor, added as a side effect. This
    is where one would find a list of all the actors that are following the
    actor. The followers collection MUST be either an OrderedCollection or a
    Collection and MAY be filtered on privileges of an authenticated user or
    as appropriate when no authentication is given.

    .. note::
         The reverse for this view is `actor-followers`.
         The URL pattern `/accounts/<slug:slug>/followers/`

    .. seealso::
         The `W3C followers definition <https://www.w3.org/TR/activitystreams-vocabulary/#followers>`_.  # noqa

         `5.3 Followers Collection <https://www.w3.org/TR/activitypub/#followers>`_
    """

    template_name = "activitypub/followers.html"

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page", None)
        actor = self.get_object()
        followed_list = actor.followed_by.order_by("actor__followed_accepted")
        paginator = Paginator(followed_list, 10)

        if request.accepted_renderer.format == "html":
            return Response(
                {"object_list": followed_list},
                template_name=self.template_name,
                content_type="text/html",
            )

        activity_result = {
            "id": f"{actor.followed_by}",
            "totalItems": followed_list.count(),
            "type": "OrderedCollection",
        }

        if not page:
            activity_result.update({"first": f"{actor.followed_by}?page=1"})
            return Response(activity_result, content_type="application/activity+json")

        try:
            page = int(page)
        except ValueError:
            raise Http404("Page parameter must be a number")
        if page > paginator.num_pages or page < 1:
            raise Http404("Page not found")
        activity_result.update(
            {
                "id": f"{actor.following}?page={page}",
                "type": "OrderedCollectionPage",
                "partOf": f"{actor.followed_by}",
            }
        )
        if page > 1:
            activity_result.update(
                {"prev": f"{actor.followed_by}?page={int(page) - 1}"}
            )
        if page < paginator.num_pages:
            activity_result.update(
                {"next": f"{actor.followed_by}?page={int(page) + 1}"}
            )
        activity_result.update(
            {"orderedItems": [f"{item.id}" for item in followed_list]}
        )

        return Response(activity_result, content_type="application/activity+json")
