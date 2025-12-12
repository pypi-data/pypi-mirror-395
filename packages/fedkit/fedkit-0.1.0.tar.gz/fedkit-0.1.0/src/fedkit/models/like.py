import uuid

from django.db import models

from ..validators import validate_iri
from .actor import Actor


class Like(models.Model):
    """
    Like model

    Store the like information of an actor to an object

    :param actor: The actor who likes the object
    :type actor: Actor
    :param object: The object that is liked
    :type object: str
    :param created_at: The date and time when the like is created
    :type created_at: datetime

    .. seealso::
        `W3C ActivityStreams Like <https://www.w3.org/ns/activitystreams#Like>`_  # noqa

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    object = models.URLField(validators=[validate_iri])
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("like-detail", kwargs={"pk": self.id})
