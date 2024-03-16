from . import views
from django.urls import path

urlpatterns=[
    path('',views.loginpage),
    path('register',views.registration),
    path('sample',views.sample_list),
    path('collect_sample',views.collect_sample)


]
