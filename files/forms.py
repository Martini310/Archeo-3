from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.forms import formset_factory


class ReturnForm(forms.ModelForm):

    
    class Meta:
        model = models.Vehicle
        fields = ['tr', 'returner', 'comments']

    def __init__(self, *args, **kwargs):
        # Pobierz początkowe wartości z argumentów funkcji
        initial = kwargs.get('initial', {})
        # Pobierz wartości przesłane w poprzednim formularzu
        value1 = initial.get('tr')
        value2 = initial.get('returner')
        # Ustaw początkową wartość dla pola field3 na podstawie przesłanej wartości
        initial['comments'] = 'value1' + " " + 'value2'
        # Wywołaj metodę __init__() rodzica
        super().__init__(*args, **kwargs)
        # Ustaw początkowe wartości dla pól formularza
        self.initial['tr'] = 'wartosc'
        self.initial['returner'] = models.User.objects.get(pk=1)
        self.initial.update(initial)

    # INITIAL VALUES
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.initial['tr'] = 'value1'
    #     self.initial['returner'] = models.User.objects.get(pk=2)
        
    # https://docs.djangoproject.com/en/4.1/ref/forms/validation/#cleaning-a-specific-field-attribute
    def clean_tr(self):
        data = self.cleaned_data['tr']
        db = models.Vehicle.objects.filter(tr=data, status='o')
        if not db:
            raise ValidationError("Nie ma pobranej takiej teczki")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
    
    

class MyOrderForm(forms.Form):
    tr = forms.CharField(label='', max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Numer rejestracyjny', 'class': 'form-control', 'oninput':"handleInput(event)"}))
    comments = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Uwagi', 'class': 'form-control'}))


    def clean_tr(self):
        tr = self.cleaned_data['tr']
        db = models.Vehicle.objects.filter(tr=tr, status__in='ao')
        if db:
            raise ValidationError("Teczka jest już pobrana")
        return tr
    

    # users = [(a, b) for a, b in enumerate(models.User.objects.all(), start=1)]
    # orderer = forms.ChoiceField(label='Zamawiający', widget=forms.Select, choices=users)

MyOrderFormSet = formset_factory(MyOrderForm, extra=10)


