from django.contrib import admin

# Register your models here.
from .models import Products

class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','stock')


admin.site.register(Products,ProductAdmin)
