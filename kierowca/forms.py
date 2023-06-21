# pylint: disable=no-member
from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from . import models


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

    # Check if driver is already taken or ordered and show error if is.
    awaits = models.Driver.objects.filter(pesel=pesel, status='a')
    on_loan = models.Driver.objects.filter(pesel=pesel, status='o')
    if awaits:
        raise ValidationError("Teczka jest już zamówiona")
    if on_loan:
        raise ValidationError("Teczka jest już pobrana")
    

class AddDriverForm(forms.ModelForm):
    """Initiate the form with assigned class, placeholder, and function to uppercase letters in TR field"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
        self.fields['first_name'].widget.attrs['oninput'] = 'handleInput(event)'
        self.fields['last_name'].widget.attrs['oninput'] = 'handleInput(event)'
        self.fields['zadanie_akt'].widget = forms.CheckboxInput()

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
    
    zadanie_akt = forms.BooleanField(initial=False,
                                     required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox',
                                                                       'checked': False,
                                                                       }))

    def clean_pesel(self):
        """ Check if driver is already taken or ordered and show error if is. """
        pesel = self.cleaned_data['pesel']
        if pesel:
            pesel_validation(pesel)
        return pesel


MyDriverOrderFormSet = formset_factory(MyDriverOrderForm, extra=10)


class ReturnDriverForm(forms.ModelForm):
    """ Form for ReturnDriverFormView to return drivers. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

        self.fields['first_name'].widget.attrs['oninput'] = 'handleInput(event)'
        self.fields['first_name'].required = False

        self.fields['last_name'].widget.attrs['oninput'] = 'handleInput(event)'
        self.fields['last_name'].required = False

        self.fields['birth_date'].required = False

        self.fields['pesel'].required = False

        self.fields['returner'].required = True


    class Meta:
        model = models.Driver
        fields = ['first_name', 'last_name', 'pesel', 'birth_date', 'returner', 'comments']

    # https://docs.djangoproject.com/en/4.1/ref/forms/validation/#cleaning-a-specific-field-attribute
    def clean_pesel(self):
        """ Check if driver is ordered and can be returned. """
        pesel = self.cleaned_data.get('pesel')
        if pesel:
            on_loan = models.Driver.objects.filter(pesel=pesel, status='o')
            if not on_loan:
                raise ValidationError("Nie ma pobranej takiej teczki")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return pesel
    

    def clean_birth_date(self):
        """ Check if driver is ordered and can be returned. """
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            on_loan = models.Driver.objects.filter(birth_date=birth_date,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    status='o')
            if not on_loan:
                raise ValidationError("Nie ma pobranej takiej teczki")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return birth_date
    

class TransferDriverForm(forms.ModelForm):
    pesel = forms.CharField(max_length=11, disabled=True, required=False)
    first_name = forms.CharField(max_length=100, disabled=True)
    last_name = forms.CharField(max_length=100, disabled=True)
    kk = forms.CharField(max_length=15, disabled=True, required=False)
    birth_date = forms.DateField(disabled=True)
    transfer_date = forms.DateField(disabled=True)

    def __init__(self, *args, **kwargs):
        # Exclude the current logged user from list of users
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['transfering_to'].queryset = models.User.objects.exclude(pk=self.user.pk)

    def clean_transfering_to(self):
        transfering_to = self.cleaned_data['transfering_to']
        if not transfering_to:
            raise ValidationError('Wybierz użytkownika')
        
    class Meta:
        model = models.Driver
        fields = ['first_name', 'last_name', 'pesel', 'kk', 'birth_date', 'transfer_date', 'transfering_to', 'comments']
