from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from cryptography.fernet import Fernet
import base64
from cryptography.fernet import InvalidToken
from django.core.validators import FileExtensionValidator
import re
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    # Media fields
    image = models.ImageField(upload_to='post_images/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'png', 'gif'])])
    video = models.FileField(upload_to='post_videos/', null=True, blank=True, validators=[FileExtensionValidator(['mp4'])])
    youtube_url = models.URLField(null=True, blank=True)
    spotify_url = models.URLField(null=True, blank=True)

    def clean(self):
        if self.youtube_url:
            youtube_regex = (
                r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$')
            if not re.match(youtube_regex, self.youtube_url):
                raise ValidationError('Enter a valid YouTube URL')
    
    def total_likes(self):
        return self.likes.count()
            
    
    def get_youtube_embed_url(self):
        if self.youtube_url:
            video_id = self.youtube_url.split('v=')[-1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        return None
    
    def get_spotify_embed_url(self):
        if "open.spotify.com" in self.spotify_url:
            return self.spotify_url.replace("open.spotify.com", "embed.spotify.com").replace("/track/", "/embed/track/")
        return None

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    
    def children(self):
        return Comment.objects.filter(parent=self)
    
    def is_parent(self):
        return self.parent is None

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

# Message Model

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=44, blank=True, null=True)  # Adjusted length to match Fernet key size
    read = models.BooleanField(default=False)
    class Meta:
        ordering = ['-timestamp']

    def encrypt_message(self, message):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_text = cipher_suite.encrypt(message.encode('utf-8'))
        return encrypted_text.decode('utf-8'), key.decode('utf-8')
    
    def decrypt_message(self, encrypted_text, key):
        try:
            cipher_suite = Fernet(key.encode('utf-8'))
            decrypted_text = cipher_suite.decrypt(encrypted_text.encode('utf-8')).decode('utf-8')
            return decrypted_text
        except InvalidToken:
            return "Decryption failed: Invalid token."
        except Exception as e:
            return f"Decryption error: {str(e)}"
    
    def save(self, *args, **kwargs):
        if not self.key:
            encrypted_content, key = self.encrypt_message(self.content)
            self.content = encrypted_content
            self.key = key
        super(Message, self).save(*args, **kwargs)

    def get_decrypted_content(self, user):
        try:
            if user == self.receiver or user == self.sender:
                decrypted_content = self.decrypt_message(self.content, self.key)
                print(f"Decrypted content: {decrypted_content}")  # Debugging line
                return decrypted_content
            return 'You are not authorized to view this message'
        except InvalidToken:
            return 'Invalid or corrupted message'


    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'
    
    