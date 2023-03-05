from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order, Vehicle, User
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages


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
        post = request.POST
        # list of values from inputs in my_order.html [(tr, comment),..]
        ids = [(post.get('t'+str(i)), post.get('k'+str(i))) for i in range(1, int(post.get('input_counter'))) if post.get('t'+str(i)) != '']

        try:
            user = User.objects.get(pk=1)
            order = Order.objects.create(order_date=timezone.now() ,orderer=user)
            Vehicle.objects.bulk_create([Vehicle(tr=x[0], responsible_person=user, order=order, comments=x[1]) for x in ids])
            return redirect(reverse_lazy('files:list'))
        
        except:
            print("ups")  
            
    else:
        return render(request, 'files/my_order.html', {'range': range(1, 11)})
    

class Orders(ListView):
    model = Order
    fields = "__all__"


class OrdersToDo(ListView):
    model = Order
    template_name = 'files/orderstodo_list.html'
    context_object_name = 'todo'


def orders_to_do(request, status):
    orders = Order.objects.all()
    orders = [order for order in orders if any([vehicle.status for vehicle in order.vehicles.all() if vehicle.status == status])]
    abr = Vehicle.LOAN_STATUS
    return render(request, 'files/orders_to_do.html', context={'orders': orders, 'status': status, 'abr': abr})


class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = '__all__'
    success_url = reverse_lazy('files:orders')


def order_details(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        # List of ids from vehicles with checked checkboxes
        id_list = request.POST.getlist('boxes')
        for id in id_list:
            Vehicle.objects.filter(pk=int(id)).update(status='o')

        messages.success(request, ("Hurraa!!!"))
        return redirect('files:orders')

    else:
        return render(request, 'files/order_detail.html', context={'order': order})
    