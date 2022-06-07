from django.contrib import admin
from .models import Image, Comment
# Register your models here.

admin.site.register(Comment)
admin.site.register(Image)
