from django.db.models import Model, CharField, TextChoices


class Appointment(Model):
    class OrganizationTypes(TextChoices):
        SCHOOL = 'Школа (ученик)'
        UNIVERSITY = 'Университет (студент)'
        COMPANY = 'Предприятие (сотрудник компании)'

    name = CharField(default='', max_length=100)
    contacts = CharField(default='', max_length=100)
    organization = CharField(
        default=OrganizationTypes.SCHOOL,
        max_length=100,
        choices=OrganizationTypes.choices
    )

    class Meta:
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
