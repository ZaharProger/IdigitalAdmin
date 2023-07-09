from dataclasses import asdict

from rest_framework import permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models.contexts import DbContext
from .models.http import DataResponse
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
        events = self.event_service.get_all_events(self.db_context)
        serialized_events = [self.event_serializer.serialize(event) for event in events]

        return Response(
            asdict(
                DataResponse(
                    data=serialized_events,
                    message='Не найдено ни одного мероприятия' if len(serialized_events) == 0 else ''
                )
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
