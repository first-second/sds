# Generated by Django 4.0.4 on 2023-06-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_alter_registration_email_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]