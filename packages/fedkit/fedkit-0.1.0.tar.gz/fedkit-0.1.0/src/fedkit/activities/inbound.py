import logging

from django.http import JsonResponse
from webapp.signals import action

from fedkit.activity import ActivityObject
from fedkit.models import Actor

from .follow import Follow

logger = logging.getLogger(__name__)

__all__ = ["Follow", "action_decorator", "create", "like", "undo"]


def action_decorator(f):
    """
    Decorator for inbound activity handlers.

    Not clear anymore what this does.
    """

    def wrapper(target, activity: ActivityObject, *args, **kwargs):
        try:
            localactor = Actor.objects.get(id=activity.actor)
        except Actor.DoesNotExist:
            logger.error(f"Actor not found: '{activity.actor}'")
            return JsonResponse(
                {"error": "Actor f'{activity.actor}' not found"}, status=404
            )

        try:
            action_object = Actor.objects.get(id=activity.object)
        except Actor.DoesNotExist:
            logger.error(f"{activity.type}: Object not found: '{activity.object}'")
            action_object = None

        action.send(
            sender=localactor,
            verb=activity.type,
            action_object=action_object,
            target=target,
        )

        return f(target, activity, *args, **kwargs)

    return wrapper


@action_decorator
def create(target: Actor, activity: ActivityObject) -> JsonResponse:
    """
    Create a new `:model:Note`.

    Type: Note
        {
        'id': 'https://23.social/users/andreasofthings/statuses/112728133944821188',
        'type': 'Note',
        'summary': None,
        'inReplyTo': None,
        'published': '2024-07-04T12:06:57Z',
        'url': 'https://23.social/@andreasofthings/112728133944821188',
        'attributedTo': 'https://23.social/users/andreasofthings',
        'to': ['https://www.w3.org/ns/activitystreams#Public'],
        'cc': ['https://23.social/users/andreasofthings/followers'],
        'sensitive': False,
        'atomUri': 'https://23.social/users/andreasofthings/statuses/112728133944821188',
        'inReplyToAtomUri': None,
        'conversation': 'tag:23.social,2024-07-04:objectId=4444254:objectType=Conversation',
        'content': '<p>I implemented http signatures (both sign and verify) for the fediverse.</p><p>In python.</p><p>I feel like I made fire.</p>',
        'contentMap': {'en': '<p>I implemented http signatures (both sign and verify) for the fediverse.</p><p>In python.</p><p>I feel like I made fire.</p>'},
        'attachment': [],
        'tag': [],
        'replies': {
            'id': 'https://23.social/users/andreasofthings/statuses/112728133944821188/replies',
            'type': 'Collection',
            'first': {
                'type': 'CollectionPage',
                'next': 'https://23.social/users/andreasofthings/statuses/112728133944821188/replies?only_other_accounts=true&page=true',
                'partOf': 'https://23.social/users/andreasofthings/statuses/112728133944821188/replies',
                'items': []
            }
        }
    }  # noqa: E501
    """

    logger.error(f"Create Object: {activity.object}")

    note = activity.object
    assert note is not None
    assert isinstance(note, dict)

    if note.get("type") == "Note":
        from webapp.models import Note

        localNote = Note.objects.create(  # noqa: F841
            remoteID=note.get("id"),
            content=note.get("content"),
            published=note.get("published"),
        )

    return JsonResponse(
        {
            "status": f"success: {activity.actor} {activity.type} {activity.object}"
        }
    )


@action_decorator
def delete(target: Actor, activity: ActivityObject) -> JsonResponse:
    """
    Delete an activity.
    """

    return JsonResponse({"status": "cannot delete"})


def echorequest(activity: ActivityObject, signature: str) -> JsonResponse:
    """
    Echo a request.
    """

    return JsonResponse({"status": "cannot echo"})


@action_decorator
def like(target: Actor, activity: ActivityObject) -> JsonResponse:
    """
    Like an activity.
    """

    return JsonResponse({"status": "cannot like"})


@action_decorator
def undo(target: Actor, activity: ActivityObject):
    """
    Undo an activity.

    Object: (example)
        {
            'id': 'https://23.social/b271295c-7a1b-4da8-ae58-927fea32bb60',
            'type': 'Follow',
            'actor': 'https://23.social/users/andreasofthings',
            'object': 'https://pramari.de/@andreas'
        }
    """
    logger.error(f"Activity Object: {activity}")

    if not activity.id:
        return JsonResponse({"status": "missing id"})

    if not activity.object:
        return JsonResponse({"status": "missing object"})

    if (
        not activity.actor and activity.object.get("type").lower() != "follow"
    ):
        return JsonResponse({"status": "invalid object/unsupported activity"})

    from webapp.models.activitypub.actor import Follow

    try:
        follow = Follow.objects.get(accepted=activity.object.get("id"))
    except Follow.DoesNotExist:
        return JsonResponse({"status": "follow not found"})
    follow.delete()
    logger.error(f"{activity.actor} has undone {activity.object}")

    return JsonResponse({"status": "undone"})
