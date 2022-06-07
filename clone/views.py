from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clone.forms import UserImageForm
from .models import Post, Profile, Comment

# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'index.html')
    
def user_image_request(request):  
    if request.method == 'POST':  
        form = UserImageForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
              
            return render(request, 'clone/post_form.html', {'form': form, 'img_obj': img_object})  
    else:  
        form = UserImageForm()  
  
    return render(request, 'clone/post_form.html', {'form': form})  