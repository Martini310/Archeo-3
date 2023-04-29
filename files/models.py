# pylint: disable=no-member
from django.db import models
from django.contrib.auth.models import User
from django.template.defaulttags import register

# Create your models here.
class Order(models.Model):
    order_date = models.DateTimeField('Data zamówienia')
    orderer = models.ForeignKey(User, related_name="orders", on_delete=models.RESTRICT, verbose_name='Zamawiający')

    def __str__(self) -> str:
        return f"Zamówienie nr {self.id}. Data: {self.order_date.strftime('%d-%m-%Y %H:%M.%S')}. Zamawiający: {self.orderer}"


class Vehicle(models.Model):
    tr = models.CharField('TR', max_length=8)
    transfer_date = models.DateTimeField('Data pobrania', blank=True, null=True)
    return_date = models.DateTimeField('Data zwrotu', blank=True, null=True)
    responsible_person = models.ForeignKey(User, related_name="vehicles", on_delete=models.RESTRICT, verbose_name='Pobierający')
    transfering_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='transfering', blank=True, null=True, verbose_name='Przekazano do')
    comments = models.CharField('Uwagi', max_length=100, null=True, blank=True)
    LOAN_STATUS = (
        ('a', 'Oczekuje'), # a - Awaits
        ('o', 'Wypożyczona'), # o - On loan
        ('r', 'Zwrócona'), # r - Returned
        ('e', 'Odrzucona') # e - Rejected/error
    )
    status = models.CharField(max_length=1, blank=True, choices=LOAN_STATUS, default='a')
    order = models.ForeignKey(Order, related_name="vehicles", on_delete=models.SET_NULL, null=True, verbose_name='Zamówienie')
    returner = models.ForeignKey(User, related_name='vehicles_returner', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Zwracający')

    def __str__(self) -> str:
        if self.status == 'o':
            return f"Teczka {self.tr} została pobrana przez: {self.responsible_person} w dniu {self.transfer_date.strftime('%d-%m-%Y %H:%M.%S')}. Nr zamówienia: {self.order.id}."
        elif self.status == 'a':
            return f"Teczka {self.tr} została zamówiona przez: {self.responsible_person} w dniu {self.order.order_date.strftime('%d-%m-%Y %H:%M.%S')}. Nr zamówienia: {self.order.id}."
        elif self.status == 'r':
            return f"Teczka {self.tr} została zwrócona przez: {self.returner} w dniu {self.return_date.strftime('%d-%m-%Y %H:%M.%S')}."
        elif self.status == 'e':
            return f"Teczka {self.tr} zamówiona przez: {self.responsible_person} została odrzucona. Nr zamówienia: {self.order.id}."
    
    def get_fields(self):
        return [(field.verbose_name, getattr(self,field.name)) for field in Vehicle._meta.fields]
    
    @register.filter
    def get_item(dictionary , key):
        dictionary = dict(dictionary)
        return dictionary.get(key)
    
    class Meta:
        permissions = [
            ("return_vehicle", "Can return vehicle"),
            ("transfer_vehicle", "Can transfer vehicle"),
        ]
