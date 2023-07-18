from django.db.models import Model, CharField, ImageField, BigIntegerField


class Event(Model):
    name = CharField(default='', max_length=100)
    date = BigIntegerField(default=0)
    image_uri = ImageField(upload_to='pics/events', null=True, blank=True)
    ref = CharField(default='', max_length=150)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
