

from . import views
from django.urls import path

urlpatterns=[
    path('',views.login),
    path('Registration_Done',views.registration),
    path('registration_form',views.patient_form),
    path('Patient_Home_ShowDoc',views.patient_home_showDoc),
    path('filter',views.filter),
    path('Patient_Home',views.patient_Home),
    path('Login_verify',views.login_verify),
    path('Update',views.Upadte_PatientForm),
    path('Updated',views.Update_Patient_info),
    path('Appointments/<int:docID>',views.booking_appointment),
    path('view_appointment/<int:id>',views.view_appointment),
    path('view_test',views.view_test),
    path('order_test/<int:id>',views.order_test),
]
