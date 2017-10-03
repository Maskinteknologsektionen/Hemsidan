# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-05 06:52
from __future__ import unicode_literals

import aldryn_apphooks_config.fields
import app_data.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('name', models.CharField(default=b'', max_length=30, verbose_name='name')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.DateTimeField(unique=True, verbose_name='start')),
                ('end', models.DateTimeField(unique=True, verbose_name='end')),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
        ),
        migrations.CreateModel(
            name='BookingConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
                ('namespace', models.CharField(default=None, max_length=100, unique=True, verbose_name='Instance namespace')),
                ('app_data', app_data.fields.AppDataField(default=b'{}', editable=False)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Apphook config',
                'verbose_name_plural': 'Apphook configs',
            },
        ),
        migrations.CreateModel(
            name='BookingSpot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField(verbose_name='start')),
                ('end', models.TimeField(verbose_name='end')),
            ],
            options={
                'verbose_name': 'Booking spot',
                'verbose_name_plural': 'Booking spots',
            },
        ),
        migrations.AddField(
            model_name='bookingconfig',
            name='booking_spots',
            field=models.ManyToManyField(to='booking_app.BookingSpot', verbose_name='Booking spots'),
        ),
        migrations.AddField(
            model_name='booking',
            name='app_config',
            field=aldryn_apphooks_config.fields.AppHookConfigField(default=None, help_text='When selecting a value, the form is reloaded to get the updated default', on_delete=django.db.models.deletion.CASCADE, to='booking_app.BookingConfig', verbose_name='app config'),
        ),
        migrations.AddField(
            model_name='booking',
            name='madeBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='made by'),
        ),
        migrations.AlterUniqueTogether(
            name='bookingconfig',
            unique_together=set([('type', 'namespace')]),
        ),
    ]
