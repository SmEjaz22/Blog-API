from rest_framework import serializers
from .models import blog_post, blog_name

class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model=blog_name
        fields= '__all__'

class PostSerializers(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='f_key.user.username', read_only=True)
    #Data Representation: In your case, the owner's name is associated with the blog_post through the f_key (which refers to the related blog_name model). By specifying the owner_name field in the serializer, you're able to return this information as part of the serialized output, making it easier for clients consuming the API to get all relevant details about a post in one response.
    class Meta:
        model=blog_post
        # fields='__all__'  #Reason of comment!!! Cannot set both 'fields' and 'exclude' options on serializer PostSerializers.
        extra_fields=['owner_name']
        exclude=['f_key']