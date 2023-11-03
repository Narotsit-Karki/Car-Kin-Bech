"""
URL configuration for CAR_KIN_BECH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views
from modules.security_module.views import RegistrationFormView
from modules.security_module.forms import LoginForm

urlpatterns = [
    path('',include('resale_store_module.urls')),
    path('login', views.LoginView.as_view(template_name = "login.html",authentication_form = LoginForm), name='login'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('register', RegistrationFormView.as_view(), name='register'),
    path('admin/', admin.site.urls),
    path('payment/',include('payment_module.urls')),

]

