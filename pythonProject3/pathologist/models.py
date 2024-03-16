from django.db import models
from django.forms import ModelForm

# Create your models here.

class pathologist(models.Model):
    name=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    field=models.CharField(max_length=255)


class pathologistForm(ModelForm):
    class Meta:
        model=pathologist
        fields="__all__"

class pathologistlogin(ModelForm):
    class Meta :
        model=pathologist
        fields=['email','password']
