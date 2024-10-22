from django.urls import path,include
from .views import CustomLoginView

app_name='accounts'
from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # Use the custom login view
    path('',include('django.contrib.auth.urls')),
    path('register/',views.register,name='register'),
]
