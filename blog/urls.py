from django.urls import path
from .views import home, post_detail
from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    path('post/<int:pk>/', post_detail, name='post-detail'),
    path('home/', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('search/', views.search, name='blog-search'),
    path('privacy/', views.privacy, name='blog-privacy'),
    path('login/', views.login, name='blog-login'),
    path('register/', views.register, name='blog-register'),
]
