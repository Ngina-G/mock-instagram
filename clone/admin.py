from django.contrib import admin
from .models import Post, Comment, Profile, User
# Register your models here.

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(User)
