from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import EventForm
from .models import Event
from .serializers import EventSerializer


class EventView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        event_id = request.GET.get('id', None)
        if event_id is None:
            events_data = Event.objects.all()
            is_single = False
        else:
            is_single = True
            try:
                events_data = Event.objects.get(pk=event_id)
            except Event.DoesNotExist:
                events_data = None

        return Response(
            {
                'data': EventSerializer(events_data, many=not is_single).data,
                'message': 'Не найдено ни одного мероприятия' if
                events_data is None or (events_data is not None and len(events_data) == 0) else ''
            },
            status=status.HTTP_200_OK,
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
            else:
                response_status = status.HTTP_400_BAD_REQUEST
        except Event.DoesNotExist:
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(
            {'message': ''},
            status=response_status,
            content_type='application/json'
        )
