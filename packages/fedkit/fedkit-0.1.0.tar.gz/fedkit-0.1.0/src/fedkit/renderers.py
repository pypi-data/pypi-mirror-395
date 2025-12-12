"""renderers.py

.. seealso:: https://www.w3.org/ns/activitystreams

.. seealso::
https://www.django-rest-framework.org/api-guide/renderers/#custom-renderers

Returns:
    _type_: _description_
"""

import logging

from rest_framework import renderers

logger = logging.getLogger(__name__)


class JrdRenderer(renderers.JSONRenderer):
    """
    JrdRenderer

    Accept: 'application/json' for WebFinger Requests.
    """

    media_type = "application/jrd+json"
    format = "jrd"


class JsonLDRenderer(renderers.JSONRenderer):
    """
    JsonLDRenderer

    Args:
        renderers (JsonLDRenderer): Renders JSON-LD data

    Returns:
        JsonLD: Added Context to JSON-LD data
    """

    media_type = "application/ld+json"
    format = "ld"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        assert isinstance(data, dict), "JsonLDRenderer.render expects a dict"
        # context = {"as": "https://www.w3.org/ns/activitystreams"}
        logger.debug("ActivityRenderer.render: media_type:" + str(accepted_media_type))

        data["@context"] = ["https://www.w3.org/ns/activitystreams"]
        if data.get("publicKey"):
            data["@context"].append("https://w3id.org/security/v1")

        logger.error(f"Data:\n\n{data}")
        logger.error("\n\n\n\n\n\n\n\n")

        try:
            from pyld import jsonld

            from .context import context

            undata = jsonld.compact(data, context)  # noqa: F841

        except ImportError:
            raise ImportError("JsonLDRenderer requires pyld")

        except jsonld.JsonLdError as e:
            logger.error(f"JsonLDRenderer failed to compact data: {e}")
            logger.error(f"data: {data}")
            # raise ValueError(f"JsonLDRenderer failed to compact data: {e}")

        if isinstance(data, dict):
            data = dict(sorted(data.items()))

        return super().render(data, accepted_media_type, renderer_context)


class ActivityRenderer(renderers.JSONRenderer):
    """
    ActivitypubRenderer
    """

    media_type = "application/activity+json"  # ; profile="https://www.w3.org/ns/activitystreams"'
    format = "activity"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        logger.debug("ActivityRenderer.render: media_type:" + str(accepted_media_type))

        data["@context"] = ["https://www.w3.org/ns/activitystreams"]
        if data.get("publicKey"):
            data["@context"].append("https://w3id.org/security/v1")

        return super().render(data, accepted_media_type, renderer_context)
