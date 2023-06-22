# pylint: disable=no-member
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, FormView, TemplateView, View
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ReturnForm, MyOrderFormSet, TransferForm, AddVehicleForm
from .models import Order, Vehicle, User
from kierowca.models import Driver, DriverOrder

# Create your views here.

def notification_context(request):
    """Context dictionary for all templates in app"""
    # look up the notifications for the current user
    transfers = Vehicle.objects.filter(transfering_to=request.user.id)
    orders = len([order for order in Order.objects.all() if any(
        [vehicle.status for vehicle in order.vehicles.all() if vehicle.status == 'a'])]) or 0
    
    driver_transfers = Driver.objects.filter(transfering_to=request.user.id)
    driver_orders = len([order for order in DriverOrder.objects.all() if any(
        [driver.status for driver in order.drivers.all() if driver.status == 'a'])]) or 0
    # The return value must be a dict, and any values in that dict
    # are added to the template context for all templates.
    # You might want to use more unique names here, to avoid having these
    # variables clash with variables added by a view.  For example, `count` could easily
    # be used elsewhere.
    return {'notifications': {'transfers': transfers, 
                              'count_orders_to_do': orders, 
                              'driver_transfers': driver_transfers, 
                              'count_driver_orders_to_do': driver_orders}}


class HomeView(TemplateView):
    template_name = "home.html"
    

def list_view(request):
    vehicles, search = _search_vehicles(request)
    users = User.objects.all()
    context = {'vehicle_list': vehicles, 'search': search or "", 'users': users}
    return render(request, "pojazd/list.html", context)


def search_view(request):
    vehicles, search = _search_vehicles(request)
    context = {'vehicle_list': vehicles, 'search': search or ""}
    return render(request, "pojazd/search_results.html", context)


def _search_vehicles(request):
    search = request.GET.get("search")
    status = request.GET.get("status")
    user = request.GET.get("user")
    vehicles = Vehicle.objects.all()

    if search:
        vehicles = vehicles.filter(tr__icontains=search)
    if status:
        vehicles = vehicles.filter(status=status)
    if user:
        vehicles = vehicles.filter(responsible_person=user)
    return vehicles, search or ""


class AddVehicle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ A View to create a new instance of vehicle. """
    model = Vehicle
    form_class = AddVehicleForm

    success_url = reverse_lazy('pojazd:list')
    permission_required = 'pojazd.add_vehicle'
    

class MyOrderView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    """ View to create a new Order. """
    template_name = 'pojazd/my_order.html'
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
                user = request.user
                # order = Order.objects.create(order_date=timezone.now(), orderer=user)
                order = Order.objects.create(orderer=user)

                Vehicle.objects.bulk_create([Vehicle(tr=row['tr'],
                                                     responsible_person=user,
                                                     order=order,
                                                     comments=row['comments']) 
                                                     for row in formset.cleaned_data if row.get('tr') is not None])
                messages.success(request, 'Twoje zamówienie zostało wysłane poprawnie!')
                return redirect(reverse_lazy("pojazd:list"))
        return self.render_to_response({'my_order_formset': formset})


class OrdersToDoView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ A View with listed all orders divides into status categories. """
    model = Order
    template_name = 'orders_to_do.html'
    permission_required = 'pojazd.view_order'

    def get(self, request, status):
        orders = Order.objects.all()
        orders = [(order, order.vehicles.filter(status='a').count) for order in orders if any(
                [vehicle.status for vehicle in order.vehicles.all() if vehicle.status == status])]
        abr = Vehicle.LOAN_STATUS
        return render(request, 'pojazd/orders_to_do.html', context={'orders': orders, 'status': status, 'abr': abr})


class VehicleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ A View to update particular Vehicle - url:'update/<int:pk>/' """
    model = Vehicle
    fields = '__all__'
    success_url = reverse_lazy('pojazd:list')
    permission_required = 'pojazd.change_vehicle'
    permission_denied_message = 'Nie masz uprawnień do tej zawartości'


class OrderDetails(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, View):
    """
    A view to update a particular Order, save or reject Vehicles in the Order.
    URL: 'order_details/<int:pk>/'
    """
    model = Vehicle
    template_name = 'pojazd/order_detail.html'

    permission_required = 'pojazd.change_vehicle'
    success_message = "Zmiany w zamówieniu zostały zapisane prawidłowo."
    permission_denied_message = "Nie masz dostępu do tej zawartości."
    
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        statuses = dict(Vehicle.LOAN_STATUS)
        return render(request, 'pojazd/order_detail.html', context={'order': order, 'statuses': statuses})
    
    def post(self, request, pk):
        # List of ids from vehicles with checked checkboxes
        order = Order.objects.get(pk=pk)
        statuses = dict(Vehicle.LOAN_STATUS)
        print(request.POST)
        id_list = request.POST.getlist('boxes')
        if id_list:
            if 'save' in request.POST:
                for input_id in id_list:
                    if input_id in request.POST.getlist('bezzwrotnie'):
                        Vehicle.objects.filter(pk=int(input_id)).update(status='e', transfer_date=timezone.now())
                    else:
                        Vehicle.objects.filter(pk=int(input_id)).update(status='o', transfer_date=timezone.now())
            elif 'reject' in request.POST:
                for input_id in id_list:
                    Vehicle.objects.filter(pk=int(input_id)).update(status='e')

            return redirect('pojazd:list')
        else:
            messages.error(request,'Proszę zaznaczyć przynajmniej 1 pozycję')
            return render(request, 'pojazd/order_detail.html', context={'order': order, 'statuses': statuses})


class ReturnFormView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    """ A View to return a vehicle. """
    form_class = ReturnForm
    template_name = 'pojazd/return.html'
    permission_required = 'pojazd.return_vehicle'

    success_url = '/pojazd/return/'
    success_message = "Teczka o numerze %(tr)s została zwrócona prawidłowo"

    time = timezone.now()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs() 
        # Retrieve the value of 'returner' from the session
        returner_pk = self.request.session.get('returner')
        if returner_pk:
            returner = User.objects.get(pk=returner_pk)
            kwargs['initial'] = {'returner': returner}
        
        return kwargs

    def form_valid(self, form):
        Vehicle.objects.filter(
            tr=form.cleaned_data['tr'], status='o').update(status='r',
                                                           returner=form.cleaned_data['returner'],
                                                           comments=form.cleaned_data['comments'],
                                                           return_date=self.time)
        # Store the value of 'returner' in the session
        self.request.session['returner'] = form.cleaned_data['returner'].pk

        return super().form_valid(form)


class ListUserVehiclesView(LoginRequiredMixin, ListView):
    """ List all vehicles that currently logged user is responsible for. """
    model = Vehicle
    context_object_name = 'orders' # 'user_vehicles'
    template_name = 'pojazd/user_vehicles.html'

    def get(self, request, status='aore'):
        orders = [order for order in Order.objects.all() if any(vehicle.responsible_person.username == request.user.get_username() and vehicle.status in status for vehicle in order.vehicles.all())]
        transfers = Vehicle.objects.filter(transfering_to=self.request.user)
        context = {'orders': (orders, Vehicle.LOAN_STATUS, status, transfers)}
        return render(request, 'pojazd/user_vehicles.html', context)


class TransferVehicleView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Update View to change the person responsible for vehicle file."""
    model = Vehicle
    form_class = TransferForm
    success_url = reverse_lazy('pojazd:user_list')
    success_message = 'Prawidłowo przekazano teczkę innemu użytkownikowi.'
    permission_required = 'pojazd.transfer_vehicle'
    # permission_denied_message = 'Brak dostępu'

    def dispatch(self, request, *args, **kwargs):
        handler = super(TransferVehicleView, self).dispatch(request, *args, **kwargs)
        # Only allow editing if current user is owner
        if self.object.responsible_person != request.user:
            return HttpResponseForbidden("Can't touch this.")
        return handler
    
    # Sending user object to the form, to verify which fields to display/remove
    def get_form_kwargs(self):
        kwargs = super(TransferVehicleView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    

class AcceptTransferVehicleView(LoginRequiredMixin, ListView):
    template_name = 'pojazd/accept_vehicles.html'
    context_object_name = 'transfers'

    def get_queryset(self):
        queryset = Vehicle.objects.filter(transfering_to=self.request.user)
        return queryset

    def post(self, request):
        if 'accept' in request.POST:
            pk = request.POST['accept']
            Vehicle.objects.filter(id=pk).update(responsible_person=request.user, transfering_to=None)
        elif 'reject' in request.POST:
            pk = request.POST['reject']
            Vehicle.objects.filter(id=pk).update(transfering_to=None)

        return redirect(reverse_lazy('pojazd:user_list', kwargs={'status': "aore"}))
