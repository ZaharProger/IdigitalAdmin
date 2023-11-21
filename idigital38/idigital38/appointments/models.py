from django.db.models import Model, CharField, TextChoices


class Appointment(Model):

    class OrganizationTypes(TextChoices):
        SCHOOL = 'Школа (ученик)'
        UNIVERSITY = 'Университет, СПО (студент)'
        COMPANY = 'Предприятие (сотрудник компании)'

    class ParticipationTypes(TextChoices):
        PARTICIPANT = 'Участник'
        PARTNER = 'Партнер'

    name = CharField(default='', max_length=100)
    status = CharField(default='', max_length=100)
    organization = CharField(
        default=OrganizationTypes.SCHOOL,
        max_length=100,
        choices=OrganizationTypes.choices
    )
    email = CharField(default='', max_length=100)
    phone = CharField(default='', max_length=100)
    participation_type = CharField(
        default=ParticipationTypes.PARTICIPANT,
        max_length=50,
        choices=ParticipationTypes.choices
    )
    sections = CharField(default='', max_length=500)

    class Meta:
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
