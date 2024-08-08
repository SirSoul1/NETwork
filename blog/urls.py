from django.urls import path
from .views import home, post_detail
from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    path('post/<int:pk>/', post_detail, name='post-detail'),
    path('about/', views.about, name='blog-about'),
]
