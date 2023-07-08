from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.index,name="index"),
    path('Register',views.register,name="register"),
    path('Login', views.login_view,name="login"),
    path('Logout',views.logout_view,name="logout"),
    
]
