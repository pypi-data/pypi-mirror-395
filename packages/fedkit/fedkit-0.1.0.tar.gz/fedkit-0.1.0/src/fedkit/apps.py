import logging

from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class ActivitypubConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fedkit"

    label = "fedkit"
    verbose_name = _("activitypub")
    path = "@"

    def ready(self):
        from django.conf import settings
        from django.contrib.auth import get_user_model

        from . import registry
        from .models import Actor, Like, Note
        from .signals import action, createActor, signalHandler

        User = get_user_model()

        logger.error("Successfully working with ActivityPub")

        post_save.connect(createActor, sender=User)
        action.connect(signalHandler, dispatch_uid="activitypub")

        settings = settings._wrapped.__dict__
        settings.setdefault("BLOCKED_SERVERS", [])
        settings.setdefault("FETCH_RELATIONS", False)

        try:
            registry.register(Actor)
        except ImportError as e:
            logger.error(f"Model for 'Actor' not installed {e}")
        except ImproperlyConfigured as e:
            logger.error(f"Cannot register `Actor` for Activities. {e}")
        except ValueError as e:
            logger.error(f"Fucking fix this error: {e}")

        try:
            registry.register(Like)
            registry.register(Note)
        except ImportError as e:
            logger.error(f"Model for 'Like' not installed {e}")
        except ImproperlyConfigured as e:
            logger.error(f"Cannot register `Like` for Activities. {e}")
        except ValueError as e:
            logger.error(f"Fucking fix this error: {e}")

        logger.info("WebApp ready.")
