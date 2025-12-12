#!/usr/bin/python3
"""
(De-)Serializers for `Note` ActivityPub Objects.
"""

from rest_framework import serializers


class NoteSerializer(serializers.Serializer):
    """
    A Note ActivityPub Object.
    """

    def validate_note(value):
        if value != "Note":
            raise serializers.ValidationError('Not a "Note"')

    # Required properties
    type = serializers.CharField(required=True, validators=[validate_note])
    content = serializers.CharField(required=True)

    # Optional properties
    id = serializers.URLField(required=False)
    name = serializers.CharField(required=False)
    mediaType = serializers.CharField(required=False)
    published = serializers.DateTimeField(required=False)
    url = serializers.URLField(required=False)
    attributedTo = serializers.URLField(required=False)
    inReplyTo = serializers.URLField(required=False)
    to = serializers.ListField(child=serializers.URLField(), required=False)
    cc = serializers.ListField(child=serializers.URLField(), required=False)
    attachment = serializers.ListField(child=serializers.URLField(), required=False)
    tag = serializers.ListField(child=serializers.CharField(), required=False)
    generator = serializers.URLField(required=False)
    context = serializers.URLField(required=False)
    source = serializers.URLField(required=False)
    preview = serializers.URLField(required=False)
    icon = serializers.URLField(required=False)
    image = serializers.URLField(required=False)
    location = serializers.URLField(required=False)
    duration = serializers.DurationField(required=False)
    startTime = serializers.DateTimeField(required=False)
    endTime = serializers.DateTimeField(required=False)
    sensitive = serializers.BooleanField(required=False)
    summary = serializers.CharField(required=False)
    contentMap = serializers.DictField(child=serializers.CharField(), required=False)
    inReplyToNote = serializers.URLField(required=False)
    replies = serializers.URLField(required=False)
    likes = serializers.URLField(required=False)
    shares = serializers.URLField(required=False)
    audience = serializers.URLField(required=False)
