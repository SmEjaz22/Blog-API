from django.db import models

# Create your models here.
class blog_name(models.Model):
    """A blog which user wants to read"""
    blog_name=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if len(self.blog_name)>70:
            return f'{self.blog_name[:70]}'
        else:
            return f"{self.blog_name}" 

class blog_posts(models.Model): # if forgot models.Model then app won't makemigrations.
    f_key=models.ForeignKey(blog_name,on_delete=models.CASCADE)
    post_name=models.CharField(max_length=150)
    post=models.TextField()
    
    
    
    def __str__(self):
        if len(self.post_name)>70:
            return f"{self.post_name[:70]}..."
        else:
            return f"{self.post_name}" 
