import base64
from abc import ABC, abstractmethod
from dataclasses import asdict

from .services import ImageService


class BaseSerializer(ABC):
    @abstractmethod
    def serialize(self, entity):
        pass

    @abstractmethod
    def deserialize(self, dictionary):
        pass


class EventSerializer(BaseSerializer):
    def __init__(self, image_service: ImageService):
        self.__service = image_service

    def serialize(self, entity):
        event_dict = asdict(entity)
        event_dict.pop('image_uri')
        if self.__service:
            if entity.image_uri:
                image_bytes = self.__service.read_image(entity.image_uri)
                event_dict['image'] = str(base64.b64encode(image_bytes))

        return event_dict

    def deserialize(self, dictionary):
        pass
