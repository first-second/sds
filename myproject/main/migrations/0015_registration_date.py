# Generated by Django 4.0.4 on 2022-05-18 07:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_registration_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2022, 5, 18, 7, 4, 58, 928878, tzinfo=utc)),
            preserve_default=False,
        ),
    ]