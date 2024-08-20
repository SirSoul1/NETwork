from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from cryptography.fernet import Fernet
import base64
from cryptography.fernet import InvalidToken


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

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