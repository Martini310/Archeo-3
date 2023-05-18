from django.shortcuts import render, redirect
from .models import DriverOrder, Driver, User
from .forms import AddDriverForm, MyDriverOrderFormSet
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy

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


class AddDriver(LoginRequiredMixin, CreateView):
    """ A View to create a new instance of vehicle. """
    model = Driver
    form_class = AddDriverForm

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
                print(formset.cleaned_data)
                
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
        
        messages.warning(request, 'Wprowadź przynajmniej jedno zamówienie')
        return self.render_to_response({'my_driverorder_formset': formset})
