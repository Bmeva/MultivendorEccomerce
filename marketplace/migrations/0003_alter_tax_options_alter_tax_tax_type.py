# Generated by Django 5.0.1 on 2024-01-13 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_tax'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name_plural': 'Tax'},
        ),
        migrations.AlterField(
            model_name='tax',
            name='tax_type',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
