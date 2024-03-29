# Generated by Django 4.2.1 on 2023-06-20 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kierowca', '0003_alter_driver_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='zadanie_akt',
            field=models.BooleanField(default=False, verbose_name='Żądanie akt'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='driver',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Oczekuje'), ('o', 'Wypożyczona'), ('r', 'Zwrócona'), ('e', 'Odrzucona'), ('z', 'Żądanie akt')], default='a', max_length=1),
        ),
    ]
