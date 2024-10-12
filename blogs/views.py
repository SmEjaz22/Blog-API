from django.shortcuts import render,redirect
from .forms import BlogForm,PostForm

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

def new_blogs(request):
    """New blogs add"""
    #After the creation of forms under forms.py
    if request.method != 'POST':
        form=BlogForm()
    else:
        form=BlogForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('blogs:all_blogs')
    context={'form':form}
    return render(request,'blogs/new_blogs.html',context)

def new_posts(request,blog_id):
    """New post(s) add"""
    #After the creation of forms under forms.py
    
    blog = blog_name.objects.get(id=blog_id)
    if request.method != 'POST':
        form=PostForm()
    else:
        form=PostForm(data=request.POST)
    if form.is_valid():
        post = form.save(commit=False)  # Create post instance without saving to the database
        post.f_key = blog  # Set the foreign key to the blog instance
        post.save()  # Now save the post to the database
        return redirect('blogs:blogs',blog_id) 
    # or you can "return redirect('blogs:new_posts',blog_id)"
    context={'form':form,'blog_name': blog}
    return render(request,'blogs/new_posts.html',context)

def edit_posts(request, post_id):
    
    """Edit an existing entry."""
    post = blog_post.objects.get(id=post_id)
    f_key = post.f_key #it gives the 'blog_name' instance that the post is linked to.
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = PostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blogs', f_key.id)
    context = {'post': post, 'blog': f_key, 'form': form}
    return render(request, 'blogs/edit_posts.html', context)