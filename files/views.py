from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order, Vehicle, User
from django.views.generic import ListView, CreateView, DetailView, UpdateView, FormView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from .forms import ReturnForm
from django.http import FileResponse
import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

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


        for v in ids:
            vehicle = Vehicle.objects.filter(tr=v[0], status='o')
            if vehicle:
                messages.error(request, "Teczka wypożyczona")
                return render(request, 'files/my_order.html', {'range': range(1, 11)})
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
    

class ReturnFormView(SuccessMessageMixin, FormView):
    form_class = ReturnForm
    template_name = 'files/return.html'

    success_url = '/files/return/'
    success_message = "Teczka o numerze %(tr)s została zwrócona prawidłowo"

    def form_valid(self, form):
        print(form.cleaned_data)
        Vehicle.objects.filter(tr=form.cleaned_data['tr'], status='o').update(status='r')
        
        return super().form_valid(form)
    

def gen_pdf(request, pk):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    order = Order.objects.get(pk=pk)

    # Add some lines of text
    lines = [
        "This is line 1", 
        "This is line 2", 
        "This is line 3"
    ]
    
    for v in order.vehicles.all():
        lines.append(v.tr)
        lines.append(v.status)

    # loop
    for line in lines:
        textob.textLine(line)

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='test.pdf')


