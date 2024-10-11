from django.contrib import admin

# Register your models here.
from .models import blog_name,blog_posts

admin.site.register(blog_name)
admin.site.register(blog_posts)