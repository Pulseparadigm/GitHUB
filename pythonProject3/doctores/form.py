from django import forms
from .models import *


class DoctorForm(forms.ModelForm):


    class Meta:
        model=Doctor
        fields=['firstname','lastname','email','password','img',]
