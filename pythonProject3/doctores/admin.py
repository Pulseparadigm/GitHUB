from django.contrib import admin

# Register your models here.
from .models import Doctor
from .models import Appointments

class DoctorAdmin(admin.ModelAdmin):
    list_display=('docid','firstname','lastname','img')

admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Appointments)





