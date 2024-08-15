from .models import Comment
from django.contrib import admin
from .models import Post

admin.site.register(Post)

admin.site.register(Comment)