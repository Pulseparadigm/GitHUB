from django.db import models


class Products(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.TextField(max_length=255)
    price = models.FloatField(max_length=255)
    stock = models.IntegerField()
    image_url = models.TextField(max_length=2083)

