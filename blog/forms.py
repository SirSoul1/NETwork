# blog/forms.py

from django import forms
from .models import Comment, Message, Post
from django.contrib.auth.models import User

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
        fields = ['receiver', 'content']

        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Type your message here...'})
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['receiver'].queryset = User.objects.filter(profile__followers=user)

    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video', 'youtube_url', 'spotify_url']

    def clean_spotify_url(self):
        url = self.cleaned_data.get('spotify_url')
        if url and not "open.spotify.com" in url:
            raise forms.ValidationError('Enter a valid Spotify URL')
        return url

        


