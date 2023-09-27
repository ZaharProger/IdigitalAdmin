from django.db.models import Model, CharField, TextChoices


class Appointment(Model):
    class OrganizationTypes(TextChoices):
        SCHOOL = 'Школа (Я ученик)'
        UNIVERSITY = 'Университет (Я студент)'
        COMPANY = 'Предприятие (Я сотрудник компании)'

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
