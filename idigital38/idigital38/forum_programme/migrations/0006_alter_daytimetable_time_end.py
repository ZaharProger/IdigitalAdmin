# Generated by Django 4.1 on 2023-08-03 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_programme', '0005_programmeday_place_alter_dayblock_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daytimetable',
            name='time_end',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
