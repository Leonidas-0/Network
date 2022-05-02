from django.contrib import admin 
from .models import User, Post, Likes, Follows

admin.site.register(Follows)
admin.site.register(Likes)
admin.site.register(User)
admin.site.register(Post)
# Register your models here.
