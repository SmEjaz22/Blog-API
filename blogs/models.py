from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class blog_name(models.Model):
    """A blog which user wants to read"""
    b_name=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE) # Connecting data to certain users. Still other logged in users can access other peoples data through url.
    
    def __str__(self):
        if len(self.b_name)>30:
            return f'{self.b_name[:30]}...'
        else:
            return f"{self.b_name}" 

class blog_post(models.Model): # if forgot models.Model then app won't makemigrations.
    f_key=models.ForeignKey(blog_name,on_delete=models.CASCADE)
    post_name=models.CharField(max_length=150)
    post=models.TextField()
    
    
    
    def __str__(self):
        if len(self.post_name)>70:
            return f"{self.post_name[:70]}..."
        else:
            return f"{self.post_name}" 
