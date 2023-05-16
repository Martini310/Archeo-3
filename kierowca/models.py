# pylint: disable=no-member
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
        ('e', 'Odrzucona') # e - Rejected/error
    )
    status = models.CharField(max_length=1, blank=True, choices=LOAN_STATUS, default='a')
    order = models.ForeignKey(DriverOrder, related_name="drivers", on_delete=models.SET_NULL, null=True, verbose_name='Zamówienie')
    returner = models.ForeignKey(User, related_name='drivers_returner', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Zwracający')


    def clean(self):
        """ Check that the PESEL number is correct and that the checksum is correct """
        if len(self.pesel) != 11:
            raise ValidationError(
                'Pesel musi mieć 11 znaków')
        
        control_sum = 0
        multipliers = {1: 1, 2: 3, 3: 7, 4: 9, 5: 1, 6: 3, 7: 7, 8: 9, 9: 1, 10: 3}
        for index, number in enumerate(self.pesel[:-1], start=1):
            control_sum += int(number) * multipliers[index]

        if 10 - (control_sum % 10) != int(self.pesel[-1]):
            raise ValidationError('PESEL: Błędna cyfra kontrolna')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}. Pesel: {self.pesel}'
    
    def get_fields(self):
        return [(field.verbose_name, getattr(self,field.name)) for field in Driver._meta.fields]
    