from django.shortcuts import render

# Create your views here.
from .models import blog_name,blog_post

def home(request):
    return render(request,"blogs/home.html")

def all_blogs(request):
    name=blog_name.objects.all()
    context={'blog_names':name}
    return render(request,'blogs/blogs.html',context)

def blog(request,blog_id):
    name=blog_name.objects.get(id=blog_id)
    post=blog_post.objects.filter(f_key=name)
    context={'blog_name':name,'post_name':post}
    return render(request,'blogs/blog.html',context)

def posts(request):
    name=blog_name.objects.all()
    p_name=blog_post.objects.filter(f_key__in=name)
    #The __in lookup allows you to filter against multiple values. So, when you write f_key__in=name, you're telling Django: "Find all blog_post objects where f_key (the foreign key to blog_name) matches any of the blog_name objects in the QuerySet name."Essentially, it retrieves all blog posts that belong to any of the blog names in the database.
    context={'blog_name':name,'post_name':p_name}
    return render(request,'blogs/posts.html',context)

# def blogs_posts(request):
