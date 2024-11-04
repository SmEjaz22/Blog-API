from django.shortcuts import render,redirect
from .forms import BlogForm,PostForm

# Create your views here.
from .models import blog_name,blog_post
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.cache import never_cache

from .serializers import BlogSerializers,PostSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

def home(request):
    return render(request,"blogs/home.html")

@login_required # TO make it work add login_url in settings
@never_cache
# @ can help only authentic users to browse data. but authentic users can browse other users data too.

@api_view(['GET'])
def all_blogs(request):
    """Show all blogs."""
    name=blog_name.objects.filter(user=request.user) # left user is a foreign key.
    #tells Django to retrieve only the blog objects from the database whose user attribute matches the current user. We just add the ownership of data to each user. Protecting it is still left.
    # serializer=BlogSerializers(name, many=True)
    context={'blog_names':name} # Creating API not a webpage, Hence no need the context dict. 
    return render(request,'blogs/blogs.html',context)
    # return Response(serializer.data) # Creating API for all_blogs data to be consumed by Vue.

@login_required
@never_cache

@api_view(['GET','POST'])
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
    # context={'blog_name':name,'post_name':post}
    # return render(request,'blogs/blog.html',context)

    B_serializer=BlogSerializers(name) # we retrieve a single blog instance using name = blog_name.objects.get(id=blog_id). This means that the variable name holds just one blog_name object.
    P_serializer=PostSerializers(post,many=True)
    
    return Response({       #Response() you can only pass one argument for the main data, so if you try Response(B_serializer.data, P_serializer.data), it will raise an error because it doesn’t support multiple data arguments.
        'blog':B_serializer.data,
        'post':P_serializer.data
    })

from django.db.models import Count
from django.shortcuts import render

@api_view(['GET'])
def posts(request):
    # Use a queryset with annotations to count posts per author and filter for those with more than 3 posts
    if request.user.is_authenticated:
        # Get all posts, ordering by post_date, and annotating to count posts per user
        all_posts = (
            blog_post.objects
            .select_related('f_key')  # Use select_related for f_key to reduce queries
            .prefetch_related('f_key__user')  # Prefetch related user objects for efficiency
            .order_by('-post_date')
        )
    else:
        all_posts = blog_post.objects.select_related('f_key').order_by('-post_date')

    # Create a dictionary where the key is the username, and the value is a list of up to 3 posts
    posts_by_author = {}
    
    # Limit to 3 posts per author directly while iterating
    for post in all_posts:
        author = post.f_key.user.username
        if author not in posts_by_author:
            posts_by_author[author] = []
        if len(posts_by_author[author]) < 3:
            posts_by_author[author].append(post)

    # Get authors with more than 3 posts
    authors_with_more_posts = (
        blog_post.objects
        .values('f_key__user__username')
        .annotate(post_count=Count('id'))
        .filter(post_count__gt=3)
    # The __gt lookup stands for "greater than," so post_count__gt=3 filters out only those results where the post_count is greater than 3.
    # This means it will return only the authors who have more than 3 blog posts.
    )

    allPosts_serializer=PostSerializers(all_posts, many=True)
    # author_serializer=PostSerializers(authors_with_more_posts)
    
    return Response({
        'allPosts':allPosts_serializer.data,
        'More_posts':authors_with_more_posts,
        'author':author,
    })

    # context = {
    #     'posts_by_author': posts_by_author,
    #     'authors_with_more_posts': [author['f_key__user__username'] for author in authors_with_more_posts],
    #     'owner': request.user
    # }
    # return render(request, 'blogs/posts.html', context)


@login_required
@never_cache

@api_view(['GET','POST'])
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
        # return redirect('blogs:all_blogs')
    
    # context={'form':form}
    # return render(request,'blogs/new_blogs.html',context)
    
        new_Blog_serialiazer=BlogSerializers(new_blog)
        return Response(new_Blog_serialiazer.data,status=201)
    
    return Response(form.errors, status=400)
    
    

@login_required
@never_cache
@api_view(['GET', 'POST'])
def new_posts(request, blog_id):
    """View to retrieve or add posts to a specific blog."""
    
    try:
        blog = blog_name.objects.get(id=blog_id)
    except blog_name.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)
    
    if request.method == 'GET':
        # Fetch and serialize posts related to the blog
        posts = blog_post.objects.filter(f_key=blog)
        serializer = PostSerializers(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Attach the blog as the foreign key and validate input data
        serializer = PostSerializers(data=request.data)
        if serializer.is_valid():
            # Manually set the foreign key to the blog instance
            serializer.save(f_key=blog)
            return Response(serializer.data, status=201)
        else:
            # If data is invalid, return errors
            return Response(serializer.errors, status=400)
        
        
        # Create post instance without saving to the database
        # Set the foreign key to the blog instance
        # Now save the post to the database
                
#        return redirect('blogs:blogs',blog_id) 
    # or you can "return redirect('blogs:new_posts',blog_id)"
#     context={'form':form,'blog_name': blog}
#     return render(request,'blogs/new_posts.html',context)


from django.utils import timezone
@login_required
@never_cache

@api_view(['GET','POST'])
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
#        form = PostForm(instance=post)
        serializer=PostSerializers(post)
        return Response(serializer.data)
    else:
        serializer=PostSerializers(post, data=request.data)
        if serializer.is_valid():
            if serializer.initial_data != serializer.validated_data:
                post.post_date=timezone.now()   # Is same as "post.post_date = timezone.now()"  # Update only if changes were made

    # Manually set the foreign key to the blog instance
            serializer.save(f_key=f_key)
            return Response(serializer.data, status=201)
        else:
            # If data is invalid, return errors
            return Response(serializer.errors, status=400)

                            # PREVIOUS CODE:
        # POST data submitted; process data.
#       form = PostForm(instance=post, data=request.POST)
#        if form.is_valid():
#            if form.has_changed():  # Check if any fields were actually changed
#                post.post_date = timezone.now()  # Update only if changes were made
#            form.save()
#            return redirect('blogs:blogs', f_key.id)
#    context = {'post': post, 'blog': f_key, 'form': form}
#    return render(request, 'blogs/edit_posts.html', context)

@api_view(['GET'])
def user_posts(request, username):
    # Fetch all posts for the specified author based on `blog_name`
    user_posts = blog_post.objects.filter(f_key__user__username=username).order_by('-post_date')
    
    serializer=PostSerializers(user_posts ,many=True)
    return Response(serializer.data)
    # context = {'user_posts': user_posts, 'author': username}
    # return render(request, 'blogs/user_posts.html', context)

def check_blog_owner(request,article):
    if article.user != request.user:
        raise Http404("You are not the owner of this blog or post.")
    