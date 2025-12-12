from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import parsers, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from fedkit.models import Actor
from fedkit.parsers import ActivityParser
from fedkit.renderers import ActivityRenderer, JsonLDRenderer
from fedkit.serializers.actor import ActorSerializer


class ActivityBaseView(APIView):
    model = Actor
    queryset = Actor.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    serializer_class = ActorSerializer
    template_name = None
    parser_classes = [
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
        ActivityParser,
        # parsers.FileUploadParser,
    ]
    renderer_classes = [
        JsonLDRenderer,
        ActivityRenderer,
        TemplateHTMLRenderer,
    ]

    def get_object(self):
        try:
            return self.queryset.get(slug=self.kwargs["slug"])
        except Actor.DoesNotExist:
            raise Http404("Actor not found")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        Process the incoming message.

        No CSRF token required for incoming activities.
        """
        return super().dispatch(*args, **kwargs)
