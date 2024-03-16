from django.db import models
from Patientsesss.models import Patient
from doctores.models import Test
from django.forms import ModelForm


# Create your models here.
class  Staff(models.Model):
    Name=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    email=models.EmailField(unique=True,null=False,blank=False)
    Department=models.CharField(max_length=255)
    ContactInfo=models.IntegerField()
    Salary=models.FloatField()
    Schedule=models.DateField()

    class Meta:
        abstract=True

class Nurse(Staff):
    on_vacation=models.CharField(max_length=255,default='NO')
    test_ordered=models.IntegerField(default=0)
    tests_pending=models.IntegerField(default=0)

    class Meta:
        db_table="Nurse"



class SampleCollector(models.Model):
    CollectorName=models.CharField(max_length=255)
    email=models.EmailField()
    password=models.CharField(max_length=255)

    class Meta:
        db_table="Sample_Collector"
        #unique_together = (( "Nurse",'Test'),)

class NurseForm(ModelForm):


    class Meta:
        model=Nurse
        fields=["Name","password","email","Department","ContactInfo","Salary"]

class nurse_login_form(ModelForm):

    class Meta:
        model=Nurse
        fields=["email","password"]

