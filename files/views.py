from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order, Vehicle, User
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy


# Create your views here.
def list_cars(request):
    context = {'vehicle_list': Vehicle.objects.all()}
    return render(request, 'files/list.html', context=context)


class ListAllVechicles(ListView):
    model = Vehicle
    template_name = 'files/list.html'


class AddVehicle(CreateView):
    model = Vehicle
    fields = "__all__"
    success_url = reverse_lazy('files:list')


class AddOrder(CreateView):
    model = Order
    fields = '__all__'
    success_url = reverse_lazy('files:list')


def my_order(request):
    if request.method == 'POST':
        ids = []
        for i in range(int(request.POST.get('input_counter'))):
            ids.append(request.POST.get('t'+str(i)))
        print(request.POST)
        try:
            print(ids)
            admin = User.objects.get(pk=1)
            # Vehicle.objects.create(tr=ids[0], responsible_person=admin)
            Vehicle.objects.bulk_create([Vehicle(tr=x, responsible_person=admin) for x in ids])
            return redirect(reverse_lazy('files:list'))
        except:
            print("ups")  
    else:
        return render(request, 'files/my_order.html')