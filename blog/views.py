
from typing import Any
from django.shortcuts import render,  get_object_or_404
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from django.contrib import messages as django_messages
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import PostForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.db.models import Max


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent__isnull=True)
        context['comment_form'] = CommentForm
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)

class PostCreateView(LoginRequiredMixin,CreateView,UserPassesTestMixin):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
   

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/home/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

@login_required
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    data = {
        'liked': liked,
        'total_likes': post.likes.count()
    }
    return JsonResponse(data)
    

@login_required
def message_form(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('home')
    else:
        form = MessageForm()
    return render(request, 'blog/message_form.html', {'form': form})

@login_required
def message_list(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            django_messages.success(request, "Message sent successfully!")
            return redirect('message-list')  # Redirect to avoid resubmission of form
    else:
        form = MessageForm()

    # Group received messages by sender, showing only the latest message
    latest_received_messages = Message.objects.filter(receiver=request.user).values('sender').annotate(last_message=Max('timestamp')).order_by('-last_message')
    received_messages = Message.objects.filter(receiver=request.user, timestamp__in=[msg['last_message'] for msg in latest_received_messages])

    # Group sent messages by receiver, showing only the latest message
    latest_sent_messages = Message.objects.filter(sender=request.user).values('receiver').annotate(last_message=Max('timestamp')).order_by('-last_message')
    sent_messages = Message.objects.filter(sender=request.user, timestamp__in=[msg['last_message'] for msg in latest_sent_messages])

    # Pre-decrypt messages
    for message in received_messages:
        message.decrypted_content = decrypt_message_content(message, request.user)
    for message in sent_messages:
        message.decrypted_content = decrypt_message_content(message, request.user)


    # Pagination for received messages
    received_paginator = Paginator(received_messages, 4)  # Show 4 messages per page
    received_page_number = request.GET.get('received_page')
    received_page_obj = received_paginator.get_page(received_page_number)

    # Pagination for sent messages
    sent_paginator = Paginator(sent_messages, 4)  # Show 5 messages per page
    sent_page_number = request.GET.get('sent_page')
    sent_page_obj = sent_paginator.get_page(sent_page_number)

    return render(request, 'blog/message_list.html', {
        'form': form,
        'received_messages': received_page_obj,
        'sent_messages': sent_page_obj,
        'received_page_obj': received_page_obj,
        'sent_page_obj': sent_page_obj,
    })

@login_required
def conversation_view(request, username):
    conversation_user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        form.fields['receiver'].initial = conversation_user
        print("Form data before validation:", form.data)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = conversation_user
            message.save()
            
            print("Message saved successfully")
            return redirect('conversation-view', username=username)
        else:
            print("Form is invalid:", form.errors)
    else:
        form = MessageForm(initial={'receiver': conversation_user})

    # Fetch all messages between the two users
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=conversation_user)) |
        (Q(sender=conversation_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    # Decrypt messages
    for message in messages:
        message.decrypted_content = decrypt_message_content(message, request.user)

    return render(request, 'blog/conversation_view.html', {
        'form': form,
        'messages': messages,
        'conversation_user': conversation_user,
    })

def decrypt_message_content(message, user):
    try:
        cipher_suite = Fernet(message.key.encode('utf-8'))
        decrypted_content = cipher_suite.decrypt(message.content.encode('utf-8')).decode('utf-8')
        return decrypted_content
    except InvalidToken:
        return "Decryption failed: Invalid token."
    except Exception as e:
        return f"Decryption error: {str(e)}"
    

def base_context(request):
    context = {}
    if request.user.is_authenticated:
        context['has_unread_messages'] = Message.objects.filter(receiver=request.user, read=False).exists()
    return context


@csrf_exempt
@login_required
def mark_messages_as_read(request):
    if request.method == 'POST':
        Message.objects.filter(receiver=request.user, read=False).update(read=True)
        return JsonResponse({'success': True})
    return JsonResponse({"status": "error"}, status=400)


def search(request):
    query = request.GET.get('q')

    if query:
        # Search for users by username
        user_results = User.objects.filter(username__icontains=query)
        
        # Search for posts by title or content
        post_results = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)

        # Pagination for posts
        paginator = Paginator(post_results, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if user_results.exists() or post_results.exists():
            return render(request, 'blog/post_search_results.html', {
                'query': query,
                'posts': page_obj,
                'page_obj': page_obj,
                'is_paginated': page_obj.has_other_pages(),
                'users': user_results,
            })
        else:
            # If no users or posts are found, return an empty results page
            return render(request, 'blog/search_results.html', {'query': query, 'results': None})

    # If no query is provided, just render the search results with no results
    return render(request, 'blog/search_results.html', {'query': query, 'results': None})


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'users/profile_view.html', {'profile_user': profile_user})






def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'blog/contact.html', {'title': 'Contact'})

# def search(request):
#     return render(request, 'blog/search.html', {'title': 'Search'})

def privacy(request):
    return render(request, 'blog/privacy.html', {'title': 'Privacy'})

def login(request):
    return render(request, 'blog/login.html', {'title': 'Login'})

def register(request):
    return render(request, 'blog/register.html', {'title': 'Register'})


