from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OrganizerSerializer


class OrganizerView(APIView):
    permission_classes = []
    authentication_classes = []

    organizer_serializer: OrganizerSerializer = None
    # organizer_service: OrganizerService = None

    def get(self, request):
        organizer_id = request.GET.get('id', None)
        organizers = []

        return Response(
            {
                'data': OrganizerSerializer(organizers, many=len(organizers) != 1).data,
                'message': 'Не найдено ни одного участника организационного комитета' if len(organizers) == 0 else ''
            },
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    def delete(self, request):
        ids = [item_id.strip() for item_id in request.GET.get('ids', '0').split(',')]
        is_valid = all(item_id.isnumeric() for item_id in ids)


        return Response(
            {'message': 'Идентификаторы должны быть целыми числами' if not is_valid else ''},
            status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )

    def post(self, request):


        return Response(
            {'message': ''},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    def put(self, request):


        return Response(
            {'message': ''},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    def patch(self, request):

        return Response(
            {'message': ''},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
