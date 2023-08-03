from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import DayTimetable, DayBlock, ProgrammeDay, Report
from .forms import DayBlockForm, ProgrammeDayForm, ReportForm, DayTimetableForm
from .serializers import DayBlockSerializer, ReportSerializer, ProgrammeDaySerializer, DayTimetableSerializer


class ProgrammeDayView(APIView):
    permission_classes = []
    authentication_classes = []

    programme_day_serializer: ProgrammeDaySerializer = None

    def get(self, request):
        day_id = request.GET.get('id', None)
        if day_id is None:
            days_data = ProgrammeDay.objects.all()
        else:
            try:
                days_data = [ProgrammeDay.objects.get(pk=day_id)]
            except (ProgrammeDay.DoesNotExist, ValueError):
                days_data = []

        is_not_found = len(days_data) == 0

        return Response(
            {
                'data': ProgrammeDaySerializer(days_data, many=True).data,
                'message': 'Не найдено ни одного дня в рамках программы форума' if is_not_found else ''
            },
            status=status.HTTP_200_OK if not is_not_found else status.HTTP_404_NOT_FOUND,
            content_type='application/json'
        )

    def delete(self, request):
        ids = [item_id.strip() for item_id in request.GET.get('ids', '0').split(',')]
        is_valid = all(item_id.isnumeric() for item_id in ids)

        if is_valid:
            ProgrammeDay.objects.filter(id__in=ids).delete()

        return Response(
            {'message': 'Идентификаторы должны быть целыми числами' if not is_valid else ''},
            status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
