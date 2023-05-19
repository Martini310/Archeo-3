# Generated by Django 4.1.7 on 2023-05-18 21:35

import django.core.validators
from django.db import migrations, models
import kierowca.models


class Migration(migrations.Migration):

    dependencies = [
        ('kierowca', '0002_rename_order_driverorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='pesel',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[kierowca.models.pesel_validation, django.core.validators.MaxLengthValidator(11, 'max 11'), django.core.validators.MinLengthValidator(11, 'min 11')], verbose_name='PESEL'),
        ),
    ]
