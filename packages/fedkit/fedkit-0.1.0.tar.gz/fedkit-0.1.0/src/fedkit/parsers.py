import logging

from rest_framework.parsers import JSONParser

logger = logging.getLogger(__name__)

"""
2025-06-15 20:50:08,917 ERROR
Parser selected: None for
{
'Host': 'pramari.de',
'X-Forwarded-For': '2a01:4f8:1c1c:8dfc::1, 169.254.1.1',
'X-Forwarded-Proto': 'https',
'Forwarded': 'for="[2a01:4f8:1c1c:8dfc::1]";proto=https',
'Content-Length': '213',
'User-Agent': 'bovine/0.5.7',
'Date': 'Sun, 15 Jun 2025 20:50:08 GMT',
'Digest': 'sha-256=HdFrMKSAWevwRudi5hhOmmLd3zxLiHAWIyMG8W1PrQ0=',
'Content-Type': 'application/activity+json',
'Signature': 'keyId="https://verify.funfedi.dev/frank#main",algorithm="rsa-sha256",headers="(request-target) host date digest content-type",signature="ehDwh9Z1gxzMHO3RvsjMWS2X8E4eteOohz2DltYK92GpZq8m+dx2ZXbVgMmoeTaMeiR78s6ryApqOq4r0UaNCjoVnRlw8bOP4JPGlqu1YEyrcdLiVxT4pB6uhlXN/1w75tzhTZobYsR2wHiiQimd/sZ4gjX7i4rgilyiAvrV+TNcKdIvtPd5S0VVtBjbXtHKX/1nnX9DWIsBAZdA55lnzdIDBTwcKzawUVi5ldzkOn9+qrnwnEHqXO3G6VXkTPa7vEqMAm1DxIcFrZHi7savhJp9fhztFEmTp7iGtv2EWQAD9lAK+jpwBjBSQuUH+ipVWtQN4GMhyKJCJvvTpCq7rg=="', 'Accept': '*/*', 'X-Cloud-Trace-Context': 'dda4ea7636d57b1f260733c42d54f176/16341754461370299733', 'X-Appengine-Citylatlong': '0.000000,0.000000', 'X-Appengine-Region': '?', 'X-Appengine-Country': 'DE', 'X-Appengine-City': '?', 'X-Google-Apps-Metadata': 'domain=gmail.com,host=pramari.de', 'X-Appengine-Default-Namespace': 'gmail.com', 'Traceparent': '00-dda4ea7636d57b1f260733c42d54f176-e2c99319aca1b555-00', 'X-Appengine-Timeout-Ms': '599999', 'X-Appengine-Https': 'on', 'X-Appengine-User-Ip': '2a01:4f8:1c1c:8dfc::1', 'X-Appengine-Api-Ticket': 'ChA4Y2IwMWViMTNmZmRjZjViEOaM8iEQ84zyIRDUuLcwEOG4tzAQjNPdMBCZ090wEIbM7zAQjMzvMBCb0vAwEKHS8DAQvdHzMBDD0fMwEPrc+jAQgN36MBCG8fswEIzx+zAQxJuNMRDLm40xEPfpkTEQ/umRMRCT0ZYxEJrRljEQmpeXMRChl5cxENGmmDEQ2KaYMRoTCISl+OWm9I0DFRebgwcdTXYCig==', 'Accept-Encoding': 'gzip, deflate', 'X-Appengine-Request-Log-Id': '684f3200ff00ff0d9284fbf5b4860001687e7072616d6172692d64650001323032353036313574323034363331000100', 'X-Appengine-Default-Version-Hostname': 'pramari-de.appspot.com'} (Available: [<fedkit.parsers.ActivityParser object at 0x3e86ce550860>, <fedkit.parsers.JsonLDParser object at 0x3e86ce552150>])
"""


class ActivityParser(JSONParser):
    """
    'application/activity+json' parser.
    """

    media_type = "application/activity+json"

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parse JSON-LD data.
        """
        result = super().parse(stream, media_type, parser_context)
        # This is now JSON-LD
        assert isinstance(result, dict)

        return result
