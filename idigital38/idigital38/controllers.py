from dataclasses import asdict

from rest_framework import permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models.contexts import DbContext
from .models.http import DataResponse, BaseResponse
from .serializers import EventSerializer, OrganizerSerializer
from .services import EventService, ImageService, OrganizerService

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

!!!!!!!!!!!!!!!!!!
ВАЖНО: Для корректной работы нужно создать в idigital38/idigital38 каталог media/pics с папками events и organizers,
чтобы обеспечить сохранение изображений на сервере, получаемых от клиента
!!!!!!!!!!!!!!!!!!
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

        events = self.event_service.get_all_events(self.db_context) if event_id is None else \
            [self.event_service.get_event_by_id(self.db_context, event_id)]
        serialized_events = []

        for event in events:
            if event is not None:
                additional_params = None if event.image_uri is None else \
                    {'image': self.image_service.read_image(event.image_uri)}
                serialized_event = self.event_serializer.serialize(
                    event,
                    additional_params=additional_params
                )
                serialized_events.append(serialized_event)

        if event_id is None or len(serialized_events) != 0:
            response = DataResponse(
                data=serialized_events,
                message='Не найдено ни одного мероприятия' if len(serialized_events) == 0 else ''
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

            directory = 'idigital38/idigital38/media/pics/events'
            events = list(filter(lambda event_item: event_item.image_uri is not None,
                                 self.event_service.get_all_events(self.db_context)))
            image_uris = [event.image_uri for event in events]
            self.image_service.remove_unused_images(image_uris, directory)

        return Response(
            asdict(
                BaseResponse(
                    message='Идентификаторы должны быть целыми числами' if not is_valid else ''
                )
            ),
            status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )

    def post(self, request):
        if 'image' in request.FILES.keys():
            directory = 'idigital38/idigital38/media/pics/events'

            image_uri = '{0}/{1}'.format(directory, request.FILES['image'])
            self.image_service.write_image(request.FILES['image'].file.read(), image_uri)
            request.data['image_uri'] = image_uri

        event = self.event_serializer.deserialize(request.data)
        self.event_service.add_event(self.db_context, event)

        return Response(
            asdict(
                BaseResponse(
                    message=''
                )
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    def put(self, request):
        directory = 'idigital38/idigital38/media/pics/events'

        if 'image' in request.FILES.keys():
            image_uri = '{0}/{1}'.format(directory, request.FILES['image'])
            self.image_service.write_image(request.FILES['image'].file.read(), image_uri)
            request.data['image_uri'] = image_uri

        event = self.event_serializer.deserialize(request.data)
        self.event_service.edit_event(self.db_context, event)

        events = list(filter(lambda event_item: event_item.image_uri is not None,
                             self.event_service.get_all_events(self.db_context)))

        image_uris = [event.image_uri for event in events]
        self.image_service.remove_unused_images(image_uris, directory)

        return Response(
            asdict(
                BaseResponse(
                    message=''
                )
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
        )


class OrganizerController(APIView):
    permission_classes = []
    authentication_classes = []

    db_context: DbContext = None
    image_service: ImageService = None
    organizer_serializer: OrganizerSerializer = None
    organizer_service: OrganizerService = None

    def get(self, request):
        organizer_id = request.GET.get('id', None)

        organizers = self.organizer_service.get_all_organizers(self.db_context) if organizer_id is None else \
            [self.organizer_service.get_organizer_by_id(self.db_context, organizer_id)]
        serialized_organizers = []

        for organizer in organizers:
            if organizer is not None:
                additional_params = None if organizer.image_uri is None else \
                    {'image': self.image_service.read_image(organizer.image_uri)}
                serialized_organizer = self.organizer_serializer.serialize(
                    organizer,
                    additional_params=additional_params
                )
                serialized_organizers.append(serialized_organizer)

        if organizer_id is None or len(serialized_organizers) != 0:
            response = DataResponse(
                data=serialized_organizers,
                message='Не найдено ни одного члена организационного комитета' if len(serialized_organizers) == 0 else ''
            )
        else:
            response = BaseResponse(
                message='Член организационного комитета не найден'
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
            self.organizer_service.remove_organizers_by_ids(self.db_context, ids)

            directory = 'idigital38/idigital38/media/pics/organizers'
            organizers = list(filter(lambda organizer_item: organizer_item.image_uri is not None,
                                     self.organizer_service.get_all_organizers(self.db_context)))
            image_uris = [organizer.image_uri for organizer in organizers]
            self.image_service.remove_unused_images(image_uris, directory)

        return Response(
            asdict(
                BaseResponse(
                    message='Идентификаторы должны быть целыми числами' if not is_valid else ''
                )
            ),
            status=status.HTTP_200_OK if is_valid else status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )

    def post(self, request):
        if 'image' in request.FILES.keys():
            directory = 'idigital38/idigital38/media/pics/organizers'

            image_uri = '{0}/{1}'.format(directory, request.FILES['image'])
            self.image_service.write_image(request.FILES['image'].file.read(), image_uri)
            request.data['image_uri'] = image_uri

        organizer = self.organizer_serializer.deserialize(request.data)
        organizer.order = self.organizer_service.calculate_order(self.db_context)
        self.organizer_service.add_organizer(self.db_context, organizer)

        return Response(
            asdict(
                BaseResponse(
                    message=''
                )
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    def put(self, request):
        directory = 'idigital38/idigital38/media/pics/organizers'

        if 'image' in request.FILES.keys():
            image_uri = '{0}/{1}'.format(directory, request.FILES['image'])
            self.image_service.write_image(request.FILES['image'].file.read(), image_uri)
            request.data['image_uri'] = image_uri

        organizer = self.organizer_serializer.deserialize(request.data)
        self.organizer_service.edit_organizer(self.db_context, organizer)

        organizers = list(filter(lambda organizer_item: organizer_item.image_uri is not None,
                                 self.organizer_service.get_all_organizers(self.db_context)))

        image_uris = [organizer.image_uri for organizer in organizers]
        self.image_service.remove_unused_images(image_uris, directory)

        return Response(
            asdict(
                BaseResponse(
                    message=''
                )
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    def patch(self, request):
        self.organizer_service.edit_organizers_order(self.db_context, request.data)

        return Response(
            asdict(
                BaseResponse(
                    message=''
                )
            ),
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
