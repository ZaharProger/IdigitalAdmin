from rest_framework import serializers

from .db_entities import Event
from ..services import ImageService


"""
    Сериализаторы нужны для подготовки и представления данных из моделей в удобной форме для передачи клиенту
    В них можно указать какие именно поля нужно сериализовать из текущей модели, но также
    можно определить и свои поля, значение которых можно определить путём вызова некоторой функции
    
    Для этого нужно пометить поле как SerializerMethodField и в качестве параметра передать название метода
    Собственно сам метод должен быть описан в сериализаторе
"""


class EventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('__get_image_by_uri')

    def __get_image_by_uri(self, event: Event):
        image_service = ImageService()
        return image_service.read_image(event.image_uri)

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'image', 'ref')
