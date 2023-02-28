from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    order_date = models.DateTimeField()


class Vehicle(models.Model):
    tr = models.CharField(max_length=8)
    transfer_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    responsible_person = models.ForeignKey(User, on_delete=models.RESTRICT)
    comments = models.CharField(max_length=100)
    LOAN_STATUS = (
        ('a', 'Awaits'), 
        ('o', 'On Loan'), 
        ('r', 'Returned'),
        ('e', 'rejected')
    )
    status = models.CharField(max_length=1, blank=True, choices=LOAN_STATUS, default='a')
    order = models.ManyToManyField(Order)

    def __str__(self) -> str:
        return f"{self.tr}, pobrał: {self.responsible_person}, status: {self.status}, zamówienie: {self.order}"
