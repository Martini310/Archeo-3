from django.urls import path
from . import views

app_name = 'files'

urlpatterns = [
    # path('list/', views.ListAllVechicles.as_view(), name='list'),
    path('list/', views.list_view, name='list'),
    path('add/', views.AddVehicle.as_view(), name='add'),
    path('my_order/', views.MyOrderView.as_view(), name='my_order'),
    # path('order_details/<int:pk>/', views.order_details, name='order_details'),
    path('order_details/<int:pk>/', views.OrderDetails.as_view(), name='order_details'),
    path('update/<int:pk>/', views.VehicleUpdateView.as_view(), name='update_vehicle'),
    path('orders_to_do/<str:status>/', views.OrdersToDoView.as_view(), name='orders_to_do'),
    path('return/', views.ReturnFormView.as_view(), name='return'),
    path('user_list/', views.ListUserVehiclesView.as_view(), name='user_list'),
    path('user_list/<str:status>/', views.ListUserVehiclesView.as_view(), name='user_list'),
    path('transfer/<int:pk>/', views.TransferVehicleView.as_view(), name='transfer'),
    path('search/', views.search_view, name="search"),
    path('accept_vehicles/', views.AcceptTransferVehicleView.as_view(), name='accept_vehicles'),
    path('accept_vehicles/<int:pk>/', views.update_transfer_status_view, name='accept')
]
