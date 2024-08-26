
from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile-view'),  # View other users' profiles
    path('<str:username>/follow/', views.follow_user, name='follow-user'), 
]
