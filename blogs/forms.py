from django import forms
from .models import blog_name,blog_post


class BlogForm(forms.ModelForm):
    class Meta:
# The Meta class is a special inner class where you define options for the
# model or form, such as verbose_name, ordering, fields, and more. Django looks
# for this class specifically to apply those options.
# So, while it can technically be named differently, it's best practice to use
# Meta to maintain consistency and clarity in your code.
        
        
        
# The fields attribute in the Meta class of a Django form specifies which
# fields from the model should be included in the form.
# For example, if your model has name, description, and date, and you only want name and description
        model = blog_name
        fields = ['b_name'] # What you want to include in the form from your Model.py
        labels = {'b_name': ''} 
        
class PostForm(forms.ModelForm):
    class Meta:
        model = blog_post
        fields = ['post_name','post']
        labels = {'post_name': 'Post Title:'}
        widgets = {'post': forms.Textarea(attrs={'cols': 80})}