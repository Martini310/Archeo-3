# Generated by Django 4.1.6 on 2023-04-21 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0008_alter_vehicle_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicle',
            options={'permissions': [('return_vehicle', 'Can return vehicle'), ('transfer_vehicle', 'Can transfer vehicle')]},
        ),
    ]
