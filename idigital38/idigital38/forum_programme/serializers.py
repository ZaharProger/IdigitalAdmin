from rest_framework.serializers import ModelSerializer

from .models import ProgrammeDay, Report, DayTimetable, DayBlock


class DayTimetableSerializer(ModelSerializer):
    class Meta:
        model = DayTimetable
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class DayBlockSerializer(ModelSerializer):
    reports = ReportSerializer(many=True, source='report_block')

    class Meta:
        model = DayBlock
        fields = ['id', 'name', 'place', 'moderators', 'day', 'reports']


class ProgrammeDaySerializer(ModelSerializer):
    day_timetable = DayTimetableSerializer(many=True, source='timetable_day')
    day_blocks = DayBlockSerializer(many=True, source='block_day')

    class Meta:
        model = ProgrammeDay
        fields = ['id', 'name', 'place', 'day_timetable', 'day_blocks']
