# pylint: disable=no-member
from django import forms
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from kierowca.models import Driver

def pesel_validation(pesel):
    """ 
    Check that the PESEL number length is correct and that the checksum is correct.
    Check if Driver with provided PESEL is already taken or ordered.
    """
    # Length
    if len(pesel) != 11:
        raise ValidationError(('Pesel musi mieć 11 znaków'))
    # Checksum
    control_sum = 0
    multipliers = {1: 1, 2: 3, 3: 7, 4: 9, 5: 1, 6: 3, 7: 7, 8: 9, 9: 1, 10: 3}
    for index, number in enumerate(str(pesel)[:-1], start=1):
        control_sum += int(number) * multipliers[index]
    if 10 - (control_sum % 10) != int(str(pesel)[-1]):
        raise ValidationError((f'PESEL: Błędna cyfra kontrolna {10 - (control_sum % 10)}'))
    if Driver.objects.filter(pesel=pesel, status__in='ao').exists():
        raise ValidationError("Ta teczka została zamówiona w module Kierowca")
    
def birth_date_validation(birth_date, first_name, last_name):
    driver = Driver.objects.filter(birth_date=birth_date, first_name=first_name, last_name=last_name, status__in='ao').exists()
    if driver:
        raise ValidationError("Ta teczka została zamówiona w module Kierowca")


class TransferListKierowcaForm(forms.Form):
    """ Form for AddTransferListView"""
    first_name = forms.CharField(label='',
                         max_length=100,
                         widget=forms.TextInput(attrs={'placeholder': 'Imię',
                                                       'class': 'form-control', 
                                                       'oninput':"handleInput(event)"}))
    
    last_name = forms.CharField(label='',
                         max_length=100,
                         widget=forms.TextInput(attrs={'placeholder': 'Nazwisko',
                                                       'class': 'form-control', 
                                                       'oninput':"handleInput(event)"}))
    
    pesel = forms.CharField(label='',
                         max_length=11,
                         required=False,
                         widget=forms.TextInput(attrs={'placeholder': 'PESEL',
                                                       'class': 'form-control', 
                                                       'oninput':"handleInput(event)",
                                                       'onfocusout':"peselToBirthDate(this)"}))
    
    kk = forms.CharField(label='',
                         max_length=10,
                         required=False,
                         widget=forms.TextInput(attrs={'placeholder': 'Numer k/k',
                                                       'class': 'form-control', 
                                                       'oninput':"handleInput(event)"}))
    
    birth_date = forms.DateField(label='',
                         widget=forms.DateInput(attrs={'placeholder': 'Data urodzenia',
                                                       'class': 'form-control'}))
    
    comments = forms.CharField(label='',
                               max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Uwagi',
                                                             'class': 'form-control'}))

    def clean_pesel(self):
        """ Check if driver is already taken or ordered and show error if is. """
        pesel = self.cleaned_data['pesel']
        if pesel:
            pesel_validation(pesel)
        return pesel

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if birth_date:
            birth_date_validation(birth_date, first_name, last_name)
        return birth_date


TransferListKierowcaFormSet = formset_factory(TransferListKierowcaForm, extra=1)
