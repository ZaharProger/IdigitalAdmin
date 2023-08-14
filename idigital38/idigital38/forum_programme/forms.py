from django.forms import ModelForm

from .models import ProgrammeDay, Report, DayBlock, DayTimetable


class ProgrammeDayForm(ModelForm):
    class Meta:
        model = ProgrammeDay
        fields = ['name', 'place']


class DayTimetableForm(ModelForm):
    class Meta:
        model = DayTimetable
        fields = ['name', 'time_start', 'time_end', 'moderators', 'speakers', 'day']


class DayBlockForm(ModelForm):
    class Meta:
        model = DayBlock
        fields = ['name', 'place', 'moderators', 'day']


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'time_start', 'time_end', 'speakers', 'block']
