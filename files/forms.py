# pylint: disable=no-member
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from . import models


class ReturnForm(forms.ModelForm):
    """ Form for ReturnFormView to return vechicles. """
    class Meta:
        model = models.Vehicle
        fields = ['tr', 'returner', 'comments']

    # https://docs.djangoproject.com/en/4.1/ref/forms/validation/#cleaning-a-specific-field-attribute
    def clean_tr(self):
        """ Check if vechicle is ordered and can be returned. """
        data = self.cleaned_data['tr']
        on_loan = models.Vehicle.objects.filter(tr=data, status='o')
        if not on_loan:
            raise ValidationError("Nie ma pobranej takiej teczki")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data


class MyOrderForm(forms.Form):
    """ Form for MyOrderView"""
    tr = forms.CharField(label='', 
                         max_length=10, 
                         widget=forms.TextInput(attrs={'placeholder': 'Numer rejestracyjny', 
                                                       'class': 'form-control', 
                                                       'oninput':"handleInput(event)"}))
    comments = forms.CharField(label='', 
                               max_length=100, 
                               required=False, 
                               widget=forms.TextInput(attrs={'placeholder': 'Uwagi', 
                                                             'class': 'form-control'}))

    def clean_tr(self):
        """ Check if tr is already taken or ordered and show error if is. """
        tr = self.cleaned_data['tr']
        awaits = models.Vehicle.objects.filter(tr=tr, status__in='a')
        on_loan = models.Vehicle.objects.filter(tr=tr, status__in='o')
        if awaits:
            raise ValidationError("Teczka jest już zamówiona")
        if on_loan:
            raise ValidationError("Teczka jest już pobrana")
        return tr
    # users = [(a, b) for a, b in enumerate(models.User.objects.all(), start=1)]
    # orderer = forms.ChoiceField(label='Zamawiający', widget=forms.Select, choices=users)


MyOrderFormSet = formset_factory(MyOrderForm, extra=10)
