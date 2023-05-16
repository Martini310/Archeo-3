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
