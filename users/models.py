from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from cryptography.fernet import Fernet

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default="Hi! I am using Simply Social")
    encryption_key = models.CharField(max_length=100, blank=True, null=True)

    # Following and Followers fields
    followers = models.ManyToManyField(User, related_name='following', blank=True)
  
    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.user.following.count()
    
    def __str__(self):
        return f'{self.user.username} Profile'
       
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


