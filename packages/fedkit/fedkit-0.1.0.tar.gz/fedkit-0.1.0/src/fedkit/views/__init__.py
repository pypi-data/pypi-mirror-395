"""
:py:module:`webapp.views.activitypub` -- ActivityPub API views

This module contains the views for the ActivityPub API.

The primary goal is to implement server-to-server communication, with
later plans to implement client-to-server communication.

The module contains acompanies views to use the ActivityPub API,
such as NodeInfo and WebFinger.

The views are designed to be used with Django's class-based views.

W3C ActivityPub is a protocol for federated social networking
based on the ActivityStreams 2.0 data format.

.. seealso::
    `W3C ActivityPub <https://www.w3.org/TR/activitypub/>`_
    `W3C ActivityStreams 2.0 <https://www.w3.org/TR/activitystreams-core/>`_
"""

# System
from .nodeinfo import NodeInfoView, VersionView
from .streaming import StreamingView
from .timelines import TimelineView

__all__ = ["NodeInfoView", "StreamingView", "TimelineView", "VersionView"]


from .action import ActionView
# ActivityPub
from .actor import ActorView
from .followers import FollowersView
from .following import FollowingView
from .globalinbox import GlobalInboxView
from .inbox import InboxView
from .liked import LikedView
from .outbox import OutboxView
# WebFinger
from .webfinger import WebFingerView

__all__ += [
    "WebFingerView",
]

__all__ = [
    "ActorView",
    "FollowersView",
    "FollowingView",
    "InboxView",
    "LikedView",
    "OutboxView",
]
__all__ += [
    "ActionView",
]

__all__ += [
    "GlobalInboxView",
]
