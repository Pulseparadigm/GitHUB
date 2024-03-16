from django.db import models
from Patientsesss.models import Patient



# Create your models here.
class Doctor(models.Model):
    docid=models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=50,null=False,blank=False)
    lastname  = models.CharField( max_length = 10,null=False,blank=False)
    email     =models. EmailField(unique=True,null=False,blank=False)
    password  =models.CharField(max_length=255,null=False,blank=False,default='123')
    img     = models.ImageField(default="C:\\Users\Laptop Castle\PycharmProjects\pythonProject3\static\doctor.png",upload_to='images/') # for creating file input

    class Meta:
        db_table="Doctor"


class Test(models.Model):
    test_type=models.CharField(max_length=255)
    test_name=models.CharField(max_length=255)
    order_status=models.CharField(max_length=255,null=False,blank=True,default='Unordered')
    cost=models.FloatField()

    class Meta:
        db_table="Test"



class Appointments(models.Model):
    Date_And_Time=models.DateTimeField();
    Patient_ID=models.ForeignKey(Patient,on_delete=models.CASCADE)
    Doctor_ID=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    visit=models.TextField("Purpose_of_Visit",blank=True,null=True)


    class Meta:
        db_table="Appointment"
        unique_together = (("Patient_ID", "Doctor_ID"),)
