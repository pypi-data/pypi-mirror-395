import functools
import ipaddress
import json
import logging
import socket
from typing import Tuple

from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from fedkit.activity import ActivityObject
from fedkit.models import Actor, Follow
from fedkit.signals import action
from fedkit.signature import signedRequest

from fedkit.validators import validate_uri

from fedkit.tasks.fetch import Fetch

__all__ = ["Fetch"]

logger = logging.getLogger(__name__)
User = get_user_model()






@shared_task
def fetchRemoteActor(id: str) -> Actor:
    """
    Task to get details for a remote actor

    .. todo::
        - Add caching
        - Add error handling
        - Add tests
    """
    actor = Fetch(id)
    return Actor(
        id=actor.get("id"),
        inbox=actor.get("inbox"),
        outbox=actor.get("outbox"),
        publicKey=actor.get("publicKey", ""),
    )


def signedFetchRemoteActor(id: str, localActor: Actor) -> Actor:
    """
    .. todo::
        - Add caching
        - Add error handling
        - Add tests
    """
    assert validate_uri(id)
    actor = signedRequest(
        "GET", id, "", f"{localActor.id}#main-key"
    )  # noqa:

    return Actor(
        id=actor.get("id"),
        inbox=actor.get("inbox"),
        outbox=actor.get("outbox"),
        publicKey=actor.get("publicKey", ""),
    )


@shared_task
def requestFollow(localID: str, remoteID: str) -> bool:
    """
    Task to request a follow from a remote actor

    args:
        id: str: The id of the remote actor
    """
    localActor = Actor.objects.get(id=localID)
    """Query the local actor by ID."""
    remoteActor = fetchRemoteActor(remoteID)
    """Fetch the remote actor details from the remote instance."""
    remoteActorObject, created = Actor.objects.get_or_create(id=remoteActor.get("id"))
    """Get or create the remote actor object in the local database (as a 'remote' actor)."""

    activity_id = action.send(
        sender=localActor, verb="Follow", target=remoteActorObject
    )
    print(localActor)
    print(remoteActorObject)
    print(activity_id)
    activity_id = activity_id[0][1].id
    """Store the 'Follow' action in the activity_stream through sending a signal. Get the activity ID."""

    print("Actor: ", localActor)
    print("Type: ", type(localActor))
    print("Actor Following: ", localActor.follows)
    print("Type: ", type(localActor.follows))

    message = json.dumps(
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": f"{activity_id}",
            "type": "Follow",
            "actor": localID,
            "object": remoteID,
        }
    )
    localActor.follows.add(remoteActorObject)  # remember we follow this actor

    signed = signedRequest(  # noqa: F841
        "POST", remoteActor.get("inbox"), message, f"{localActor.id}#main-key"
    )
    return True


@shared_task
def acceptFollow(inbox: str, activity: ActivityObject, accept_id: str) -> bool:
    """
    >>> from fedkit.signature import signedRequest
    >>> r = signedRequest(
        "POST",
        "https://pramari.de/accounts/andreas/inbox",
        activitymessage,
        "https://pramari.de/@andreas#main-key"
    )
    """
    base = Site.objects.get_current().domain

    message = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Accept",
        "id": f"https://{base}/{accept_id}",
        "actor": activity.object,
        "object": activity.toDict(),
    }
    logger.error(f"acceptFollow to {activity.actor}")
    logger.error(f"with message: {message=}")

    # remember we accepted this follow

    follow = Follow.objects.get(actor=activity.actor)
    follow.accepted = accept_id
    follow.save()

    signed = signedRequest(
        "POST",
        inbox,
        message,
        f"{activity.object}#main-key",
    )

    if signed.ok:
        return True
    return False


@shared_task
def sendLike(localActor: str, object: str) -> bool:
    """
    .. py:function:: sendLike(localActor: dict, object: str) -> bool
    .. todo::
        - Add tests
        - Implement
    """

    if not isinstance(localActor, str):
        raise ValueError("localActor must be a string")
    if not isinstance(object, str):
        raise ValueError("object must be a string")

    try:
        fetched = Fetch(object)
    except ValueError:
        logger.debug(f"Object returned invalid: {object}")
        return False
    remote = fetched.get("attributedTo")
    actor_inbox = Fetch(remote).get("inbox")
    """
    {'@context': ['https://www.w3.org/ns/activitystreams', {'ostatus': 'http://ostatus.org#', 'atomUri': 'ostatus:atomUri', 'inReplyToAtomUri': 'ostatus:inReplyToAtomUri', 'conversation': 'ostatus:conversation', 'sensitive': 'as:sensitive', 'toot': 'http://joinmastodon.org/ns#', 'votersCount': 'toot:votersCount'}], 'id': 'https://23.social/users/andreasofthings/statuses/112826215633359303', 'type': 'Note', 'summary': None, 'inReplyTo': None, 'published': '2024-07-21T19:50:25Z', 'url': 'https://23.social/@andreasofthings/112826215633359303', 'attributedTo': 'https://23.social/users/andreasofthings', 'to': ['https://www.w3.org/ns/activitystreams#Public'], 'cc': ['https://23.social/users/andreasofthings/followers'], 'sensitive': False, 'atomUri': 'https://23.social/users/andreasofthings/statuses/112826215633359303', 'inReplyToAtomUri': None, 'conversation': 'tag:23.social,2024-07-21:objectId=4978426:objectType=Conversation', 'content': '<p>Harris/Ocasio-Cortez</p>', 'contentMap': {'en': '<p>Harris/Ocasio-Cortez</p>'}, 'attachment': [], 'tag': [], 'replies': {'id': 'https://23.social/users/andreasofthings/statuses/112826215633359303/replies', 'type': 'Collection', 'first': {'type': 'CollectionPage', 'next': 'https://23.social/users/andreasofthings/statuses/112826215633359303/replies?min_id=112826217149903948&page=true', 'partOf': 'https://23.social/users/andreasofthings/statuses/112826215633359303/replies', 'items': ['https://23.social/users/andreasofthings/statuses/112826217149903948']}}}  # noqa: E501
    """

    message = json.dumps(
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Like",
            "actor": localActor,
            "object": object,
        }
    )

    print("sending like")
    print(f"to: {actor_inbox}")
    print(message)
    signed = signedRequest(  # noqa: F841
        "POST", actor_inbox, message, f"{localActor}#main-key"
    )

    return True


"""
@shared_task
def activitypub_send_task(user: User, message: str) -> Tuple[bool]:
    from Crypto.Hash import SHA256
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.PublicKey import RSA

    private_key = RSA.importKey(user.actor_set.get().private_key)
    # Sign the message
    signer = PKCS1_v1_5.new(private_key)

    actor = user.actor_set.get()
    date = datetime.datetime.now(datetime.timezone.utc)

    signed_string = f"(request-target): post /inbox\nhost: {user.socialaccount_set.first().extra_data['instance']}\ndate: {date}"  # noqa: E501
    # signature = keypair.sign(OpenSSL::Digest::SHA256.new, signed_string)
    digest = SHA256.new()
    digest.update(signed_string.encode("utf-8"))
    signature = signer.sign(digest)
    headers = {
        "keyId": f"{actor.get_actor_url()}",
        "headers": "(request-target) host date",
        "signature": f"{signature}",
    }
    import request

    return request.post(user.actor_set.get().get_inbox, headers=headers)
"""


@shared_task
def genKeyPair() -> Tuple[str, str]:
    from cryptography.hazmat.backends import \
        default_backend as crypto_default_backend  # noqa: E501
    from cryptography.hazmat.primitives import \
        serialization as crypto_serialization  # noqa: E501
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048,  # noqa: E501
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption(),
    ).decode("utf-8")

    public_key = (
        key.public_key()
        .public_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode("utf-8")
    )
    return (private_key, public_key)
