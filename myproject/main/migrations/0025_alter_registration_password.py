# Generated by Django 4.0.4 on 2023-06-19 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_registration_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='password',
            field=models.CharField(max_length=30, verbose_name='Password'),
        ),
    ]
