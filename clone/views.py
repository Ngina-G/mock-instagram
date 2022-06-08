from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clone.forms import SignUpForm, UpdateUserForm, UpdateUserProfileForm, PostForm, CommentForm
from .models import Post, Profile, Comment
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
# Create your views here.
   
@login_required(login_url='/accounts/login')
def index(request):
    images = Post.objects.all()
    users = User.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
        comment_form = CommentForm()
    params = {
        'images': images,
        'form': form,
        'comment_form': comment_form,
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
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
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


def LikePost (request,pk):
    # id = request.GET.get('image_id')
    # image_id = Post.objects.get(id=id)

    post= get_object_or_404(Post,id=request.POST.get('image_id'))
    post.likes.add(request.user)

    return redirect('home')

#     if post.likes.filter(id=request.user.id).exists():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)

#     return HttpResponseRedirect(reverse('home', args=[str(pk)]))


# def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
#         liked = False
#         if likes_connected.likes.filter(id=self.request.user.id).exists():
#             liked = True
#         data['number_of_likes'] = likes_connected.number_of_likes()
#         data['post_is_liked'] = liked
#         return data


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