# pylint: disable=no-member
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from . import models


class AddDriverForm(forms.ModelForm):
    """Initiate the form with assigned class, placeholder, and function to uppercase letters in TR field"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
        # self.fields['tr'].widget.attrs['oninput'] = 'handleInput(event)'

    class Meta:
        model = models.Driver
        fields = '__all__'


class MyDriverOrderForm(forms.Form):
    """ Form for MyDriverOrderView"""
    first_name = forms.CharField(label='',
                         max_length=50,
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
        # """ Check if driver is already taken or ordered and show error if is. """
        pesel = self.cleaned_data['pesel']
        # awaits = models.Driver.objects.filter(pesel=pesel, status__in='a')
        # on_loan = models.Driver.objects.filter(pesel=pesel, status__in='o')
        # if awaits:
        #     raise ValidationError("Teczka jest już zamówiona")
        # if on_loan:
        #     raise ValidationError("Teczka jest już pobrana")

        models.pesel_validation(pesel)
        return pesel


MyDriverOrderFormSet = formset_factory(MyDriverOrderForm, extra=10)