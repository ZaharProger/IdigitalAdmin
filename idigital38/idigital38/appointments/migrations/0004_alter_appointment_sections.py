# Generated by Django 4.1 on 2023-11-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_remove_appointment_contacts_appointment_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='sections',
            field=models.CharField(default='', max_length=500),
        ),
    ]
