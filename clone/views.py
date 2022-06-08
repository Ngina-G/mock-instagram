from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clone.forms import UserImageForm, SignUpForm, UpdateUserForm, UpdateUserProfileForm, PostForm, CommentForm
from .models import Post, Profile, Comment
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse

# Create your views here.
   
@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
def home(request):
    images = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    params = {
        'images': images,
        'form': form,
        'users': users,

    }
    # named_redirect = reverse('profile_edit')
    # return redirect(named_redirect, params)
    return render(request, 'index.html', params)


@login_required(login_url='/accounts/login')
def profile(request, username):
    images = request.user.profile.post.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'profile_form': prof_form,
        'images': images,

    }
    return render(request, 'clone/profile.html', params)


@login_required(login_url='/accounts/login')
def user_profile(request, id):
    user_prof = get_object_or_404(User, id=id)
    if request.user == user_prof:
        return redirect('profile', id=request.user.id)
    user_posts = user_prof.profile.post.all()
    
    params = {
        'user_prof': user_prof,
        'user_posts': user_posts,
    }
    return render(request, 'clone/user_profile.html', params)

@login_required(login_url='/accounts/login')
def post_comment(request, id):
    image = get_object_or_404(Post, pk=id)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = image
            savecomment.user = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    params = {
        'image': image,
        'form': form,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
      
    }
    return render(request, 'clone/post.html', params)


def LikeView (request,pk):
    image= get_object_or_404(Post,id=request.POST.get('image_id'))
    image.likes.add(request.user)
    return HttpResponseRedirect(reverse_lazy('user',args=[str(pk)]))


@login_required(login_url='/accounts/login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'clone/search.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'clone/search.html', {'message': message})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
    
            username = form.cleaned_data.get('username')
            created_user = form.save()
            Profile.objects.get_or_create(user=created_user)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')   