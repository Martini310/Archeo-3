from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.forms import formset_factory


class ReturnForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle
        fields = ['tr', 'returner', 'comments']

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
    tr = forms.CharField(label='', max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Numer rejestracyjny', 'class': 'form-control'}))
    comments = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Uwagi', 'class': 'form-control'}))

    # users = [(a, b) for a, b in enumerate(models.User.objects.all(), start=1)]
    # orderer = forms.ChoiceField(label='Zamawiający', widget=forms.Select, choices=users)

MyOrderFormSet = formset_factory(MyOrderForm, extra=3)