from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .forms import EventForm
from .models import Event
from .serializers import EventSerializer


class EventView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        method = self.request.method
        return [] if method == 'GET' else [IsAuthenticated()]

    def get(self, request):
        event_id = request.GET.get('id', None)
        if event_id is None:
            events_data = Event.objects.all()
        else:
            try:
                events_data = [Event.objects.get(pk=event_id)]
            except (Event.DoesNotExist, ValueError):
                events_data = []

        is_not_found = len(events_data) == 0

        return Response(
            {
                'data': EventSerializer(events_data, many=True).data,
                'message': 'Не найдено ни одного мероприятия' if is_not_found else ''
            },
            status=status.HTTP_200_OK if not is_not_found else status.HTTP_404_NOT_FOUND,
            content_type='application/json'
        )

    def delete(self, request):
        ids = [item_id.strip() for item_id in request.GET.get('ids', '0').split(',')]
        is_valid = all(item_id.isnumeric() for item_id in ids)

        if is_valid:
            Event.objects.filter(id__in=ids).delete()

        return Response(
            {'message': 'Идентификаторы должны быть целыми числами' if not is_valid else ''},
            status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )

    def post(self, request):
        new_event = EventForm(request.data, request.FILES)
        if new_event.is_valid():
            new_event.save()
            response_status = status.HTTP_200_OK
        else:
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(
            {'message': ''},
            status=response_status,
            content_type='application/json'
        )

    def put(self, request):
        try:
            found_events_data = Event.objects.get(pk=int(request.data['id']))
            serialized_data = EventSerializer(found_events_data, data=request.data, partial=True)

            if serialized_data.is_valid():
                serialized_data.save()
                response_status = status.HTTP_200_OK
                message = ''
            else:
                response_status = status.HTTP_400_BAD_REQUEST
                message = 'Форма содержит недопустимые данные'
        except (Event.DoesNotExist, ValueError):
            response_status = status.HTTP_404_NOT_FOUND
            message = 'Не найдено мероприятия по заданному идентификатору'

        return Response(
            {'message': message},
            status=response_status,
            content_type='application/json'
        )
