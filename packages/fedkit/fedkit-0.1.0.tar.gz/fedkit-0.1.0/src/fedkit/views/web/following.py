from django import forms
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView

# from webapp.models import Profile as Fllwng
from fedkit.models.actor import Follow


class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = "__all__"
        widgets = {
            "object": forms.URLInput(attrs={"class": "form-control"}),
        }


class FollowingCreateView(CreateView):
    model = Follow
    form_class = FollowForm
    template_name = "activitypub/follow_create.html"


class FollowingDetailView(DetailView):
    model = Follow
    template_name = "activitypub/follow_detail.html"


class FollowingListView(ListView):
    model = Follow
    template_name = "activitypub/follow_list.html"


class FollowingDeleteView(DeleteView):
    model = Follow
    success_url = "/following/"
    template_name = "activitypub/follow_delete.html"
