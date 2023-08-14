from django.db.models import Model, CharField, BigIntegerField, \
    ForeignKey, CASCADE


class ProgrammeDay(Model):
    name = CharField(default='', max_length=100)
    place = CharField(default='', max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = 'programme_day'
        verbose_name_plural = 'programme_days'


class DayTimetable(Model):
    name = CharField(default='', max_length=100)
    time_start = BigIntegerField(default=0)
    time_end = BigIntegerField(default=0, null=True, blank=True)
    moderators = CharField(default='', max_length=500, null=True, blank=True)
    speakers = CharField(default='', max_length=500, null=True, blank=True)
    day = ForeignKey(to=ProgrammeDay, on_delete=CASCADE, null=True, blank=True, related_name='timetable_day')

    class Meta:
        verbose_name = 'day_timetable'
        verbose_name_plural = 'day_timetables'


class DayBlock(Model):
    name = CharField(default='', max_length=150)
    place = CharField(default='', max_length=150, null=True, blank=True)
    moderators = CharField(default='', max_length=500, null=True, blank=True)
    day = ForeignKey(to=ProgrammeDay, on_delete=CASCADE, null=True, blank=True, related_name='block_day')

    class Meta:
        verbose_name = 'day_block'
        verbose_name_plural = 'day_blocks'


class Report(Model):
    name = CharField(default='', max_length=150)
    time_start = BigIntegerField(default=0)
    time_end = BigIntegerField(default=0)
    speakers = CharField(default='', max_length=500, null=True, blank=True)
    block = ForeignKey(to=DayBlock, on_delete=CASCADE, null=True, blank=True, related_name='report_block')

    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'
