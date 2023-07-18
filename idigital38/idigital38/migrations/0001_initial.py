# Generated by Django 4.1 on 2023-07-18 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('date', models.BigIntegerField(default=0)),
                ('image_uri', models.ImageField(null=True, upload_to='static/pics/events')),
                ('ref', models.CharField(default='', max_length=150)),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('image_uri', models.ImageField(null=True, upload_to='static/pics/organizers')),
                ('role', models.CharField(default='', max_length=100)),
                ('additional_role', models.CharField(max_length=100, null=True)),
                ('order', models.SmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'organizer',
                'verbose_name_plural': 'organizers',
            },
        ),
    ]
