from django.forms import ModelForm

from .models import Organizer


class OrganizerForm(ModelForm):
    class Meta:
        model = Organizer
        fields = ['name', 'role', 'additional_role', 'image_uri']
