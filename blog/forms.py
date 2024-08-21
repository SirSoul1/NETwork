# blog/forms.py

from django import forms
from .models import Comment, Message, Post

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment here...',
        'rows': 4,
    }))

    class Meta:
        model = Comment
        fields = ['content','parent']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a reply...'}),
            'parent': forms.HiddenInput
        }

# Form for sending messages
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver','content']

        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Type your message here...'})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'youtube_url']


        


