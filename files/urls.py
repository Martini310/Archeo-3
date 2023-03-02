from django.urls import path
from . import views

app_name = 'files'

urlpatterns = [
    path('list/', views.list_cars, name='list'),
    path('add/', views.AddVehicle.as_view(), name='add'), 
    path('order/', views.AddOrder.as_view(), name='order'), 
    path('my_order/', views.my_order, name='my_order'), 
    path('orders/', views.Orders.as_view(), name='orders'), 
    path('order_details/<int:pk>/', views.order_details, name='order_details'), 
    path('update/<int:pk>/', views.VehicleUpdateView.as_view(), name='update_vehicle'), 
    path('orderstodo/', views.OrdersToDo.as_view(), name='orderstodo')
]
