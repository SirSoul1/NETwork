from django.shortcuts import render
from .models import Post

posts = [
    {
    'author' : 'CoreyMS',
    'title' : 'Blog Post 1',
    'content' : 'First post content',
    'date_posted' : 'August 27, 2018'
    },
    {
    'author' : 'Jane Doe',
    'title' : 'Blog Post 2',
    'content' : 'Second post content',
    'date_posted' : 'August 28, 2018'
    }

]
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'blog/contact.html', {'title': 'Contact'})

def search(request):
    return render(request, 'blog/search.html', {'title': 'Search'})

def privacy(request):
    return render(request, 'blog/privacy.html', {'title': 'Privacy'})

def login(request):
    return render(request, 'blog/login.html', {'title': 'Login'})

def register(request):
    return render(request, 'blog/register.html', {'title': 'Register'})

