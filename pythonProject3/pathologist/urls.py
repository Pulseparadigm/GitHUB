
from . import views
from django.urls import path
urlpatterns=[
    path('',views.loginpage),
    path('registration',views.registration),
    path('sample',views.sample_list),
    path('generate_report',views.generate_report)
]
