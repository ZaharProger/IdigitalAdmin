from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Organizer


class OrganizerSerializer(ModelSerializer):
    image = SerializerMethodField('get_image_by_uri')

    def get_image_by_uri(self, obj):
        with open(obj.image_uri, 'rb') as image:
            image_data = image.read()

        return image_data

    class Meta:
        model = Organizer
        exclude = ['image_uri']
