from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Django uses a default view function for login template. We don't need to create one.
# We are using Django default USERCREATIONFORM but write our own views and templates.

def register(request):
    """Registering a new user """
    if request.method != 'POST':
        form=UserCreationForm()
    else:
         form=UserCreationForm(data=request.post)
    if form.is_valid():
        newuser=form.save()
        login(request,newuser) # As we are seeing here, login takes newuser in it's parame.
        return redirect('blogs:all_blogs')
    context={'form':form}
    return render(request,'registration/register.html',context)     
    