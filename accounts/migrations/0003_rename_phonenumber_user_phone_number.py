# Generated by Django 4.2.5 on 2023-10-04 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phonenumber',
            new_name='phone_number',
        ),
    ]
