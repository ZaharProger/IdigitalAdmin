from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.transaction import atomic

from .models import ProgrammeDay, DayTimetable, DayBlock, Report
from .forms import DayBlockForm, ProgrammeDayForm, ReportForm, DayTimetableForm
from .serializers import ProgrammeDaySerializer, DayTimetableSerializer, DayBlockSerializer, ReportSerializer

# Это я тесты проводил для POST хэндлера, можно закомментить, в гит я не закидывал тестовый файл
from .test import request_data

class ProgrammeDayView(APIView):
    permission_classes = []
    authentication_classes = []

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

    def add_nested_data(self, data, fk_key, fk_value, callback) -> list:
        inserted_data = []

        for item in data:
            item[fk_key] = fk_value
            item_form = callback(item)
            if item_form.is_valid():
                saved_item = item_form.save()
                item['id'] = saved_item.id
                inserted_data.append(item)

        return inserted_data

    def post(self, request):
        day_form_data = {
            'name': request_data['name'] if 'name' in request_data.keys() else None,
            'place': request_data['place'] if 'place' in request_data.keys() else None
        }
        timetable_form_data = request_data['day_timetable'] if 'day_timetable' in request_data.keys() else []
        blocks_form_data = request_data['day_blocks'] if 'day_blocks' in request_data.keys() else []

        day_form = ProgrammeDayForm(day_form_data)
        all_correct = False
        if day_form.is_valid():
            with atomic():
                last_inserted_id = day_form.save()

                self.add_nested_data(
                    data=timetable_form_data,
                    fk_key='day',
                    fk_value=last_inserted_id,
                    callback=lambda form: DayTimetableForm(form)
                )
                inserted_blocks = self.add_nested_data(
                    data=blocks_form_data,
                    fk_key='day',
                    fk_value=last_inserted_id,
                    callback=lambda form: DayBlockForm(form)
                )
                for inserted_block in inserted_blocks:
                    self.add_nested_data(
                        data=inserted_block['reports'] if 'reports' in inserted_block else [],
                        fk_key='block',
                        fk_value=inserted_block['id'],
                        callback=lambda form: ReportForm(form)
                    )
                all_correct = True

        return Response(
            {'message': ''},
            status=status.HTTP_200_OK if all_correct else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )

    def update_nested_data(self, data, callback) -> list:
        updated_data = []

        for item in data:
            serialized_item = callback(item['id'], item)
            if serialized_item.is_valid():
                saved_item = serialized_item.save()
                item['id'] = saved_item.id
                updated_data.append(item)

        return updated_data

    def put(self, request):
        day_form_data = {
            'id': request_data['id'] if 'id' in request_data.keys() else None,
            'name': request_data['name'] if 'name' in request_data.keys() else None,
            'place': request_data['place'] if 'place' in request_data.keys() else None
        }
        timetable_form_data = request_data['day_timetable'] if 'day_timetable' in request_data.keys() else []
        blocks_form_data = request_data['day_blocks'] if 'day_blocks' in request_data.keys() else []

        try:
            day_id = int(day_form_data['id'])
            found_day = ProgrammeDay.objects.get(pk=day_id)
            serialized_day = ProgrammeDaySerializer(found_day, data=day_form_data, partial=True)

            removed_timetable_ids = [item_id.strip() for item_id in request.data.get('removed_timetable', '').split(',')]
            removed_blocks_ids = [item_id.strip() for item_id in request.data.get('removed_blocks', '').split(',')]
            removed_reports_ids = [item_id.strip() for item_id in request.data.get('removed_reports', '').split(',')]

            is_valid = (
                all(item_id.isnumeric() for item_id in removed_timetable_ids) and
                all(item_id.isnumeric() for item_id in removed_blocks_ids) and
                all(item_id.isnumeric() for item_id in removed_reports_ids)
            )

            with atomic():
                if serialized_day.is_valid():
                    serialized_day.save()

                if is_valid:
                    DayTimetable.objects.filter(id__in=removed_timetable_ids).delete()
                    DayBlock.objects.filter(id__in=removed_blocks_ids).delete()
                    Report.objects.filter(id__in=removed_reports_ids).delete()

                self.update_nested_data(
                    data=[item for item in timetable_form_data if 'id' in item.keys()],
                    callback=lambda item_id, item_data: DayTimetableSerializer(
                        DayTimetable.objects.get(pk=int(item_id)),
                        data=item_data,
                        partial=True
                    )
                )
                updated_blocks = self.update_nested_data(
                    data=[item for item in blocks_form_data if 'id' in item.keys()],
                    callback=lambda item_id, item_data: DayBlockSerializer(
                        DayBlock.objects.get(pk=int(item_id)),
                        data={item_key: item_data[item_key] for item_key in item_data.keys() if item_key != 'reports'},
                        partial=True
                    )
                )
                for updated_block_data in updated_blocks:
                    self.update_nested_data(
                        data=[item for item in (updated_block_data['reports']
                                                if 'reports' in updated_block_data else []) if 'id' in item.keys()],
                        callback=lambda item_id, item_data: ReportSerializer(
                            Report.objects.get(pk=int(item_id)),
                            data=item_data,
                            partial=True
                        )
                    )

                self.add_nested_data(
                    data=[item for item in timetable_form_data if 'id' not in item.keys()],
                    fk_key='day',
                    fk_value=found_day.id,
                    callback=lambda form: DayTimetableForm(form)
                )
                inserted_blocks = self.add_nested_data(
                    data=[item for item in blocks_form_data if 'id' not in item.keys()],
                    fk_key='day',
                    fk_value=found_day.id,
                    callback=lambda form: DayBlockForm(form)
                )
                filtered_blocks = [item for item in blocks_form_data if 'id' in item.keys()]
                filtered_blocks.extend(inserted_blocks)
                for block in filtered_blocks:
                    self.add_nested_data(
                        data=[item for item in (block['reports']
                                                if 'reports' in block else []) if 'id' not in item.keys()],
                        fk_key='block',
                        fk_value=block['id'],
                        callback=lambda form: ReportForm(form)
                    )

            response_status = status.HTTP_200_OK

        except (ProgrammeDay.DoesNotExist, ValueError, TypeError):
            message = 'Не найден день программы форума по заданному идентификатору'
            response_status = status.HTTP_404_NOT_FOUND

        return Response(
            {'message': message},
            status=response_status,
            content_type='application/json'
        )
