"""
Has been used for debugging purposes.
Can possibly be deprecated.
"""

import logging

from django.http import Http404
from django.utils.http import parse_header_parameters
from rest_framework import exceptions
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.settings import api_settings

logger = logging.getLogger(__name__)


def media_type_matches(lhs, rhs):
    """
    Returns ``True`` if the media type in the first argument <= the
    media type in the second argument.  The media types are strings
    as described by the HTTP spec.

    Valid media type strings include:

    'application/json; indent=4'
    'application/json'
    'text/*'
    '*/*'
    """
    lhs = _MediaType(lhs)
    rhs = _MediaType(rhs)
    logger.debug(f"5. lhs: {lhs}, rhs: {rhs}")
    match = lhs.match(rhs)
    logger.debug(f"6. match: {match}")
    return match


def order_by_precedence(media_type_lst):
    """
    Returns a list of sets of media type strings, ordered by precedence.
    Precedence is determined by how specific a media type is:

    3. 'type/subtype; param=val'
    2. 'type/subtype'
    1. 'type/*'
    0. '*/*'
    """
    ret = [set(), set(), set(), set()]
    for media_type in media_type_lst:
        precedence = _MediaType(media_type).precedence
        ret[3 - precedence].add(media_type)
    return [media_types for media_types in ret if media_types]


class _MediaType:
    def __init__(self, media_type_str):
        self.orig = "" if (media_type_str is None) else media_type_str
        self.full_type, self.params = parse_header_parameters(self.orig)
        self.main_type, sep, self.sub_type = self.full_type.partition("/")
        logger.error(f"MediaType: {self.orig}")
        logger.error(f"MediaType full-type: {self.full_type}")
        logger.error(f"MediaType partitioned: {self.main_type} {sep} {self.sub_type}")

    def match(self, other):
        """Return true if this MediaType satisfies the given MediaType."""
        for key in self.params:
            if key != "q" and other.params.get(key, None) != self.params.get(key, None):
                return False

        if (
            self.sub_type != "*"
            and other.sub_type != "*"
            and other.sub_type != self.sub_type
        ):
            return False

        if (
            self.main_type != "*"
            and other.main_type != "*"
            and other.main_type != self.main_type
        ):
            return False

        return True

    @property
    def precedence(self):
        """
        Return a precedence level from 0-3 for the media type given how specific it is.
        """
        if self.main_type == "*":
            return 0
        elif self.sub_type == "*":
            return 1
        elif not self.params or list(self.params) == ["q"]:
            return 2
        return 3

    def __str__(self):
        ret = "%s/%s" % (self.main_type, self.sub_type)
        for key, val in self.params.items():
            ret += "; %s=%s" % (key, val)
        return ret


class WebappContentNegotiation(DefaultContentNegotiation):
    """
    WebappContentNegotiation

    """

    settings = api_settings

    def select_parser(self, request, parsers):
        parser = super().select_parser(request, parsers)
        logger.error("WebappContentNegotiation.select_parser")
        logger.error("request: " + str(request))
        logger.error("request.headers: " + str(request.headers))
        logger.error("parsers: " + str(parsers))
        if request.path.startswith("/@"):
            logger.error(
                f"Parser selected: {parser} for 'Content-Type: {request.headers.get('content-type')}' (Available: {parsers})"
            )
        return parser

    def get_accept_list(self, request):
        """
        Given the incoming request, return a
        tokenized list of media type strings.
        """
        header = request.META.get("HTTP_ACCEPT", "*/*")
        return [token.strip() for token in header.split(",")]

    def filter_renderers(self, renderers, format):
        """
        If there is a '.json' style format suffix, filter the renderers
        so that we only negotiation against those that accept that format.
        """
        renderers = [renderer for renderer in renderers if renderer.format == format]
        if not renderers:
            raise Http404
        return renderers

    def select_renderer(self, request, renderers, format_suffix):
        """
        Given a request and a list of renderers, return a two-tuple of:
        (renderer, media type).
        """
        # Allow URL style format override.  eg. "?format=json
        format_query_param = self.settings.URL_FORMAT_OVERRIDE
        format = format_suffix or request.query_params.get(format_query_param)

        if format:
            renderers = self.filter_renderers(renderers, format)

        accepts = self.get_accept_list(request)
        logger.debug("1. Accept list: %s", accepts)

        # Check the acceptable media types against each renderer,
        # attempting more specific media types first
        # NB. The inner loop here isn't as bad as it first looks :)
        #     Worst case is we're looping over len(accept_list) * len(self.renderers)
        for media_type_set in order_by_precedence(accepts):
            logger.debug("2. Media type set: %s", media_type_set)
            for renderer in renderers:
                logger.debug("3. Trying for Renderer: %s", renderer)
                for media_type in media_type_set:
                    logger.debug(f"4. {media_type} is in {media_type_set}")
                    if media_type_matches(renderer.media_type, media_type):
                        logger.debug(f"7. {media_type} matches {renderer.media_type}")
                        # Return the most specific media type as accepted.
                        media_type_wrapper = _MediaType(media_type)
                        if (
                            _MediaType(renderer.media_type).precedence
                            > media_type_wrapper.precedence
                        ):
                            # Eg client requests '*/*'
                            # Accepted media type is 'application/json'
                            full_media_type = ";".join(
                                (renderer.media_type,)
                                + tuple(
                                    f"{key}={value}"
                                    for key, value in media_type_wrapper.params.items()
                                )
                            )
                            return renderer, full_media_type
                        else:
                            # Eg client requests 'application/json; indent=8'
                            # Accepted media type is 'application/json; indent=8'
                            return renderer, media_type
        raise exceptions.NotAcceptable(available_renderers=renderers)

        # if request.path.startswith("/@"):
        #     logger.error(f"selected_renderer: {selected_renderer} for 'Accept: {request.headers.get('accept')}'")
