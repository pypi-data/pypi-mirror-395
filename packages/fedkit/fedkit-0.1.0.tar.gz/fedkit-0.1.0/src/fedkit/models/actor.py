#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4
# pylint: disable=invalid-name

"""
Activitypub models for `Angry Planet Cloud`.

"""

import logging
import uuid
from functools import cached_property

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..exceptions import RemoteActorError
from ..validators import validate_iri

logger = logging.getLogger(__name__)
User = get_user_model()

def get_actor_types():
    """
    Activity Streams 2.0 Abstraction Layer for Activity Types
    """
    ACTOR_TYPES = {
        "Application": _("Application"),
        "Group": _("Group"),
        "Organization": _("Organization"),
        "Person": _("Person"),
        "Service": _("Service"),
    }
    return ACTOR_TYPES


class Actor(models.Model):
    """
    Activity Streams 2.0 - Actor

    :py:class:fedkit.models:Actor objects **MUST** have, in
    addition to the properties mandated by `Object Identifiers <https://www.w3.org/TR/activitypub/#obj-id>`_,  # noqa: E501
    the following properties:


    - `actorID` -  A unique `URL` for the `Actor`. The `id` property is *REQUIRED*
        for `Actor` objects.
    - `inbox` - A link to an `OrderedCollection` of `Activities` that this
        `Actor` has received, typically from clients. The `inbox` property is
        *REQUIRED* for `Actor` objects.
    - `outbox` - A link to an `OrderedCollection` of `Activities` that this
        `Actor` has published, such as `Posts`, `Comments`, etc. The `outbox`
        property is *REQUIRED* for `Actor` objects.

        - `followers` - A link to an `OrderedCollection` of `actors` that are
        `following` this `actor`. The `followers` property is *OPTIONAL* for
        `Actor` objects.

        - `following` - A link to an `OrderedCollection` of `actors` that this
        `actor` is `following`. The `following` property is *OPTIONAL* for
        `Actor` objects.

        - `liked` - A link to an `OrderedCollection` of `Objects` that this
        `actor` has `liked`. The `liked` property is *OPTIONAL* for `Actor`
        objects.

        - `follows` - a django `ManyToManyField` relationship to `self` that
        stores any `actors` that this `actor` is `follows`.

        - `followed_by` - a django `ManyToManyField` relationship to `self` that
        stores any `actors` that are `following` this `actor`.


    .. seealso::
        The definition of W3C ActivityPub `Actor Objects <https://www.w3.org/TR/activitypub/#actor-objects>`_

    .. testsetup::

        from fedkit.models.actor import Actor

    The model persists the `Actor` object in the database. The `Actor` object
    provides all the necessary properties to interact with the
    `Activity Streams 2.0` specification. Just like with regualar Django
    objects, you can create, update, delete and query `Actor` objects:

    .. doctest::

        Actor.objects.create(id='https://example.com/actor')
        Actor.objects.create(id='https://example.com/other')
        actor = Actor.objects.get(id='https://example.com/actor')
        other = Actor.objects.get(id='https://example.com/other')

    The `Actor` object will provide required and some optional properties:

    .. testcode::

        actor.id               # MUST
        actor.type             # MUST
        actor.inbox            # MUST
        actor.outbox           # MUST
        actor.following        # SHOULD
        actor.followers        # SHOULD
        actor.liked            # MAY
        actor.preferedUserName # MAY
        actor.preferedUsername # MAY

    This will produce the full url for the `inbox` of the actor:

    .. testoutput::

        'https://example.com/actor'

    The `Actor` object will provide required and some optional properties:

    .. testcode::
        actor.follows.add(other)
        actor.follows.all()

    This will add the `other` actor to the `follows` of the `actor`:

    .. testoutput::

        <QuerySet [<Actor: https://example.com/other>]>
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True
    )

    id = models.CharField(
        max_length=255,
        primary_key=True,
        unique=True,
        blank=False,
        validators=[validate_iri],
    )

    slug = models.SlugField(max_length=255, unique=True)

    preferredUsername = models.CharField(
        max_length=255,
        help_text=_("The preferred username of the actor."),
    )

    summary = models.TextField(help_text=_("Short Summary"))

    public_key_pem = models.TextField(help_text=_("Public Key"))
    private_key_pem = models.TextField(help_text=_("Private Key"))

    img = models.ImageField(
        upload_to="mediafiles/user/",
        default="/user/default.png",
    )
    gravatar = models.BooleanField(
        default=True, help_text=_("Use Gravatar profile image.")
    )

    type = models.CharField(max_length=255, default="Person", choices=get_actor_types)


    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True,
        through="Follow",
    )

    discoverable = models.BooleanField(
        default=True,
        help_text=_("Is this actor discoverable by other actors?"),
    )

    manuallyApprovesFollowers = models.BooleanField(
        default=False,
        help_text=_("Does this actor manually approve followers?"),
    )

    class Meta:
        verbose_name = _("Actor (Activity Streams 2.0)")
        verbose_name_plural = _("Actors (Activity Streams 2.0)")
        unique_together = ("id", "type", "user")

    def __str__(self):
        """
        Return the string representation of the object.
        """
        return str(self.id)

    def save(self, *args, **kwargs):
        """
        Save the actor with a slug based on the user's username.
        """
        from django.template.defaultfilters import slugify
        if not self.remote:
            self.slug = slugify(self.user.username)
        else:
            self.slug = slugify(self.id)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Return the absolute URL of this actor.
        Activity Streams 2.0
        """
        return reverse("actor-view", kwargs={"slug": str(self.user.username)})

    @cached_property
    def remote(self):
        """
        If this does not belong to a user, it is remote.
        """
        return self.user is None

    @property
    def publicKey(self) -> str:
        """
        The :py:class:Actor main public-key.

        .. todo::
            It should be moved to the Actor object.
        """
        if not self.remote:
            return f"{self.public_key_pem}"
        raise RemoteActorError("Remote actors do not have a public key.")

    @property
    def keyID(self) -> str:
        """
        The :py:class:Actor main key-id.

        .. todo::
            Implement a mechanism to keep other keys
            than the main key; and to rotate keys.
        """
        if not self.remote:
            return f"{self.id}#main-key"
        raise RemoteActorError("Remote actors do not have a key-id.")

    @cached_property
    def inbox(self):
        """
        :py:attr:inbox returns a link to an `OrderedCollection`

        Return the URL of the `inbox`, that contains an `OrderedCollection`.
        An `Inbox` is a `Collection` to which `Items` are added, typically by
        the `owner` of the `Inbox`. The `inbox` property is *REQUIRED* for
        `Actor` objects.

        :: return: URL
        :: rtype: str

        .. seealso::
            :py:class:`fedkit.views.inbox.InboxView`

        """
        if not self.remote:
            base = f"https://{Site.objects.get_current().domain}"
            return f"{base}" + reverse(
                "actor-inbox",
                args=[self.slug],
            )
        raise RemoteActorError("Remote actors do not have a local inbox.")

    @cached_property
    def outbox(self):
        """
        :py:attr:outbox returns a link to an `OrderedCollection`

        Return the URL of the outbox.

        :: return: URL
        :: rtype: str

        .. seealso::
            :py:class:`fedkit.views.outbox.OutboxView`
        """
        if not self.remote:
            base = f"https://{Site.objects.get_current().domain}"
            return f"{base}%s" % reverse(
                "actor-outbox",
                args=[self.slug],
            )
        raise RemoteActorError("Remote actors do not have a local outbox.")

    @property
    def followers(self):
        """
        `followers` will return the URL to an `OrderedCollection`, a
        collection of `actors` that are `following` this `actor`.

        :return: URL

        .. seealso::
            The view to serve this `OrderedCollection` is served by
            :py:class:`fedkit.views.followers.FollowersView`

        .. seealso:: Following the `Activity Streams 2.0` specification for
            `followers <https://www.w3.org/TR/activitypub/#actor-objects>`_,
            the `followers` property is OPTIONAL.


        """
        if not self.remote:
            base = f"https://{Site.objects.get_current().domain}"
            return f"{base}%s" % reverse(
                "actor-followers",
                args=[self.slug],
            )
        raise RemoteActorError("Remote actors do not have a local follower.")

    @property
    def following(self):
        """
        `following` returns a link to an `OrderedCollection`, a
        collection of `actors` that this `actor` is `following`.

        :return: URL
        :rtype: str

        .. seealso::
            The view to serve this `OrderedCollection` is served by
            :py:class:`fedkit.views.following.FollowingView`

        """
        if not self.remote:
            base = f"https://{Site.objects.get_current().domain}"
            return f"{base}%s" % reverse(
                "actor-following",
                args=[self.slug],
            )
        raise RemoteActorError("Remote actors do not have a local following.")


    @property
    def liked(self):
        """
        Following the definition of the `Activity Streams 2.0` specification,
        the `liked` property returns a link to a collection of `Objects` tha
        this `actor` has `liked`.

        Return the URL to the likes-collection.

        :: return: URL
        :: rtype: str

        """
        if not self.remote:
            base = f"https://{Site.objects.get_current().domain}"
            return f"{base}%s" % reverse(
                "actor-liked",
                args=[self.slug],
            )
        raise RemoteActorError("Remote actors do not have a local liked.")



class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="actor")
    object = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="object")
    accepted = models.URLField(blank=True, null=True, validators=[validate_iri])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def getID(self):
        from django.contrib.sites.models import Site

        base = f"https://{Site.objects.get_current().domain}"
        return f"{base}/{self.id}"

    def __str__(self):
        return f"{self.actor} follows {self.object}"
