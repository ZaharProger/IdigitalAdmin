# Generated by Django 4.1 on 2023-09-27 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='organization',
            field=models.CharField(choices=[('Школа (ученик)', 'School'), ('Университет (студент)', 'University'), ('Предприятие (сотрудник компании)', 'Company')], default='Школа (ученик)', max_length=100),
        ),
    ]
