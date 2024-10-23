from django.shortcuts import render,redirect
from .forms import BlogForm,PostForm

# Create your views here.
from .models import blog_name,blog_post
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.cache import never_cache

def home(request):
    return render(request,"blogs/home.html")

@login_required # TO make it work add login_url in settings
@never_cache
# @ can help only authentic users to browse data. but authentic users can browse other users data too.
def all_blogs(request):
    """Show all blogs."""
    name=blog_name.objects.filter(user=request.user) # left user is a foreign key.
    #tells Django to retrieve only the blog objects from the database whose user attribute matches the current user. We just add the ownership of data to each user. Protecting it is still left.
    context={'blog_names':name}
    return render(request,'blogs/blogs.html',context)

@login_required
@never_cache
def blog(request,blog_id):
    """Show posts of clicked blog"""
    try:
        name=blog_name.objects.get(id=blog_id)
    except blog_name.DoesNotExist:
        raise Http404("404 not found")

    
    #Make sure the blogs belongs to current user.
    # if name.user != request.user: # Means if blog_name is not owned by current user.
    #     raise Http404
    check_blog_owner(request,name)
    
    
    post=blog_post.objects.filter(f_key=name)
    context={'blog_name':name,'post_name':post}
    return render(request,'blogs/blog.html',context)


from django.db.models import Count

def posts(request):
    # Get posts grouped by each user, limiting to 3 per user
    posts_by_author = {}
    
    if request.user.is_authenticated:
        user_posts = blog_post.objects.filter(f_key__user=request.user).order_by('-post_date')
        other_posts = blog_post.objects.exclude(f_key__user=request.user).order_by('-post_date')

        # Combine the querysets so that the logged-in user's posts appear first
        all_posts = list(user_posts) + list(other_posts)
    else:
        all_posts = blog_post.objects.select_related('f_key').order_by('-post_date')

    # Create a dictionary where the key is the username, and the value is a list of up to 3 posts
    for post in all_posts:
        author = post.f_key.user.username
        if author not in posts_by_author:
            posts_by_author[author] = []
        if len(posts_by_author[author]) < 3:
            posts_by_author[author].append(post)
    
    # Check if users have more than 3 posts
    authors_with_more_posts = (
        blog_post.objects.values_list('f_key__user__username',flat=True)
        # selects the username of the user related to the f_key (foreign key) in blog_post.
        
        # The flat=True option in values_list is used to return a single list of values instead of a list of tuples.

        # Example:
        # Without flat=True: If you query for usernames without this option, the result will be a list of tuples, like this:
        # [('username1',), ('username2',), ('username3',)]
        
        # With flat=True: When you use flat=True, you get a flat list:
        # ['username1', 'username2', 'username3']
        
        .annotate(post_count=Count('id'))
        .filter(post_count__gt=3)
    )
    # In Python, round brackets can be used to group expressions or break lines without creating a tuple unless there's a comma separating values. So, this code simply defines a QuerySet using Django's ORM chain of methods and breaks it into readable lines.

    context = {
        'posts_by_author': posts_by_author,
        'authors_with_more_posts': list(authors_with_more_posts),
        'owner':request.user
    }
    return render(request, 'blogs/posts.html', context)


@login_required
@never_cache
def new_blogs(request):
    """New blogs add"""
    #After the creation of forms under forms.py
    if request.method != 'POST':
        form=BlogForm()
    else:
        form=BlogForm(data=request.POST)
    if form.is_valid():
        
        new_blog=form.save(commit=False)
        new_blog.user=request.user #We set the new blog's user attribute to the current user. 
        new_blog.save()
        
        
        
        # form.save()
        return redirect('blogs:all_blogs')
    context={'form':form}
    return render(request,'blogs/new_blogs.html',context)

@login_required
@never_cache
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


from django.utils import timezone
@login_required
@never_cache
def edit_posts(request, post_id):
    
    """Edit an existing entry."""
    try:
        post = blog_post.objects.get(id=post_id)
        f_key = post.f_key #it gives the 'blog_name' instance that the post is linked to.
    # the left f_key is now a blog object instance. We could name it anything. 
    except blog_post.DoesNotExist:
        raise Http404("404 not found")
    
    
    # if f_key.user != request.user: #f_key.user literally means blog.user. We check whether the user/owner of the blog matches the currently logged-in user. raise Http404
    
    check_blog_owner(request,f_key)
    
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = PostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            if form.has_changed():  # Check if any fields were actually changed
                post.post_date = timezone.now()  # Update only if changes were made
            form.save()
            return redirect('blogs:blogs', f_key.id)
    context = {'post': post, 'blog': f_key, 'form': form}
    return render(request, 'blogs/edit_posts.html', context)

def user_posts(request, username):
    # Fetch all posts for the specified author based on `blog_name`
    user_posts = blog_post.objects.filter(f_key__user__username=username).order_by('-post_date')
    context = {'user_posts': user_posts, 'author': username}
    return render(request, 'blogs/user_posts.html', context)

def check_blog_owner(request,article):
    if article.user != request.user:
        raise Http404("You are not the owner of this blog or post.")
    