import logging

from django import forms
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from fedkit.models import Like, Actor
from fedkit.signals import action
from fedkit.tasks import sendLike

logger = logging.getLogger(__name__)


def urlfields_assume_https(db_field, **kwargs):
    """
    ModelForm.Meta.formfield_callback function to
    assume HTTPS for scheme-less domains in URLFields.
    """
    if isinstance(db_field, models.URLField):
        kwargs["assume_scheme"] = "https"
    return db_field.formfield(**kwargs)


class LikesForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ["actor", "object"]
        widgets = {
            "object": forms.URLInput(attrs={"class": "form-control"}),
        }
        formfield_callback = urlfields_assume_https


class LikeCreateView(LoginRequiredMixin, CreateView):
    template_name = "activitypub/like_create.html"
    form_class = LikesForm
    model = Like
    # success_url = "/thanks/"

    def get_initial(self):
        actor = self.request.user.profile.actor
        return {"actor": actor}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slug"] = self.request.user.profile.slug
        return context

    def form_valid(self, form):
        """
        Upon succesful save, send a signal to the
        activitypub app to send a like to the object.

        .. todo:: This should be done through a signal in first place.

        .. seealso:: :py:func:`webapp.signals.action`

        .. seealso:: :py:func:`webapp.tasks.activitypub.sendLike`

        """
        self.object = form.save()

        action.send(
            sender=self.request.user.profile.actor,
            verb="like",
            action_object=self.object,
        )
        actor = self.request.user.profile.actor
        if settings.DEBUG:
            sendLike(actor.id, form.cleaned_data["object"])
        else:
            # this should be a celery task
            sendLike(actor.id, form.cleaned_data["object"])
        return super().form_valid(form)


class LikeDetailView(LoginRequiredMixin, DetailView):
    model = Like
    template_name = "activitypub/like_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slug"] = self.request.user.profile.slug
        return context


class LikeDeleteView(LoginRequiredMixin, DeleteView):
    model = Like
    template_name = "activitypub/like_delete.html"
    success_url = "/thanks/"

    def form_valid(self, form):
        """
        :py:method:form_valid validates form input.

        Upon succesful save, send a signal to the
        activitypub app to undo the like of the object.

        .. seealso:: To learn about signals see: :py:func:`webapp.signals.action`

        .. seealso:: :py:func:`webapp.tasks.activitypub.sendUndo`

        .. seealso:: `ActivityPub Undo <https://www.w3.org/TR/activitystreams-vocabulary/#dfn-undo>`_  # noqa: E501
        """
        action.send(
            sender=self.request.user.profile.actor,
            verb="undo",
            action_object=self.object,
        )
        return super().form_valid(form)


class LikeListView(LoginRequiredMixin, ListView):
    model = Like
    template_name = "activitypub/like_list.html"
    context_object_name = "likes"
    paginate_by = 10

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        actor = Profile.objects.get(slug=slug).actor
        return Like.objects.all().order_by("-created_at").filter(actor=actor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        context["actor"] = Profile.objects.get(slug=slug).actor
        return context
