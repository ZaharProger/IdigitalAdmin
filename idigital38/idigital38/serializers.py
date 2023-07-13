import base64
from abc import ABC, abstractmethod
from dataclasses import asdict

from .models.db_entities import Event, Organizer


class BaseSerializer(ABC):
    @abstractmethod
    def serialize(self, entity, additional_params=None):
        pass

    @abstractmethod
    def deserialize(self, dictionary):
        pass


class EventSerializer(BaseSerializer):
    def serialize(self, entity, additional_params=None):
        event_dict = asdict(entity)
        event_dict.pop('image_uri')
        if entity.image_uri is not None and additional_params is not None:
            image_bytes = additional_params['image'] if 'image' in additional_params.keys() else None
            event_dict['image'] = str(base64.b64encode(image_bytes)) if image_bytes is not None else None

        return event_dict

    def deserialize(self, dictionary):
        event = Event(
            name=dictionary['name'],
            date=int(dictionary['date']),
            ref=dictionary['ref'],
            image_uri=dictionary['image_uri'] if 'image_uri' in dictionary.keys() else None
        )
        if 'id' in dictionary.keys():
            event.id = int(dictionary['id'])

        return event


class OrganizerSerializer(BaseSerializer):
    def serialize(self, entity, additional_params=None):
        organizer_dict = asdict(entity)
        organizer_dict.pop('image_uri')
        if entity.image_uri is not None and additional_params is not None:
            image_bytes = additional_params['image'] if 'image' in additional_params.keys() else None
            organizer_dict['image'] = str(base64.b64encode(image_bytes)) if image_bytes is not None else None

        return organizer_dict

    def deserialize(self, dictionary):
        organizer = Organizer(
            name=dictionary['name'],
            role=dictionary['role'],
            additional_role=dictionary['additional_role'] if 'additional_role' in dictionary.keys() else None,
            image_uri=dictionary['image_uri'] if 'image_uri' in dictionary.keys() else None,
        )
        if 'id' in dictionary.keys():
            organizer.id = int(dictionary['id'])
        if 'order' in dictionary.keys():
            organizer.order = int(dictionary['order'])

        return organizer
