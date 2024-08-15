
from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile-view'),  # View other users' profiles
    # The other routes related to profile management are already handled in the mysite/urls.py
]
