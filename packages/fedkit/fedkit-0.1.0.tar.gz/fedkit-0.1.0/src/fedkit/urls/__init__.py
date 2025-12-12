#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4
# pylint: disable=invalid-name

"""
urls_activity.py.

urls necessary to make all social views work.

"""

import logging

from django.urls import include, path
from django.views.generic import TemplateView


from fedkit.views import ActorView  # NoteView,
from fedkit.views import (ActionView, FollowersView, FollowingView,
                          GlobalInboxView, InboxView, LikedView, NodeInfoView,
                          OutboxView, StreamingView, TimelineView, VersionView,
                          WebFingerView)

logger = logging.getLogger(__name__)

app_name = "fedkit"

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='fedkit/index.html')),
]

urlpatterns += [
    # /.well-known/nodeinfo
    path(".well-known/nodeinfo", NodeInfoView.as_view(), name="nodeinfo"),
    path(".well-known/webfinger", WebFingerView.as_view(), name="webfinger"),
    path("api/v1/version", VersionView.as_view(), name="version"),
    path("api/v1/timeline", TimelineView.as_view(), name="timeline"),
    path("api/v1/streaming", StreamingView.as_view(), name="streaming"),
    path("inbox", GlobalInboxView.as_view(), name="global-inbox"),
    path(
        r"@<slug:slug>",
        ActorView.as_view(),
        name="actor-view",
    ),
    path(
        r"@<slug:slug>/inbox",
        InboxView.as_view(),
        name="actor-inbox",
    ),
    path(
        r"@<slug:slug>/outbox",
        OutboxView.as_view(),
        name="actor-outbox",
    ),
    path(
        r"@<slug:slug>/followers",
        FollowersView.as_view(),
        name="actor-followers",
    ),
    path(
        r"@<slug:slug>/following",
        FollowingView.as_view(),
        name="actor-following",
    ),
    path(
        r"@<slug:slug>/liked",
        LikedView.as_view(),
        name="actor-liked",
    ),
]

urlpatterns += [
    #     path(r"note/<uuid:pk>", NoteView.as_view(), name="note-detail"),
    path(r"action/<uuid:pk>", ActionView.as_view(), name="action_detail"),
]

urlpatterns += [
    path(r"web/", include("fedkit.urls.web")),
]
