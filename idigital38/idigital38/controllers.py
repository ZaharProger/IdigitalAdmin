from dataclasses import asdict

from rest_framework import permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models.contexts import DbContext
from .models.http import DataResponse, BaseResponse
from .serializers import EventSerializer
from .services import EventService, ImageService

"""
Так выглядит контроллер в Django REST Framework
Существуют функциональные и классовые контроллеры, которые отличаются друг от друга по
стилю написания и возможностям кастомизации

В permission_classes необходимо при готовой авторизации указать разрешения на использование
данного компонента API (с помощью модуля permissions)
Аналогично с аутентификацией

Есть классовые поля, которые можно напрямую задать из urls.py, тем самым
сделав своего рода Dependency Injection

Методы в контроллере называются аналогично HTTP методам (get, post, put) и так далее
Если перейти в APIView и оттуда в View, можно посмотреть все зарезервированные имена
"""


class EventController(APIView):
    permission_classes = []
    authentication_classes = []

    db_context: DbContext = None
    event_service: EventService = None
    image_service: ImageService = None
    event_serializer: EventSerializer = None

    def get(self, request):
        event_id = request.GET.get('id', None)

        if event_id is None:
            events = self.event_service.get_all_events(self.db_context)
            serialized_events = [self.event_serializer.serialize(event) for event in events]

            response = DataResponse(
                data=serialized_events,
                message='Не найдено ни одного мероприятия' if len(serialized_events) == 0 else ''
            )
        else:
            event = self.event_service.get_event_by_id(self.db_context, event_id)
            if event is not None:
                serialized_event = self.event_serializer.serialize(event)
                response = DataResponse(
                    data=serialized_event,
                    message=''
                )
            else:
                response = BaseResponse(
                    message='Мероприятие не найдено'
                )

        return Response(
            asdict(response),
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    def delete(self, request):
        ids = [item_id.strip() for item_id in request.GET.get('ids', '0').split(',')]
        is_valid = all(item_id.isnumeric() for item_id in ids)

        if is_valid:
            self.event_service.remove_events_by_ids(self.db_context, ids)

        return Response(
            asdict(
                BaseResponse(
                    message='Идентификаторы должны быть целыми числами' if not is_valid else ''
                )
            ),
            status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
