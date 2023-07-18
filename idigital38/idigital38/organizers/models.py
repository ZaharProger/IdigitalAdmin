from django.db.models import Model, CharField, ImageField, SmallIntegerField


class Organizer(Model):
    name = CharField(default='', max_length=100)
    image_uri = ImageField(upload_to='static/pics/organizers', null=True)
    role = CharField(default='', max_length=100)
    additional_role = CharField(max_length=100, null=True)
    order = SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'organizer'
        verbose_name_plural = 'organizers'
