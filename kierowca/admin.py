from django.contrib import admin
from .models import Order, Driver

# Register your models here.
admin.site.register(Driver)
admin.site.register(Order)
