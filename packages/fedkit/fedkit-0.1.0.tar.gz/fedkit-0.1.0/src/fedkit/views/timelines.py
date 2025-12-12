"""
2024-08-30 12:16:20 default[20240830t115815]  Not Found: /api/v1/streaming/public
2024-08-30 12:16:20 default[20240830t115815]  Not Found: /api/v1/timelines/public
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TimelineView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)
