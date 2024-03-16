from . import views
from django.urls import path

urlpatterns=[
    path('',views.nurse_form),
    path('login',views.nurse_login),
    path('show_order',views.show_order),
    path('give_order',views.give_order),
    path('sample_collector_took_order',views.sample_collector_took_order),
    path('nurse_test_collected',views.nurse_test_collected),
    path('send_to_lab',views.send_sample_to_lab),
    path('pathologist_took_order',views.pathologist_took_order)
]
