# Generated by Django 4.1.7 on 2023-05-04 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0011_alter_vehicle_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='tr',
            field=models.CharField(max_length=9, verbose_name='TR'),
        ),
    ]
