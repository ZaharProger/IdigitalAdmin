from rest_framework import permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models.contexts import DbContext
from .models.serializers import EventSerializer
from .services import EventService


class EventController(APIView):
    permission_classes = []
    authentication_classes = []

    db_context: DbContext = None
    service: EventService = None

    def get(self, request):
        events = self.service.get_all_events(self.db_context)
        serialized_events = EventSerializer(events, many=True)

        return Response(
            serialized_events.data,
            status=status.HTTP_200_OK
        )
