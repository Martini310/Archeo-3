from django.urls import path
from . import views

app_name = 'kierowca'

urlpatterns = [
    path('list/', views.list_view, name='list'),
    path('search/', views.search_view, name="search"),
    path('add/', views.AddDriver.as_view(), name='add'),
    path('my_driverorder', views.MyDriverOrderView.as_view(), name='my_driverorder'),
    path('orders_to_do/<str:status>/', views.DriverOrdersToDoView.as_view(), name='driverorders_to_do'),
    path('order_details/<int:pk>/', views.OrderDetails.as_view(), name='order_details'),
]