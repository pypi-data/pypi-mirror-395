"""
fedapp/signature.py

This module contains two main functions, an signature checker for incoming
requests, and a function to make signed requests to the fediverse.

https://github.com/HelgeKrueger/bovine/blob/4ba2a83d1b4104ebffaaca357fbc9c225ffb06bf/bovine/bovine/utils/signature_checker.py
and
https://github.com/HelgeKrueger/bovine/blob/4ba2a83d1b4104ebffaaca357fbc9c225ffb06bf/bovine/bovine/utils/signature_parser.py

https://github.com/christianp/django-activitypub-bot/blob/main/bot/send_signed_message.py
"""

import base64
import hashlib
import json
import logging
import traceback
from datetime import datetime, timedelta, timezone, UTC

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519, padding
from cryptography.hazmat.primitives.serialization import (load_pem_private_key,
                                                          load_pem_public_key)
from django.http import HttpRequest

from .fedkit_typing import method, url
from .validators import validate_uri

logger = logging.getLogger(__name__)


class HttpSignature:
    def __init__(self):
        self.fields = []

    def build_message(self):
        return "\n".join(f"{name}: {value}" for name, value in self.fields)

    def build_signature(self, key_id, private_key):
        message = self.build_message()

        signature_string = sign_message(private_key, message)
        # headers = "(request-target) " + " ".join(
        #    name for name, _ in self.fields
        # )

        headers = " ".join(name for name, _ in self.fields)

        signature_parts = [
            f'keyId="{key_id}"',
            'algorithm="rsa-sha256"',  # todo: other algorithm support
            f'headers="{headers}"',
            f'signature="{signature_string}"',
        ]

        return ",".join(signature_parts)

    def verify(self, public_key, signature):
        message = self.build_message()
        public_key_loaded = load_pem_public_key(public_key.encode("utf-8"))

        try:
            public_key_loaded.verify(
                base64.standard_b64decode(signature),
                message.encode("utf-8"),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        except InvalidSignature:
            logger.warning("Could not verify signature")
            return False
        return True
        # return verify_signature(public_key, message, signature)

    def with_field(self, field_name, field_value):
        self.fields.append((field_name, field_value))
        return self

    """
    def ed25519_sign(self, private_encoded):
        private_bytes = multicodec.unwrap(multibase.decode(private_encoded))[1]
        private_key = (  # noqa: BLK100
            ed25519.Ed25519PrivateKey.from_private_bytes(  # noqa: E501
                private_bytes
            )
        )

        message = self.build_message()

        return multibase.encode(
            private_key.sign(message.encode("utf-8")), "base58btc"
        )

    def ed25519_verify(self, didkey, signature):
        public_key = did_key_to_public_key(didkey)

        signature = multibase.decode(signature)

        message = self.build_message().encode("utf-8")

        return public_key.verify(signature, message)
    """


def digest_sha256(content: str) -> str:
    """
    Create a sha-256 digest of the content string.
    """
    if isinstance(content, str):
        content_buffer = content.encode("utf-8")

    digest = base64.standard_b64encode(hashlib.sha256(content_buffer).digest()).decode(
        "utf-8"
    )
    return "SHA-256=" + digest


def getPrivateKey(key_id: str) -> str:
    """
    Get the private key for a given key_id
    """
    from fedkit.models import Actor

    try:
        if len(key_id.split("#")) == 2:
            actor_id, key = key_id.split("#")
        elif len(key_id.split("#")) == 1:
            actor_id = key_id
    except ValueError:
        RuntimeError(f"Could not split key_id {key_id}")

    assert validate_uri(actor_id)

    return Actor.objects.get(id=actor_id).private_key_pem


def signedRequest(
    method: method, url: url, message: dict, key_id: str, headers: dict = {}
) -> requests.PreparedRequest:
    """
    Wrapper around requests.method to sign a request with
    a private key for the fediverse

    Fields to sign:
        host date digest content-type

    :param method: The HTTP method
    :param url: The URL to send the request to
    :param message: The message to send in JSON LD
    :param key_id: The private key_id to sign the message with

    :return: The signed request

    https://docs.python-requests.org/en/latest/user/advanced/

    Example:

    """
    from urllib.parse import urlparse

    assert isinstance(message, dict)
    message_string = json.dumps(message)

    private_key = getPrivateKey(key_id=key_id)
    headers = {} if headers is None else headers

    host = urlparse(url).hostname  # req.headers.get("host")
    target = urlparse(url).path
    logger.debug(f"host: {host} of {url}")

    digest = digest_sha256(message_string)
    logger.debug(f"digest: {digest}")

    date = datetime.now(UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
    logger.debug(f"date: {date}")

    content_type = "application/activity+json"
    accept = "application/activity+json"

    signature = (
        HttpSignature()
        .with_field("(request-target)", f"post {target}")
        .with_field("host", host)
        .with_field("date", date)
        .with_field("digest", digest)
        .with_field("content-type", content_type)
        .build_signature(key_id, private_key)
    )
    headers.update(
        {
            "accept": accept,
            "host": host,
            "date": date,
            "digest": digest,
            "content-type": content_type,
            "signature": signature,
        }
    )

    match method:
        case "POST":
            request = requests.Request(
                "POST", url, data=message, headers=headers
            ).prepare()
        case "GET":
            assert message == {}
            request = requests.Request("GET", url, headers=headers).prepare()
        case _:
            raise ValueError(f"Unsupported method {method}")
    return request


def did_key_to_public_key(did):
    """
    .. todo::
        this is the only place in which multiformats are being used.
        Can we remove this dependency?
    """
    from multiformats import multibase, multicodec

    assert did.startswith("did:key:")
    decoded = multibase.decode(did[8:])
    codec, key_bytes = multicodec.unwrap(decoded)
    assert codec.name == "ed25519-pub"

    return ed25519.Ed25519PublicKey.from_public_bytes(key_bytes)


def parse_gmt(date_string: str) -> datetime:
    from dateutil.parser import parse

    return parse(date_string)


def check_max_offset_now(dt: datetime, minutes: int = 5) -> bool:
    now = datetime.now(tz=timezone.utc)

    if dt > now + timedelta(minutes=minutes):
        return False

    if dt < now - timedelta(minutes=minutes):
        return False

    return True


def sign_message(private_key, message):
    key = load_pem_private_key(private_key.encode("utf-8"), password=None)

    return base64.standard_b64encode(
        key.sign(
            message.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    ).decode("utf-8")


class Signature(object):
    def __init__(self, key_id: str, algorithm: str, headers: str, signature: str):
        self.key_id = key_id
        self.algorithm = algorithm
        self.headers = headers
        self.signature = signature

        if self.algorithm not in ["rsa-sha256", "hs2019"]:
            logger.error(f"Unsupported algorithm {self.algorithm}")
            logger.debug(self.signature)
            logger.debug(self.headers)
            logger.debug(self.key_id)

            raise Exception(f"Unsupported algorithm {self.algorithm}")

    def fields(self):
        return self.headers.split(" ")

    @staticmethod
    def from_signature_header(header):
        try:
            headers = header.split(",")
            headers = [x.split('="', 1) for x in headers]
            parsed = {x[0]: x[1].replace('"', "") for x in headers}

            return Signature(
                parsed["keyId"],
                parsed.get("algorithm", "rsa-sha256"),
                parsed["headers"],
                parsed["signature"],
            )
        except Exception:
            logger.error(f"failed to parse signature {header}")


class SignatureChecker:
    """
    Class to check the signature of a Django HttpRequest.

    The class is initialized with a key retriever function that is used to
    retrieve the public key of the actor that signed the request.

    """

    def __init__(self):
        from fedkit.tasks import fetchRemoteActor

        self.key_retriever = fetchRemoteActor

    def validate(self, request: HttpRequest, digest=None):
        if "signature" not in request.headers:
            """
            This is a request without a signature.

            .. todo::
                Eventually raise an Exception here?
            """
            logger.debug("Signature not present")
            return None

        if digest is not None:
            request_digest = request.headers["digest"]
            request_digest = request_digest[:4].lower() + request_digest[4:]
            if request_digest != digest:
                logger.error("Different digest")
                return None

        try:
            http_signature = HttpSignature()
            parsed_signature = Signature.from_signature_header(
                request.headers["signature"]
            )
            logger.debug(request.headers["signature"])
            signature_fields = parsed_signature.fields()

            if (
                "(request-target)" not in signature_fields
                or "date" not in signature_fields
            ):
                logger.error("Required field not present in signature")
                return "Required field not present in signature"

            if digest is not None and "digest" not in signature_fields:
                logger.error("Digest not present, but computable")
                return "Digest not present, but computable"

            http_date = parse_gmt(request.headers["date"])
            if not check_max_offset_now(http_date):
                logger.error(f"Found too old date {request.headers['date']}")
                return f"Found too old date {request.headers['date']}"

            for field in signature_fields:
                if field == "(request-target)":
                    m = request.method or ""
                    method = "" if m is None else m.lower()
                    # parsed_url = urlparse(request.url)
                    # path = parsed_url.path
                    path = request.path
                    http_signature.with_field(field, f"{method} {path}")
                else:
                    http_signature.with_field(field, request.headers[field])

            public_key = self.key_retriever(parsed_signature.key_id).get("publicKey")[
                "publicKeyPem"
            ]

            if public_key is None:
                logger.error(
                    f"Could'nt retrieve key for {parsed_signature.key_id}"
                )
                return f"Could'nt retrieve key for {parsed_signature.key_id}"

            if http_signature.verify(public_key, parsed_signature.signature):
                return parsed_signature.key_id

        except Exception as e:
            logger.debug(str(e))
            logger.debug(request.headers)
            for log_line in traceback.format_exc().splitlines():
                logger.debug(log_line)
            return e
