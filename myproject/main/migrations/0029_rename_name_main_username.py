# Generated by Django 4.0.4 on 2023-06-21 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_rename_username_main_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='main',
            old_name='name',
            new_name='username',
        ),
    ]
