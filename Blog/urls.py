"""
URL configuration for Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include


from django.contrib.auth.models import User, Group
from django.apps import apps  # To get all models
from django_otp.admin import OTPAdminSite
import os
# from django_otp.plugins.otp_totp.models import TOTPDevice
# from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
 
 
# Create a custom OTPAdmin site
class OTPAdmin(OTPAdminSite):
    pass

# Create an instance of the custom admin site
admin_site = OTPAdmin(name="OTPAdmin")

models = apps.get_models()
for model in models:
    try:
        admin_site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
 
 

if os.getenv('VERCEL_ENV') is None:
    from dotenv import load_dotenv
    load_dotenv()
    
admin_url = os.getenv('ADMIN_URL', 'WrongUrlBuddy.')



urlpatterns = [
    path('',include('blogs.urls')),
    path('accounts/',include('accounts.urls')),
    path(f'{admin_url}/', admin_site.urls),  
]
