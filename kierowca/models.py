# pylint: disable=no-member
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class DriverOrder(models.Model):
    order_date = models.DateTimeField('Data zamówienia', auto_now_add=True)
    orderer = models.ForeignKey(User, related_name="dirver_orders", on_delete=models.RESTRICT, verbose_name='Zamawiający')

    def __str__(self) -> str:
        return f"Zamówienie nr {self.id}. Data: {self.order_date.strftime('%d-%m-%Y %H:%M.%S')}. Zamawiający: {self.orderer}"


class Driver(models.Model):
    first_name = models.CharField('Imię', max_length=100)
    last_name = models.CharField('Nazwisko', max_length=100)
    pesel = models.CharField('PESEL', max_length=11, blank=True, null=True)
    kk = models.CharField('Numer K/K',max_length=15 , blank=True, null=True)
    birth_date = models.DateField('Data urodzenia')
    transfer_date = models.DateTimeField('Data pobrania', blank=True, null=True)
    return_date = models.DateTimeField('Data zwrotu', blank=True, null=True)
    responsible_person = models.ForeignKey(User, related_name="drivers", on_delete=models.RESTRICT, verbose_name='Pobierający')
    transfering_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='transfering_drivers', blank=True, null=True, verbose_name='Przekazano do')
    comments = models.CharField('Uwagi', max_length=100, null=True, blank=True)
    LOAN_STATUS = (
        ('a', 'Oczekuje'), # a - Awaits
        ('o', 'Wypożyczona'), # o - On loan
        ('r', 'Zwrócona'), # r - Returned
        ('e', 'Odrzucona'), # e - Rejected/error
        ('z', 'Żądanie akt')
    )
    status = models.CharField(max_length=1, blank=True, choices=LOAN_STATUS, default='a')
    order = models.ForeignKey(DriverOrder, related_name="drivers", on_delete=models.SET_NULL, null=True, verbose_name='Zamówienie')
    returner = models.ForeignKey(User, related_name='drivers_returner', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Zwracający')
    zadanie_akt = models.BooleanField(verbose_name='Żądanie akt')

    def __str__(self):
        return f'{self.first_name} {self.last_name}. Pesel: {self.pesel}'
    
    def get_fields(self):
        return [(field.verbose_name, getattr(self,field.name)) for field in Driver._meta.fields]
    
    class Meta:
        permissions = [
            ("return_driver", "Can return driver"),
            ("transfer_driver", "Can transfer driver"),
        ]
