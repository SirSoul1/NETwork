from django.urls import path
from .views import home, post_detail
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('home/', PostListView.as_view(), name='blog-home'),
    path('home/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('home/post/new/', PostCreateView.as_view(), name='post-create'),
    path('home/post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('home/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('search/', views.search, name='blog-search'),
    path('privacy/', views.privacy, name='blog-privacy'),
    path('login/', views.login, name='blog-login'),
    path('register/', views.register, name='blog-register'),
    
]


