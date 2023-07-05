from django.db import models
from django.contrib.auth.models import User
import locale

# Create your models here.
# locale.setlocale(locale.LC_TIME, "pl_PL")

class TransferListKierowca(models.Model):
    date = models.DateTimeField('Data spisu', auto_now_add=True)
    responsible_person = models.ForeignKey(User, related_name='spisy', on_delete=models.DO_NOTHING)
    
    def __str__(self) -> str:
        return f"Protokół nr {self.pk} z dnia {self.date.strftime('%d %B %Y, g.%H:%M')}."
    

class TransferDriver(models.Model):
    first_name = models.CharField('Imię', max_length=100)
    last_name = models.CharField('Nazwisko', max_length=100)
    pesel = models.CharField('PESEL', max_length=11, blank=True, null=True)
    kk = models.CharField('Numer K/K',max_length=15 , blank=True, null=True)
    birth_date = models.DateField('Data urodzenia')
    transfer_list = models.ForeignKey(TransferListKierowca, related_name='transfer_list', on_delete=models.DO_NOTHING, blank=True, null=True)
    comments = models.CharField('Uwagi', max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"ID: {self.pk}. {self.first_name} {self.last_name}, pesel {self.pesel or ''}. {self.comments or ''}"
    
    def get_fields(self):
        return [(field.verbose_name, getattr(self,field.name)) for field in TransferDriver._meta.fields]
    