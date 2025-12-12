from django.http import JsonResponse
from django.views.generic import DetailView

from fedkit.models import Note


class NoteView(DetailView):
    """
    Boilerplate for ActivityPub Note view.

    A Note is a short written work, typically
    less than a single paragraph in length.

    This view will return a json-ld representation
    of the note if requested.

    .. seealso::
        :py:mod:fedkit.urls.activitypub
        `/action/<uuid:uuid>/`

    """

    model = Note
    template_name = "activitypub/note.html"

    def json_ld(self, request):
        """
        Return a json-ld representation of the note.
        """
        json_ld = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Note",
            "id": self.get_object().get_absolute_url(),
            "content": self.get_object().content,
            "published": self.get_object().published.isoformat(),
            "attributedTo": self.get_object().author.get_absolute_url(),
        }

        return JsonResponse(json_ld, content_type="application/ld+json")
