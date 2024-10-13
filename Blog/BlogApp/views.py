from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .permissions import IsAuthorOrReadOnly

# Create your views here.
def base(request):
    return render('base.html')
def index(request):
    return render(request,'index.html')
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            Profile.objects.get_or_create(user=user)
            return redirect('home')  # Redirect to the post list or any other page
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')





def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to login after successful signup
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})
@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Get all posts, newest first
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {'page_obj': page_obj})
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'createpost.html', {'form': form})

def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    print(f"Image URL: {post.image.url}") 
    return render(request, 'viewpost.html', {'post': post})

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)  # Ensure the user is the author
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view_post', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'updatepost.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('home')
    
    return render(request, 'deletepost.html', {'post': post})

@login_required
def user_feed(request):
    # Fetch only the posts authored by the logged-in user, ordered by creation date
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    return render(request, 'userfeed.html', {'posts': posts})

def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def profile_edit(request):
    if request.method == 'POST':
        # Get the user profile
        profile = request.user.profile
        
        # Update profile picture if provided
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES['profile_pic']
        
        # Update username and email
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Check if the new username is unique
        if User.objects.exclude(pk=request.user.pk).filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('profile_edit')

        # Update user model fields
        request.user.username = username
        request.user.email = email
        request.user.save()  # Save the changes to the user

        # Update other profile fields
        profile.bio = request.POST.get('bio')
        profile.location = request.POST.get('location')
        profile.save()  # Save the changes to the profile

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_view')  # Redirect to the profile view page

    return render(request, 'profileedit.html', {'user': request.user})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')  # Order by latest first
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Assign the current user as the author of the post
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Allow only the author to update their own post
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        # Allow only the author to delete their own post
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this post.")
        instance.delete()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)