from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.transaction import atomic

from .models import ProgrammeDay
from .forms import DayBlockForm, ProgrammeDayForm, ReportForm, DayTimetableForm
from .serializers import ProgrammeDaySerializer

# Это я тесты проводил для POST хэндлера, можно закомментить, в гит я не закидывал тестовый файл
from .test import request_data


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

    """
        Здесь происходит извлечение вложенных данных из словаря, добавление внешнего ключа для связки в БД в
        каждый вложенный экземпляр и упаковка в джанго форму (описывается в параметре callback) 
        с последующим сохранением в БД
    """

    def save_nested_data(self, main_form, nested_form_key, fk_key, fk_value, callback) -> dict:
        inserted_data = {}

        nested_form_data = main_form[nested_form_key] if nested_form_key in main_form.keys() else []
        for item in nested_form_data:
            item[fk_key] = fk_value
            item_form = callback(item)
            if item_form.is_valid():
                saved_item = item_form.save()
                inserted_data[saved_item.id] = item

        return inserted_data

    def post(self, request):
        day_form_data = {
            'name': request_data['name'] if 'name' in request_data.keys() else None,
            'place': request_data['place'] if 'place' in request_data.keys() else None
        }

        day_form = ProgrammeDayForm(day_form_data)
        all_correct = False
        if day_form.is_valid():
            with atomic():
                last_inserted_id = day_form.save()

                self.save_nested_data(
                    main_form=request_data,
                    nested_form_key='day_timetable',
                    fk_key='day',
                    fk_value=last_inserted_id,
                    callback=lambda form: DayTimetableForm(form)
                )
                inserted_blocks = self.save_nested_data(
                    main_form=request_data,
                    nested_form_key='day_blocks',
                    fk_key='day',
                    fk_value=last_inserted_id,
                    callback=lambda form: DayBlockForm(form)
                )
                for inserted_block_id, inserted_block_data in inserted_blocks.items():
                    self.save_nested_data(
                        main_form=inserted_block_data,
                        nested_form_key='reports',
                        fk_key='block',
                        fk_value=inserted_block_id,
                        callback=lambda form: ReportForm(form)
                    )
                all_correct = True

        return Response(
            {'message': ''},
            status=status.HTTP_200_OK if all_correct else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
