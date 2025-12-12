#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4
# pylint: disable=invalid-name

"""
Activitypub related models for `Angry Planet Cloud`.

Specifically:
    - Action

"""

import logging
import uuid

from django.contrib.contenttypes.fields import \
    GenericForeignKey  # type: ignore
from django.contrib.contenttypes.models import ContentType  # type: ignore
from django.db import models  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils.timezone import now  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore

from ..managers import ActionManager

logger = logging.getLogger(__name__)


def get_activity_types():
    """
    Activity Streams 2.0 Abstraction Layer for Activity Types
    """
    from fedkit.schema import ACTIVITY_TYPES

    return ACTIVITY_TYPES


class Action(models.Model):
    """
    Activity Streams 2.0

    Inp
    https://github.com/justquick/django-activity-stream/blob/main/actstream/models.get_profile_types
    """

    objects = ActionManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default=now, db_index=True)
    public = models.BooleanField(default=True, db_index=True)

    actor_content_type = models.ForeignKey(
        ContentType,
        related_name="actor",
        on_delete=models.CASCADE,
        db_index=True,
    )
    actor_object_id = models.CharField(max_length=255, db_index=True)
    actor = GenericForeignKey("actor_content_type", "actor_object_id")

    activity_type = models.CharField(
        max_length=255, db_index=True, choices=get_activity_types
    )

    description = models.TextField(blank=True, null=True)

    target_content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target",
        on_delete=models.CASCADE,
        db_index=True,
    )
    target_object_id = models.CharField(
        max_length=255, blank=True, null=True, db_index=True
    )
    target = GenericForeignKey("target_content_type", "target_object_id")

    action_object_content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="action_object",
        on_delete=models.CASCADE,
        db_index=True,
    )
    action_object_object_id = models.CharField(
        max_length=255, blank=True, null=True, db_index=True
    )
    action_object = GenericForeignKey(
        "action_object_content_type", "action_object_object_id"
    )

    timestamp = models.DateTimeField(default=now, db_index=True)

    public = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        result = ""
        details = {
            "actor": str(self.actor),
            "verb": self.activity_type,  # should be action_type
            "target": str(self.target),
            "action_object": str(self.action_object),
            "since": self.since(),
        }
        if self.target:
            if self.action_object:
                result = _(
                    f"{details['actor']} {details['verb']} {details['action_object']} on {details['target']} {details['since']}s ago"  # noqa: E501
                )
            result = _(
                f"{details['actor']} {details['verb']} {details['target']} {details['since']}s ago"
            )
        if self.action_object:
            result = _(
                f"{details['actor']} {details['verb']} {details['action_object']} {details['since']}s ago"  # noqa: E501
            )
        result = _(
            f"{self.actor} {self.activity_type}"
        )  # _(f"{self.actor} {self.verb} {self.since} ago")
        return str(result)

    def since(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince

        return (
            timesince(self.timestamp, now)
            .encode("utf8")
            .replace(b"\xc2\xa0", b" ")
            .decode("utf8")
        )

    def get_absolute_url(self):
        return reverse("action_detail", args=[self.pk])

    @property
    def activity_id(self):
        from django.contrib.sites.models import Site

        base = f"https://{Site.objects.get_current().domain}"
        return f"{base}{self.get_absolute_url()}"
