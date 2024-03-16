from django.db import models
from Nurses.models import SampleCollector
from django.forms import ModelForm

# Create your models here.
class SampleCollectorForm(ModelForm):
    class Meta:
        model=SampleCollector
        fields="__all__"

class SampleCollectorlogin(ModelForm):
    class Meta :
        model=SampleCollector
        fields=['email','password']

