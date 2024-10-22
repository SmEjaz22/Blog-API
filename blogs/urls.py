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
    path('posts/',views.posts,name='posts'),
    path('add_blogs/',views.new_blogs,name='new_blogs'),
    path('add_posts/<int:blog_id>',views.new_posts,name='new_posts'),
    path('edit_posts/<int:post_id>',views.edit_posts,name='edit_posts'),

    path('user_posts/<str:username>/', views.user_posts, name='user_posts'),
    # path('toggle_like/', views.toggle_like, name='toggle_like'),

]

