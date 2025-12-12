from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import response, status

from fedkit.models import Action
from fedkit.serializers import ActionSerializer
from fedkit.views.activity import ActivityBaseView


class OutboxView(ActivityBaseView):
    """
    5.1 Outbox
    The outbox is a list of all activities that an actor has published. The
    outbox is a collection of activities. The outbox is ordered by the
    published property of each activity, from the most recently published
    to the oldest published. The outbox is paginated, with the most recent
    items first. The outbox is a subtype of OrderedCollection.

    https://www.w3.org/TR/activitypub/#outbox
    """

    template_name = "fedkit/outbox.html"

    def get(self, request, *args, **kwargs):
        """
        Retrieve the activity stream of the actor's `outbox`_.

        .. _outbox: https://www.w3.org/TR/activitypub/#outbox

        """

        page = request.GET.get("page", None)
        actor = self.get_object()

        activity_list = Action.objects.filter(actor_object_id=self.get_object().id)
        paginator = Paginator(activity_list, 10)

        activity_stream = {
            "id": f"{actor.outbox}",
            "totalItems": activity_list.count(),
        }

        if not page:  # Ordered Collection
            activity_stream.update({"type": "OrderedCollection"})
            activity_stream.update({"first": f"{actor.outbox}?page=1"})
        else:
            try:
                page = int(page)
            except ValueError:
                raise Http404("Page parameter must be a number")
            if page > paginator.num_pages or page < 1:
                raise Http404("Page not found")
            activity_stream.update({"type": "OrderedCollectionPage"})
            if page > 1:
                activity_stream.update({"prev": f"{actor.outbox}?page={int(page) - 1}"})
            if page < paginator.num_pages:
                activity_stream.update({"next": f"{actor.outbox}?page={int(page) + 1}"})
            activity_stream.update(
                {"last": f"{actor.outbox}?page={paginator.num_pages}"}
            )
            activity_stream.update({"first": f"{actor.outbox}?page=1"})
            activity_stream.update(
                {
                    "orderedItems": [
                        ActionSerializer(item).data for item in activity_list
                    ]
                }
            )

        if "html" in request.accepted_renderer.format:
            if not self.template_name:
                raise Http404("Template not found")
            data = {"object": activity_stream}
            return response.Response(
                data, template_name=self.template_name, content_type="text/html"
            )

        return response.Response(
            activity_stream,
            content_type="application/activity+json",
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        """
        Create a new activity and add it to the actor's `outbox`_.

        .. _outbox: https://www.w3.org/TR/activitypub/#outbox

        .. todo::
          - Implement ActivityPub outbox post method
          - Validate incoming activity data
          - Handle errors gracefully
          - Implement permissions

          -
        .. seealso::
          - :meth:`fedkit.views.outbox.OutboxView.get`
        """
        # actor = self.get_object()
        # activity = Activity.objects.create(actor=actor, type="Create")
        # activity.save()
        # activity_response = activity.to_json()
        return response.Response(
            {}, content_type="application/activity+json", status=status.HTTP_201_CREATED
        )
