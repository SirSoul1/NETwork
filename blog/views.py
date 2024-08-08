from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'posts': posts})
    


# Add more views as needed, such as for viewing individual posts, adding posts, etc.
