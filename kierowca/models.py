from django.db import models
from django.contrib.auth.models import User
from localflavor.pl.forms import PLPESELField

# Create your models here.

class Order(models.Model):
    order_date = models.DateTimeField('Data zamówienia', auto_now_add=True)
    orderer = models.ForeignKey(User, related_name="orders", on_delete=models.RESTRICT, verbose_name='Zamawiający')

    def __str__(self) -> str:
        return f"Zamówienie nr {self.id}. Data: {self.order_date.strftime('%d-%m-%Y %H:%M.%S')}. Zamawiający: {self.orderer}"


class Driver(models.Model):
    first_name = models.CharField('Imię', max_length=100)
    last_name = models.CharField('Nazwisko', max_length=100)
    pesel = models.DecimalField('PESEL')
    