# pylint: disable=no-member
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib import messages
from django.db.models import Q
from .forms import TransferListKierowcaFormSet
from .models import TransferDriver, TransferListKierowca, User

# Create your views here.

def list_view(request):
    drivers, search = _search_drivers(request)
    users = User.objects.all()
    context = {'driver_list': drivers, 'search': search or "", 'users': users}
    return render(request, "spis_kierowca/list.html", context)


def search_view(request):
    drivers, search = _search_drivers(request)
    context = {'driver_list': drivers, 'search': search or ""}
    return render(request, "spis_kierowca/search_results.html", context)


def _search_drivers(request):
    search = request.GET.get("search")
    user = request.GET.get("user")
    drivers = TransferDriver.objects.all()
    if search:
        drivers = drivers.filter(Q(pesel__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(kk__icontains=search))
    if user:
        drivers = drivers.filter(transfer_list__responsible_person=user)
    return drivers.order_by('-transfer_list__id', 'id'), search or ""


class AddTransferListKierowcaView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, TemplateView):
    """ View to create a new DriverOrder. """
    template_name = 'spis_kierowca/add_list.html'
    success_message = "sukces"
    permission_required = 'spis_kierowca.add_transferdriver'


    def get(self, *args, **kwargs):
        formset = TransferListKierowcaFormSet()
        return self.render_to_response({'transfer_list_formset': formset})

    # Define method to handle POST request
    def post(self, request, *args, **kwargs):
        formset = TransferListKierowcaFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            # if form is not empty create new order with divers from form
            if any(len(row) > 0 for row in formset.cleaned_data):
                user = request.user
                transfer_list = TransferListKierowca.objects.create(responsible_person=user)
                print(transfer_list)
                print(formset.cleaned_data)
                TransferDriver.objects.bulk_create([TransferDriver(first_name=row['first_name'],
                                                                   last_name=row['last_name'],
                                                                   pesel=row['pesel'],
                                                                   birth_date=row['birth_date'],
                                                                   kk=row['kk'],
                                                                   transfer_list=transfer_list,
                                                                   comments=row['comments']) 
                                                                   for row in formset.cleaned_data if (row.get('last_name') is not None and row.get('first_name') is not None)])
        
                messages.success(request, 'Twój spis teczek przekazywanych do archiwum został zapisany poprawnie!')
                return redirect(reverse_lazy("spis_kierowca:list"))
        
        messages.warning(request, 'Wprowadź przynajmniej jedną teczkę lub popraw błędy')
        return self.render_to_response({'transfer_list_formset': formset})
    

class TransferDriverUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ A View to update particular Driver - url:'update/<int:pk>/' """
    model = TransferDriver
    fields = '__all__'
    success_url = reverse_lazy('spis_kierowca:list')
    permission_required = 'spis_kierowca.change_transferdriver'
    permission_denied_message = 'Nie masz uprawnień do tej zawartości'


class TransferListView(ListView):
    model = TransferListKierowca
    template_name = 'spis_kierowca/list_details.html'

    def get_queryset(self):
        return TransferDriver.objects.filter(transfer_list=self.kwargs['pk'])
