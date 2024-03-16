from django.contrib import admin
from django.urls import path
from doctores import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('update_info',views.Update_doctor_info),
    path('Show_Patients',views.show_patients),
    path('test/<int:id>',views.test),
    path('login',views.loginpage),
    path('Login_verify',views.login_verify),
    path('test/test_list/<int:id>',views.test_list),
    path('test/addtest/<int:id>',views.add_test),
    path('test/removetest/<int:id>',views.remove_test),
    path('test/see_report/<int:id>',views.see_report)
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
