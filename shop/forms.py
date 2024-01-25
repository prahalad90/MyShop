from django import forms
from .models import Order

class orderForm(forms.ModelForm):
    class Meta:
        """Meta definition for MODELNAMEform."""
        model = Order
        fields = ('F_name','L_name')
        widgets = {
            'F_name' : forms.TextInput(attrs={"class": 'form-control col-6'}),
            'L_name' : forms.TextInput(attrs={"class": 'form-control col-6'}),
        }