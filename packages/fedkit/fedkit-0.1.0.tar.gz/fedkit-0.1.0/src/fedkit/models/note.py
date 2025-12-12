import logging
import uuid

from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .actor import Actor

logger = logging.getLogger(__name__)


class Note(models.Model):
    """
    Activity Streams 2.0

    .. Type: Note

    .. seealso::
        Activity `Extended Type Note <https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note>`_  # noqa: E501
    """

    class Meta:
        verbose_name = _("Note (Activity Streams 2.0)")
        verbose_name_plural = _("Notes (Activity Streams 2.0)")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    remoteID = models.URLField(blank=True, null=True, db_index=True)

    content = models.TextField()
    attributedTo = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True)
    contentMap = models.JSONField(blank=True, null=True)

    published = models.DateTimeField(default=now, db_index=True)
    updated = models.DateTimeField(default=now, db_index=True)

    public = models.BooleanField(default=True, db_index=True)
    sensitive = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("note-detail", args=[self.id])

    @property
    def type(self):
        return "Note"

    @property
    def summary(self):
        return self.summary
