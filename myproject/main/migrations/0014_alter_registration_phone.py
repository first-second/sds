# Generated by Django 4.0.4 on 2022-05-18 06:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_registration_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='phone',
            field=models.CharField(blank=True, max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. 10 digits allowed.", regex='^\\+?1?\\d{10}$')]),
        ),
    ]
