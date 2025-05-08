from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CategoryViewSet, BlogViewSet, CommentViewSet, UserViewSet
from .views import BlogsListAPIView
from .api_views import UserCreateView
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/blogs/', BlogsListAPIView.as_view(), name='blogs_api'),
    path('api/users/', UserCreateView.as_view(), name='user-create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
