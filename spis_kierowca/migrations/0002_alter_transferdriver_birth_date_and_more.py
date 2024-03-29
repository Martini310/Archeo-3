# Generated by Django 4.2.1 on 2023-06-16 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spis_kierowca', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferdriver',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data urodzenia'),
        ),
        migrations.AlterField(
            model_name='transferdriver',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Imię'),
        ),
        migrations.AlterField(
            model_name='transferdriver',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nazwisko'),
        ),
        migrations.AlterField(
            model_name='transferdriver',
            name='transfer_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='transfer_list', to='spis_kierowca.transferlistkierowca'),
        ),
    ]
