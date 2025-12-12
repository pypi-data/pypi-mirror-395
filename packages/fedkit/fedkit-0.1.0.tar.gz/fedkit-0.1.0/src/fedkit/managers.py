from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Manager, Model
from django.db.models.query import EmptyQuerySet, QuerySet

from .decorators import stream
from .registry import check


class BaseQuerySet(QuerySet):
    """
    A QuerySet with a fetch_generic_relations() method to bulk fetch
    all generic related items.  Similar to select_related(), but for
    generic foreign keys. This wraps QuerySet.prefetch_related.
    """

    def fetch_generic_relations(self, *args):
        qs = self._clone()

        if not settings.FETCH_RELATIONS:
            """ """
            return qs

        pf = self.model._meta.private_fields

        gfk_fields = [g for g in pf if isinstance(g, GenericForeignKey)]

        if args:  # If args is specified, limit to those fields in args
            gfk_fields = [g for g in gfk_fields if g.name in args]

        return qs.prefetch_related(*[g.name for g in gfk_fields])

    def _clone(self, klass=None, **kwargs):
        return super(BaseQuerySet, self)._clone()

    def none(self):
        clone = self._clone({"klass": BaseEmptyQuerySet})
        if hasattr(clone.query, "set_empty"):
            clone.query.set_empty()
        return clone


class BaseEmptyQuerySet(BaseQuerySet, EmptyQuerySet):
    def fetch_generic_relations(self, *args):
        return self


class BaseManager(Manager):
    """
    A manager that for working with
    Generik Foreign Keys.

    get_query_set will return a QuerySet with Generic Foreign Keys
    instead of a regular QuerySet.
    """

    def get_query_set(self):
        return BaseQuerySet(self.model)

    get_queryset = get_query_set

    def none(self):
        return self.get_queryset().none()


class ActionManager(BaseManager):
    """
    Default manager for Actions, accessed through Action.objects
    """

    def public(self, *args, **kwargs):
        """
        Public actions only.
        """
        kwargs["public"] = True
        return self.filter(*args, **kwargs)

    @stream
    def actor(self, obj: Model, **kwargs):
        """
        Stream of most recent public actions for the actor `obj`.
        Keyword arguments will be passed to Action.objects.filter
        """
        check(obj)
        return obj.actor_actions.public(**kwargs)
