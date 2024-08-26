from django.urls import path
from .views import home, like_post, post_detail
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, mark_messages_as_read
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('home/', login_required(PostListView.as_view()), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('home/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('home/post/new/', PostCreateView.as_view(), name='post-create'),
    path('home/post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('home/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('home/messages/', views.message_list, name='message-list'),
    path('home/send/<int:pk>/', views.message_form, name='message-form'),
    path('home/messages/coversation/<str:username>/', views.conversation_view, name='conversation-view'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contact, name='blog-contact'),
    path('privacy/', views.privacy, name='blog-privacy'),
    path('login/', views.login, name='blog-login'),
    path('register/', views.register, name='blog-register'),
    path('search/', views.search, name='search'),
    path('profile/<str:username>/', views.profile_view, name='profile-view'),
    path('home/messages/mark-read', mark_messages_as_read, name='mark-messages-as-read'), 
    path('home/post/<int:pk>/like/', like_post, name='like-post'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


