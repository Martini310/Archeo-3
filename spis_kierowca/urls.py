from django.urls import path
from . import views

app_name = 'spis_kierowca'

urlpatterns = [
    path('list/', views.list_view, name='list'),
    path('search/', views.search_view, name="search"),
    path('add_list/', views.AddTransferListKierowcaView.as_view(), name='add_list'),
]