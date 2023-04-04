from django.urls import path
from . import views

app_name = 'files'

urlpatterns = [
    path('list/', views.ListAllVechicles.as_view(), name='list'),
    path('add/', views.AddVehicle.as_view(), name='add'),
    path('my_order/', views.MyOrderView.as_view(), name='my_order'),
    path('order_details/<int:pk>/', views.order_details, name='order_details'),
    path('update/<int:pk>/', views.VehicleUpdateView.as_view(), name='update_vehicle'),
    path('orders_to_do/<str:status>/', views.orders_to_do, name='orders_to_do'),
    path('return/', views.ReturnFormView.as_view(), name='return'),
    path('user_list/', views.ListUserVehiclesView.as_view(), name='user_list'),
    path('transfer/<int:pk>/', views.TransferVehicleView.as_view(), name='transfer'),
]
