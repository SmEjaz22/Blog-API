from django.shortcuts import render

# Create your views here.
from .models import blog_name,blog_post

def home(request):
    return render(request,"blogs/home.html")

def blogs(request):
    name=blog_name.objects.all()
    p_name=blog_post.objects.filter(f_key=name)
    context={'blog_name':name,'post_name':p_name}
    return render(request,'blogs/blogs.html',context)

def posts(request):
    name=blog_post.objects.all()
    context={'posts_name':name}
    return render(request,'blogs/posts.html',context)

# def blogs_posts(request):
