# Generated by Django 5.0.5 on 2024-06-07 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_openinghour_options_alter_openinghour_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='office_phone',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
