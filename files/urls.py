from django.urls import path
from . import views

app_name = 'files'

urlpatterns = [
    path('list/', views.list_cars, name='list'),
    path('add/', views.AddVehicle.as_view(), name='add'), 
    path('order/', views.AddOrder.as_view(), name='order'), 
    path('my_order/', views.my_order, name='my_order')
]
