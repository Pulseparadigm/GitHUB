from django.db import models

from django.core.validators import MaxValueValidator

# Create your models here.
class Patient(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=255)

    date_of_birth=models.DateField(max_length=255,default='2024-02-24',null=False,blank=False)
    adress=models.CharField(max_length=255)
    phone=models.IntegerField()
    medical_history=models.CharField(max_length=200)
    password=models.CharField(max_length=200,blank=False,null=False)


    class Meta:
        db_table='Patient'


