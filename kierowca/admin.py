from django.contrib import admin
from .models import DriverOrder, Driver

# Register your models here.
admin.site.register(Driver)
admin.site.register(DriverOrder)
