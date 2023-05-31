from django.urls import path
from . import views

app_name = 'spis_kierowca'

urlpatterns = [
    path('list/', views.list_view, name='list'),
    path('search/', views.search_view, name="search"),
    path('add_list/', views.AddTransferListKierowcaView.as_view(), name='add_list'),
    path('update/<int:pk>/', views.TransferDriverUpdateView.as_view(), name='update_transfer'),
    path('list_details/<int:pk>/', views.TransferListView.as_view(), name='list_details'),
]