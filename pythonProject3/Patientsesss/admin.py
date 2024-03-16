from django.contrib import admin


# Register your models here.


from .models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display=('id','name','date_of_birth','adress','phone','medical_history')


admin.site.register(Patient,PatientAdmin)
