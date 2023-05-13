# Generated by Django 4.1.7 on 2023-05-13 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Data zamówienia')),
                ('orderer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Zamawiający')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tr', models.CharField(max_length=9, verbose_name='TR')),
                ('transfer_date', models.DateTimeField(blank=True, null=True, verbose_name='Data pobrania')),
                ('return_date', models.DateTimeField(blank=True, null=True, verbose_name='Data zwrotu')),
                ('comments', models.CharField(blank=True, max_length=100, null=True, verbose_name='Uwagi')),
                ('status', models.CharField(blank=True, choices=[('a', 'Oczekuje'), ('o', 'Wypożyczona'), ('r', 'Zwrócona'), ('e', 'Odrzucona')], default='a', max_length=1)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to='pojazd.order', verbose_name='Zamówienie')),
                ('responsible_person', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='vehicles', to=settings.AUTH_USER_MODEL, verbose_name='Pobierający')),
                ('returner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles_returner', to=settings.AUTH_USER_MODEL, verbose_name='Zwracający')),
                ('transfering_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfering', to=settings.AUTH_USER_MODEL, verbose_name='Przekazano do')),
            ],
            options={
                'permissions': [('return_vehicle', 'Can return vehicle'), ('transfer_vehicle', 'Can transfer vehicle')],
            },
        ),
    ]
