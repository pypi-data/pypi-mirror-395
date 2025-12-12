from django.core.paginator import Paginator
from django.http import Http404
from rest_framework.response import Response

from fedkit.views.activity import ActivityBaseView


class FollowingView(ActivityBaseView):
    """
    Provide a list of who this profile is following.

    ```
    Every actor SHOULD have a following collection. This is a list of
    everybody that the actor has followed, added as a side effect. The
    following collection MUST be either an OrderedCollection or a Collection
    and MAY be filtered on privileges of an authenticated user or as
    appropriate when no authentication is given.
    ```

    .. note::
         The reverse for this view is `actor-following`.
         The URL pattern `/accounts/<slug:slug>/following/`

    .. seealso::
        The `W3C following definition:
        `5.4 Following Collection <https://www.w3.org/TR/activitypub/#following>`_
    """

    template_name = "activitypub/following.html"

    def get_queryset(self):
        from fedkit.models import Follow

        return Follow.objects.filter(actor=self.get_object()).order_by("accepted")

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page", None)
        paginator = Paginator(self.get_queryset(), 10)

        if request.accepted_renderer.format == "html":
            return Response(
                {"object_list": self.get_queryset()},
                template_name=self.template_name,
                content_type="text/html",
            )

        activity_result = {
            "id": f"{self.get_object().following}",
            "totalItems": self.get_queryset().count(),
            "type": "OrderedCollection",
        }

        if not page:
            activity_result.update({"first": f"{self.get_object().following}?page=1"})
            return Response(activity_result, content_type="application/activity+json")

        try:
            page = int(page)
        except ValueError:
            raise Http404("Page parameter must be a number")
        if page > paginator.num_pages or page < 1:
            raise Http404("Page not found")
        activity_result.update(
            {
                "id": f"{self.get_object().following}?page={page}",
                "type": "OrderedCollectionPage",
                "partOf": f"{self.get_object().following}",
            }
        )
        if page > 1:
            activity_result.update(
                {"prev": f"{self.get_object().following}?page={int(page) - 1}"}
            )
        if page < paginator.num_pages:
            activity_result.update(
                {"next": f"{self.get_object().following}?page={int(page) + 1}"}
            )
        activity_result.update(
            {"orderedItems": [f"{item.id}" for item in self.get_queryset()]}
        )

        return Response(activity_result, content_type="application/activity+json")
