from django.urls import path
from . import views

app_name='blogs'
# **app_name** is a predefined variable in Django that
# the framework uses specifically to recognize the namespace for
# URL patterns in an app. It must be spelled exactly as app_name,
# and any variations like app_names, appname, or appnames will not work.

urlpatterns = [
    path('',views.home,name='home'),
    path('blogs/',views.all_blogs,name='all_blogs'),
    path('blogs/<int:blog_id>',views.blog,name='blogs'),
    path('posts/',views.posts,name='posts')
]
