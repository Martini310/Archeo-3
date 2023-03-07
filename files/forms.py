from django import forms
from . import models

class ReturnForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = []

    tr = forms.CharField()
    returner = forms.ModelChoiceField(queryset=models.User.objects.all())
