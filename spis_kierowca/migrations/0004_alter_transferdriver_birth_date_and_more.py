# Generated by Django 4.2.1 on 2023-06-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spis_kierowca', '0003_alter_transferdriver_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferdriver',
            name='birth_date',
            field=models.DateField(verbose_name='Data urodzenia'),
        ),
        migrations.AlterField(
            model_name='transferdriver',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Nazwisko'),
        ),
    ]
