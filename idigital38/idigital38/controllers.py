from rest_framework import permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models.contexts import DbContext
from .models.serializers import EventSerializer
from .services import EventService


"""
Так выглядит контроллер в Django REST Framework
Существуют функциональные и классовые контроллеры, которые отличаются друг от друга по
стилю написания и возможностям кастомизации

В permission_classes необходимо при готовой авторизации указать разрешения на использование
данного компонента API (с помощью модуля permissions)
Аналогично с аутентификацией

db_context и service - классовые поля, которые можно напрямую задать из urls.py, тем самым
сделав своего рода Dependency Injection

Методы в контроллере называются аналогично HTTP методам (get, post, put) и так далее
Если перейти в APIView и оттуда в View, можно посмотреть все зарезервированные имена
"""


class EventController(APIView):
    permission_classes = []
    authentication_classes = []

    db_context: DbContext = None
    service: EventService = None

    def get(self, request):
        events = self.service.get_all_events(self.db_context)
        # Параметр many указывает на сериализацию коллекции
        serialized_events = EventSerializer(events, many=True)

        return Response(
            serialized_events.data,
            status=status.HTTP_200_OK
        )
