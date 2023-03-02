from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    order_date = models.DateTimeField()
    orderer = models.ForeignKey(User, related_name="orders", on_delete=models.RESTRICT)

    def __str__(self) -> str:
        return f"Zamówienie nr {self.id}. Data: {self.order_date}. Zamawiający: {self.orderer}"


class Vehicle(models.Model):
    tr = models.CharField(max_length=8)
    transfer_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    responsible_person = models.ForeignKey(User, related_name="vehicles", on_delete=models.RESTRICT)
    comments = models.CharField(max_length=100)
    LOAN_STATUS = (
        ('a', 'Awaits'), 
        ('o', 'On Loan'), 
        ('r', 'Returned'),
        ('e', 'rejected')
    )
    status = models.CharField(max_length=1, blank=True, choices=LOAN_STATUS, default='a')
    order = models.ForeignKey(Order, related_name="vehicles", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.tr}, POBRAŁ: {self.responsible_person}, STATUS: {self.status}, ZAMÓWIENIE: {self.order.id}"
