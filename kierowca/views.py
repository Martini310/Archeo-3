from django.shortcuts import render
from .models import DriverOrder, Driver, User
from .forms import AddDriverForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
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
    # permission_required = 'kierowca.add_driver'
