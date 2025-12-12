import json

from rest_framework.response import Response

from fedkit.views.activity import ActivityBaseView


class LikedView(ActivityBaseView):
    """
    View for handling the objects an actor liked.

    ```
    GET /liked/
    ```

    Every actor MAY have a liked collection. This is a list of every object
    from all of the actor's Like activities, added as a side effect. The
    liked collection MUST be either an OrderedCollection or a Collection
    and MAY be filtered on privileges of an authenticated user or as
    appropriate when no authentication is given.

    .. seealso::
        `ActivityPub Liked <https://www.w3.org/TR/activitypub/#liked>`_
    """

    template_name = "activitypub/liked.html"

    def liked(self):
        result = self.get_object().like_set.all()
        return result

    def get(self, request, *args, **kwargs):
        result = {
            "id": f"{self.get_object().liked}",
            "type": "Collection",
            "totalItems": 0,
            "items": [],
        }
        likes = self.liked().values_list("object", flat=True).order_by("-created_at")
        result.update({"totalItems": len(likes)})
        result.update({"items": json.dumps(list(likes))})
        if request.accepted_renderer.format == "html":
            return Response(
                result, template_name=self.template_name, content_type="text/html"
            )
        return Response(result, content_type="application/activity+json")
