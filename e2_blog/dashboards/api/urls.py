from django.urls import path
from .views import BlogPostListAPIView

urlpatterns = [
    path('blogs/', BlogPostListAPIView.as_view(), name='blogs_api'),
]
