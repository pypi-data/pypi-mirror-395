from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class StreamingView(APIView):
    def get(self, request):
        return Response("Hello, world!", status=status.HTTP_200_OK)
