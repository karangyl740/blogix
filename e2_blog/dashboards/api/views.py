from rest_framework.views import APIView
from rest_framework.response import Response
from dashboards.models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostListAPIView(APIView):
    def get(self, request):
        blogs = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogs, many=True)
        return Response(serializer.data)
