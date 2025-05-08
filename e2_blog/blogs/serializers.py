
from rest_framework import serializers
from .models import Category, Blogs, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = UserSerializer()

    class Meta:
        model = Blogs
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    blog = BlogSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = '__all__'