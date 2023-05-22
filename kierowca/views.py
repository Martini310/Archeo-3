# pylint: disable=no-member
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.views.generic import CreateView, TemplateView, ListView, View, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import AddDriverForm, MyDriverOrderFormSet, ReturnDriverForm
from .models import DriverOrder, Driver, User

# Create your views here.
def list_view(request):
    drivers, search = _search_drivers(request)
    users = User.objects.all()
    context = {'driver_list': drivers, 'search': search or "", 'users': users}
    return render(request, "kierowca/list.html", context)


def search_view(request):
    drivers, search = _search_drivers(request)
    context = {'driver_list': drivers, 'search': search or ""}
    return render(request, "kierowca/search_results.html", context)


def _search_drivers(request):
    search = request.GET.get("search")
    status = request.GET.get("status")
    user = request.GET.get("user")
    drivers = Driver.objects.all()

    if search:
        drivers = drivers.filter(Q(pesel__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
    if status:
        drivers = drivers.filter(status=status)
    if user:
        drivers = drivers.filter(responsible_person=user)
    return drivers, search or ""


class AddDriver(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """ A View to create a new instance of vehicle. """
    model = Driver
    form_class = AddDriverForm

    success_message = "zapisano!"
    success_url = reverse_lazy('kierowca:list')
    # TODO permission_required = 'kierowca.add_driver'


class MyDriverOrderView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    """ View to create a new DriverOrder. """
    template_name = 'kierowca/my_driverorder.html'
    success_message = "sukces"

    def get(self, *args, **kwargs):
        formset = MyDriverOrderFormSet()
        return self.render_to_response({'my_driverorder_formset': formset})

    # Define method to handle POST request
    def post(self, request, *args, **kwargs):
        formset = MyDriverOrderFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            # if form is not empty create new order with divers from form
            if any(len(row) > 0 for row in formset.cleaned_data):
                user = request.user
                order = DriverOrder.objects.create(orderer=user)
                # print(formset.cleaned_data)
                
                Driver.objects.bulk_create([Driver(first_name=row.get('first_name'),
                                                    last_name=row['last_name'],
                                                    pesel=row['pesel'],
                                                    birth_date=row['birth_date'],
                                                    responsible_person=user,
                                                    order=order,
                                                    comments=row['comments']) 
                                                     for row in formset.cleaned_data if row.get('last_name') is not None])
                messages.success(request, 'Twoje zamówienie zostało wysłane poprawnie!')
                return redirect(reverse_lazy("kierowca:list"))
        
        messages.warning(request, 'Wprowadź przynajmniej jedno zamówienie lub popraw błędy')
        return self.render_to_response({'my_driverorder_formset': formset})


class DriverOrdersToDoView(LoginRequiredMixin, ListView):
    """ A View with listed all Driver orders divides into status categories. """
    model = DriverOrder
    template_name = 'driverorders_to_do.html'
    # permission_required = 'kierowca.view_order'

    def get(self, request, status):
        orders = DriverOrder.objects.all()
        orders = [(order, order.drivers.filter(status='a').count) for order in orders if any(
                [driver.status for driver in order.drivers.all() if driver.status == status])]
        abr = Driver.LOAN_STATUS
        return render(request, 'kierowca/driverorders_to_do.html', context={'orders': orders, 'status': status, 'abr': abr})


class OrderDetails(LoginRequiredMixin, SuccessMessageMixin, View):
    """
    A view to update a particular Order, save or reject Driver in the Order.
    URL: 'order_details/<int:pk>/'
    """
    model = Driver
    template_name = 'kierowca/order_details.html'

    # permission_required = 'kierowca.change_driver'
    success_message = "Zmiany w zamówieniu zostały zapisane prawidłowo."
    # permission_denied_message = "Nie masz dostępu do tej zawartości."
    
    def get(self, request, pk):
        order = DriverOrder.objects.get(pk=pk)
        statuses = dict(Driver.LOAN_STATUS)
        return render(request, 'kierowca/order_details.html', context={'order': order, 'statuses': statuses})
    
    def post(self, request, pk):
        # List of ids from Drivers with checked checkboxes
        order = DriverOrder.objects.get(pk=pk)
        statuses = dict(Driver.LOAN_STATUS)
        id_list = request.POST.getlist('boxes')
        if id_list:
            if 'save' in request.POST:
                for input_id in id_list:
                    Driver.objects.filter(pk=int(input_id)).update(status='o', transfer_date=timezone.now())
            elif 'reject' in request.POST:
                for input_id in id_list:
                    Driver.objects.filter(pk=int(input_id)).update(status='e')

            return redirect('kierowca:list')
        else:
            messages.error(request,'Proszę zaznaczyć przynajmniej 1 pozycję')
            return render(request, 'kierowca/order_details.html', context={'order': order, 'statuses': statuses})


class ReturnDriverFormView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """ A View to return a driver. """
    form_class = ReturnDriverForm
    template_name = 'kierowca/return.html'
    # permission_required = 'kierowca.return_driver'

    success_url = '/kierowca/return/'
    success_message = "Teczka o numerze %(pesel)s została zwrócona prawidłowo"

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
        pesel=form.cleaned_data['pesel']
        if pesel:
            Driver.objects.filter(pesel=pesel, status='o').update(status='r',
                                                            returner=form.cleaned_data['returner'],
                                                            comments=form.cleaned_data['comments'],
                                                            return_date=self.time)
        else:
            Driver.objects.filter(first_name=form.cleaned_data['first_name'],
                                  last_name=form.cleaned_data['last_name'],
                                  birth_date=form.cleaned_data['birth_date'],
                                  status='o').update(status='r',
                                                    returner=form.cleaned_data['returner'],
                                                    comments=form.cleaned_data['comments'],
                                                    return_date=self.time)
        # Store the value of 'returner' in the session
        self.request.session['returner'] = form.cleaned_data['returner'].pk

        return super().form_valid(form)
