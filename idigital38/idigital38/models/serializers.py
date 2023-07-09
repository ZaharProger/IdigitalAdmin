from rest_framework import serializers

from .db_entities import Event
from ..services import ImageService


class EventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('__get_image_by_uri')

    def __get_image_by_uri(self, event: Event):
        image_service = ImageService()
        return image_service.read_image(event.image_uri)

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'image', 'ref')
