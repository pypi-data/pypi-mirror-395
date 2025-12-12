import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.dispatch import Signal
from django.utils import timezone

from .models import Actor
from .registry import check

logger = logging.getLogger(__name__)

action = Signal()


def signalHandler(*args, **kwargs):
    """
    Handler function to create Action instance upon action signal call.

    This function is called whenever an action signal is called. It creates an
    instance of the Action model and saves it to the database.

    :param  \*args: Additional arguments for the action.  # noqa: W605
    :param  \*\*kwargs: Additional keyword arguments to an action. # noqa: W605

    :return: The created Action instance.

    This function will handle signals sent by the action signal. It will create
    an instance of the Action model and save it to the database. It will allow
    the following pattern:

    .. testsetup::
        from fedkit.models import Actor, Note
        from fedkit.signals import action

    This function will handle signals sent by the action signal. It will create
    an instance of the Action model and save it to the database. With that, one
    can easily track actions in the application. It will allow the following
    pattern:

    .. doctest::
        a = Actor.objects.get(id="https://pramari.de/@andreas")
        n = Note.objects.all()[0]

    Interacting with the signal will allow to do the following:

    .. testcode::
        action.send(sender=a, actor=a, verb="created", action_object=n)
        action.send(sender=a, actor=a, verb="liked", action_object=n)

    This will create two actions in the database. One for the creation of the
    note and one for the like action. The actions can be queried as follows:

    .. testoutput::
        Action.objects.count() > 0

    .. seealso::
        `Django Activity Streams <https://github.com/justquick/django-activity-stream/blob/main/actstream/actions.py>`_, from which this is heavily inspired.  # noqa: E501

    """  # noqa: E501
    print("Hello, world!")
    logger.error("Entering signal handler")
    signal = kwargs.pop("signal", None)  # noqa: F841
    actor = kwargs.pop("sender")
    verb = kwargs.pop("verb")

    # We must store the untranslated string
    # If verb is an ugettext_lazyed string, fetch the original string
    if hasattr(verb, "_proxy____args"):
        verb = verb._proxy____args[0]

    actor_content_type = ContentType.objects.get_for_model(actor)
    actor_object_id = actor.pk

    logger.error(f"Actor: {actor}, verb: {verb}, kwargs: {kwargs}")

    activity = apps.get_model("fedkit", "action")(
        actor_content_type=actor_content_type,
        actor_object_id=actor_object_id,
        activity_type=str(verb).lower(),
        public=bool(kwargs.pop("public", True)),
        description=kwargs.pop("description", None),
        timestamp=kwargs.pop("timestamp", timezone.now()),
    )

    # for opt in ("target", "action_object"):
    target = kwargs.pop("target", None)
    if target is not None:
        check(target)  # Check if the object is registered
        setattr(activity, "target_object_id", target.pk)
        setattr(
            activity,
            "target_content_type",
            ContentType.objects.get_for_model(target),
        )

    action_object = kwargs.pop("action_object", None)
    if action_object is not None:
        check(action_object)  # Check if the object is registered
        setattr(activity, "action_object_object_id", action_object.pk)
        setattr(
            activity,
            "action_object_content_type",
            ContentType.objects.get_for_model(action_object),
        )

    activity.save(force_insert=True)
    logger.debug("Succesfully exited signalHandler")
    return activity


def createActor(sender, instance, created, **kwargs):
    from django.contrib.auth import get_user_model
    from django.contrib.sites.models import Site
    from fedkit.models import Actor
    User = get_user_model()
    if created:  # not user.profile:
        try:
            base = f"https://{Site.objects.get_current().domain}"
        except Site.DoesNotExist:
            """
            .. todo::
                This is a temporary solution. In the future, we should
                have a default site that is created when the application
                is installed. It may fix tests, but possibly does not
                work when in production.
            """
            base = "https://example.com"

        if isinstance(instance, User):
            Actor.objects.create(
                user=instance, type="Person", id=f"{base}/@{instance.username}"
            )
