# pylint: disable=no-member
# import io
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.http import FileResponse
# from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ReturnForm, MyOrderFormSet, TransferForm
from .models import Order, Vehicle, User
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter

# Create your views here.


class ListAllVechicles(ListView):
    """ A View with listed all vehicles in DB. """
    model = Vehicle
    template_name = 'files/list.html'
    context_object_name = 'vehicle_list'


class AddVehicle(LoginRequiredMixin, CreateView):
    """ A View to create a new instance of vehicle. """
    model = Vehicle
    fields = "__all__"
    success_url = reverse_lazy('files:list')


class MyOrderView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    """ View to create a new Order. """
    template_name = 'files/my_order.html'
    success_message = "sukces"

    def get(self, *args, **kwargs):
        formset = MyOrderFormSet()
        return self.render_to_response({'my_order_formset': formset})

    # Define method to handle POST request
    def post(self, request, *args, **kwargs):
        formset = MyOrderFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            # if form is not empty create new order with vehicles from form
            if any(len(row) > 0 for row in formset.cleaned_data):
                user = User.objects.get(pk=1)
                order = Order.objects.create(order_date=timezone.now(), orderer=user)
                Vehicle.objects.bulk_create([Vehicle(tr=row['tr'], 
                                                     transfer_date=timezone.now(), 
                                                     responsible_person=user, 
                                                     order=order,
                                                     comments=row['comments']) 
                                                     for row in formset.cleaned_data if row.get('tr') is not None])
                messages.success(request, 'Twoje zamówienie zostało wysłane poprawnie!')
                return redirect(reverse_lazy("files:list"))
        return self.render_to_response({'my_order_formset': formset})


@login_required
def orders_to_do(request, status):
    """ A View with listed all orders divides into status categories. """
    orders = Order.objects.all()
    orders = [order for order in orders if any(
        [vehicle.status for vehicle in order.vehicles.all() if vehicle.status == status])]
    abr = Vehicle.LOAN_STATUS
    return render(request, 'files/orders_to_do.html', context={'orders': orders, 'status': status, 'abr': abr})


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    """ A View to update particular Vehicle - url:'update/<int:pk>/' """
    model = Vehicle
    fields = '__all__'
    success_url = reverse_lazy('files:list')


@login_required
def order_details(request, pk):
    """ A View to update particular Order, Save or Reject Vehicles in Order - url:'order_details/<int:pk>/' """
    order = Order.objects.get(pk=pk)
    if request.method == "POST":
        # List of ids from vehicles with checked checkboxes
        id_list = request.POST.getlist('boxes')
        if 'save' in request.POST:
            for input_id in id_list:
                Vehicle.objects.filter(pk=int(input_id)).update(status='o')
        elif 'reject' in request.POST:
            for input_id in id_list:
                Vehicle.objects.filter(pk=int(input_id)).update(status='e')

        messages.success(request, ("Hurraa!!!"))
        return redirect('files:list')

    else:
        return render(request, 'files/order_detail.html', context={'order': order})


class ReturnFormView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """ A View to return a vehicle. """
    form_class = ReturnForm
    template_name = 'files/return.html'

    success_url = '/files/return/'
    success_message = "Teczka o numerze %(tr)s została zwrócona prawidłowo"

    def form_valid(self, form):
        print(form.cleaned_data)
        Vehicle.objects.filter(
            tr=form.cleaned_data['tr'], status='o').update(status='r')

        return super().form_valid(form)


class ListUserVehiclesView(LoginRequiredMixin, ListView):
    """ List all vehicles that currently logged user is responsible for. """
    model = Vehicle
    context_object_name = 'orders' # 'user_vehicles'
    template_name = 'files/user_vehicles.html'
    
    def get_queryset(self):
        # Get list of orders where at least in one vehicle user is a responsible person
        orders = [order for order in Order.objects.all() if any(vehicle.responsible_person.username == self.request.user.get_username() for vehicle in order.vehicles.all())]
        return orders


class TransferVehicleView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Update View to change the person responsible for vehicle file."""
    model = Vehicle
    form_class = TransferForm
    success_url = reverse_lazy('files:user_list')
    success_message = 'Prawidłowo przekazano teczkę innemu użytkownikowi.'
    permission_required = 'files.change_vehicle'


# def gen_pdf(request, pk):
#     # Create Bytestream buffer
#     buf = io.BytesIO()
#     # Create a canvas
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#     # Create a text object
#     textob = c.beginText()
#     textob.setTextOrigin(inch, inch)
#     textob.setFont("Helvetica", 14)

#     order = Order.objects.get(pk=pk)

#     # Add some lines of text
#     lines = [
#         "This is line 1",
#         "This is line 2",
#         "This is line 3"
#     ]

#     for v in order.vehicles.all():
#         lines.append(v.tr)
#         lines.append(v.status)

#     # loop
#     for line in lines:
#         textob.textLine(line)

#     # Finish Up
#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buf.seek(0)

#     return FileResponse(buf, as_attachment=True, filename='test.pdf')
