from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

def validate_not_returned(value):
    vehicle = models.Vehicle.objects.filter(tr=value, status='o')
    if not vehicle:
        print(vehicle)
        raise ValidationError(
            _('%(value)s - nie ma takiej teczki'),
            params={'value': value},
        )
    

class ReturnForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle
        fields = ['tr', 'returner', 'comments']

        
    # tr = forms.CharField(validators=[validate_not_returned])
    # returner = forms.ModelChoiceField(queryset=models.User.objects.all())
    
