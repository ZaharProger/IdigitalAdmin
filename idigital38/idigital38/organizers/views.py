from django.db.models import Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .forms import OrganizerForm
from .models import Organizer
from .serializers import OrganizerSerializer


class OrganizerView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    organizer_serializer: OrganizerSerializer = None

    def get(self, request):
        organizer_id = request.GET.get('id', None)
        if organizer_id is None:
            organizers_data = Organizer.objects.all()
        else:
            try:
                organizers_data = [Organizer.objects.get(pk=organizer_id)]
            except (Organizer.DoesNotExist, ValueError):
                organizers_data = []

        is_not_found = len(organizers_data) == 0

        return Response(
            {
                'data': OrganizerSerializer(organizers_data, many=True).data,
                'message': 'Не найдено ни одного участника организационного комитета' if is_not_found else ''
            },
            status=status.HTTP_200_OK if not is_not_found else status.HTTP_404_NOT_FOUND,
            content_type='application/json'
        )

    def delete(self, request):
        ids = [item_id.strip() for item_id in request.GET.get('ids', '0').split(',')]
        is_valid = all(item_id.isnumeric() for item_id in ids)

        if is_valid:
            Organizer.objects.filter(id__in=ids).delete()

        return Response(
            {'message': 'Идентификаторы должны быть целыми числами' if not is_valid else ''},
            status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )

    def post(self, request):
        new_organizer = OrganizerForm(request.data, request.FILES)
        if new_organizer.is_valid():
            max_order = Organizer.objects.aggregate(Max('order'))
            new_order = 0 if max_order is None else max_order['order__max'] + 1
            new_organizer.instance.order = new_order

            new_organizer.save()
            response_status = status.HTTP_200_OK
        else:
            response_status = status.HTTP_400_BAD_REQUEST
            print(new_organizer.errors)

        return Response(
            {'message': ''},
            status=response_status,
            content_type='application/json'
        )

    def put(self, request):
        try:
            found_organizers_data = Organizer.objects.get(pk=int(request.data['id']))
            serialized_data = OrganizerSerializer(found_organizers_data, data=request.data, partial=True)

            if serialized_data.is_valid():
                serialized_data.save()
                response_status = status.HTTP_200_OK
                message = ''
            else:
                response_status = status.HTTP_400_BAD_REQUEST
                message = 'Форма содержит недопустимые данные'
        except (Organizer.DoesNotExist, ValueError):
            response_status = status.HTTP_404_NOT_FOUND
            message = 'Не найдено участника организационного комитета по заданному идентификатору'

        return Response(
            {'message': message},
            status=response_status,
            content_type='application/json'
        )

    def patch(self, request):
        try:
            for organizer_id, organizer_order in request.data.items():
                Organizer.objects.filter(id=int(organizer_id)).update(order=organizer_order)

            is_success = True
        except ValueError:
            is_success = False

        return Response(
            {'message': '' if is_success else 'Идентификаторы должны быть целыми числами'},
            status=status.HTTP_200_OK if is_success else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
