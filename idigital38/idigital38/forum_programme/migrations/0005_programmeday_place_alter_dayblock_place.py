# Generated by Django 4.1 on 2023-07-30 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_programme', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmeday',
            name='place',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='dayblock',
            name='place',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
    ]
