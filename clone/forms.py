from django.db import models  
from django.forms import ModelForm  
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment 
  
  
class UserImageForm(ModelForm):  
    class Meta:  
        model = Profile
        exclude = ['bio']
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_name',  'profile_photo', 'bio']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image',)


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('name',)
