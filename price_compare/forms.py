from django import forms
from .models import Tracked_Products

class Tracked_Products_Form(forms.ModelForm):
    class Meta:
        model = Tracked_Products
