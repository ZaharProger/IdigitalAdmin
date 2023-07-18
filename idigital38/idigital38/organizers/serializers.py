from rest_framework.serializers import ModelSerializer
from .models import Organizer


class OrganizerSerializer(ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'
