from django.forms import ModelForm

from .models import Appointment


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'contacts', 'organization']
