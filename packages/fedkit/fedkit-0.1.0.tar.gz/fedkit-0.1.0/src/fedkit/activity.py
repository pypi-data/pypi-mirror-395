"""
.. py:module:: activity
    :synopsis: ActivityPub schema and utilities

    https://docs.python.org/3/library/typing.html
"""

import json
import logging
from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

# from dataclasses import asdict
# from dataclasses import is_dataclass
from fedkit.models import Action

logger = logging.getLogger(__name__)


def default_document_loader(url: str, options: dict = {}):
    from urllib.parse import urlparse

    from fedkit.schema import schemas

    parsedurl = urlparse(url)
    stripped_path = parsedurl.path.rstrip("/")
    if not parsedurl.hostname:
        logging.info(f"json-ld schema '{url!r}' has no hostname")
        return schemas["unknown"]
    key = f"{parsedurl.hostname}{stripped_path}"
    try:
        return schemas[key]
    except KeyError:
        try:
            key = f"*{stripped_path}"
            return schemas[key]
        except KeyError:
            # Return an empty context instead of throwing
            # an error, as per the ActivityStreams spec
            return schemas["unknown"]


def canonicalize(ld_data: dict) -> dict:
    """ """
    from pyld import jsonld

    if not isinstance(ld_data, dict):
        raise ValueError("Pass decoded JSON data into LDDocument")

    context = ld_data.get("@context", [])

    if not isinstance(context, list):
        context = [context]

    if not context:
        context.append("https://www.w3.org/ns/activitystreams")
        context.append("https://w3id.org/security/v1")
        context.append(
            {
                "blurhash": "toot:blurhash",
                "Emoji": "toot:Emoji",
                "featured": {"@id": "toot:featured", "@type": "@id"},
                "focalPoint": {
                    "@container": "@list",
                    "@id": "toot:focalPoint",
                },
                "Hashtag": "as:Hashtag",
                "indexable": "toot:indexable",
                "manuallyApprovesFollowers": "as:manuallyApprovesFollowers",
                "sensitive": "as:sensitive",
                "toot": "http://joinmastodon.org/ns#",
                "votersCount": "toot:votersCount",
            }
        )
    ld_data["@context"] = context

    jsonld.set_document_loader(default_document_loader)
    return jsonld.compact(jsonld.expand(ld_data), context)


@dataclass
class Location:
    """
    ActivityPub/Streams representation of of Location objects.

    .. seealso::
        The W3C definition of `location <https://www.w3.org/TR/activitystreams-vocabulary/#dfn-location>`_ in ActivityStreams.  # noqa: E501
    """

    name: str
    type: str = "Place"
    longitude: Decimal = 0
    latitude: Decimal = 0
    altitude: Decimal = 0
    units: str = "m"


@dataclass
class ActivityObject:
    """
    ActivityObject is a base class for all ActivityPub objects.

    .. seealso::
        The W3C definition of `ActivityPub Objects <https://www.w3.org/ns/activitystreams>_`.  # noqa: E501
    """

    def __init__(self, message, *args, **kwargs) -> None:
        """
        Initialize the ActivityObject.

        .. todo::
            sanitize the incoming message
        """
        match message:
            case dict():
                self._fromDict(incoming=canonicalize(message))
            case str():
                self._fromDict(incoming=canonicalize(json.loads(message)))
            case _:
                raise ValueError("Invalid type for message")

        super().__init__(*args, **kwargs)

    def toDict(self, *args, **kwargs) -> dict:
        """Conveniece method to convert the object to a dictionary."""
        result = {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }
        return result

    def toAction(self) -> Action:
        """
        Convert the ActivityStreams object to a database Action record.
        This involves resolving dictionary representations of objects (like actor)
        into actual Django model instances.
        """
        from fedkit.models import Action, Actor, Note

        def _get_or_create_model(data: dict):
            """
            Resolves a dictionary into a Django model instance.
            """
            if not isinstance(data, dict):
                return None

            obj_type = data.get("type")
            obj_id = data.get("id")

            if not obj_type or not obj_id:
                return None

            # This mapping determines which Django model to use for an
            # ActivityStreams object type.
            model_map = {
                "Person": Actor,
                "Application": Actor,
                "Service": Actor,
                "Group": Actor,
                "Organization": Actor,
                "Note": Note,
                "Article": Note,
                "Image": Note,
                "Video": Note,
                "Audio": Note,
            }
            model = model_map.get(obj_type)

            if not model:
                logger.warning(
                    "Unable to convert ActivityStreams type "
                    f"'{obj_type}' to a Django model."
                )
                return None

            # Prepare data for model creation/update.
            # Only use keys that are actual fields on the model.
            model_fields = {f.name for f in model._meta.get_fields()}
            defaults = {
                k: v
                for k, v in data.items()
                if k in model_fields and not isinstance(v, (dict, list))
            }
            # The 'id' field is used for lookup, not for updating.
            defaults.pop("id", None)

            instance, created = model.objects.get_or_create(
                id=obj_id, defaults=defaults
            )
            if not created and defaults:
                # If the object already existed, update its fields.
                for key, value in defaults.items():
                    setattr(instance, key, value)
                instance.save(update_fields=list(defaults.keys()))
            return instance

        # Resolve actor, object, and target to model instances.
        actor_instance = _get_or_create_model(self.__dict__.get("actor"))
        object_instance = _get_or_create_model(self.__dict__.get("object"))
        target_instance = _get_or_create_model(self.__dict__.get("target"))

        # The actor is a required field for an Action.
        if not actor_instance:
            logger.warning(
                "Could not create Action, actor not found or resolvable: "
                f"{self.__dict__.get('actor')}"
            )
            return None

        # Instantiate the Action model in memory first.
        action = Action(
            activity_type=self.__dict__.get("type"),
            description=self.__dict__.get("summary", ""),
        )

        # Assign the related model instances to the GenericForeignKey fields.
        # This is the safe way to handle GFKs.
        action.actor = actor_instance
        action.action_object = object_instance
        action.target = target_instance

        # Save the fully-formed instance to the database.
        action.save()

        return action

    def _fromDict(self, incoming: dict) -> None:
        """
        Initialize the object from a dictionary.

        .. important::
            The function will convert '@context' to 'context' and update
            the object. Python dataclasses do not allow '@' in attribute names.
        """
        if not isinstance(incoming, dict):
            raise ValueError("Invalid type for incoming")
        self.__dict__.update({"context": incoming.pop("@context", None)})
        self.__dict__.update(incoming)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.toDict()})"

    context: dict | str  # Object

    attachment: Optional[List[dict]] = None  # Object
    attributedTo: Optional[List[dict]] = None  # Person or Organization
    audience: Optional[List[dict]] = None  # Collection
    content: Optional[str] = None
    name: Optional[str] = None
    generator: Optional[dict] = None  # Application
    icon: Optional[dict] = None  # Link
    image: Optional[dict] = None  # Link
    inReplyTo: Optional[dict] = None  # Object
    location: Optional[Location] = None  # Place
    preview: Optional[dict] = None  # Link
    published: Optional[str] = ""
    updated: Optional[str] = ""
    replies: Optional[dict] = None  # Collection
    summary: Optional[str] = ""
    url: Optional[str] = ""
    tag: Optional[List[dict]] = field(default_factory=lambda: [{}])
    to: Optional[List[dict]] = field(default_factory=lambda: [])
    bto: Optional[List[dict]] = field(default_factory=lambda: [])
    cc: Optional[List[dict]] = field(default_factory=lambda: [])
    bcc: Optional[List[dict]] = field(default_factory=lambda: [])
    mediaType: Optional[str] = ""
    duration: Optional[str] = ""
