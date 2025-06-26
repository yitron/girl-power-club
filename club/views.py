from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import MembershipApplication, Profile, Post, Comment
from .forms import (
    MembershipApplicationForm, 
    UserLoginForm, 
    ProfileUpdateForm, 
    PostForm, 
    CommentForm,
    ApproveApplicationForm
)

def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        post_form = PostForm()
        return render(request, 'club/home.html', {
            'posts': posts,
            'post_form': post_form,
        })
    return render(request, 'club/landing.html')

def join_club(request):
    if request.method == 'POST':
        form = MembershipApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            messages.success(request, 'Your application has been submitted! An admin will review it soon.')
            return redirect('join_success')
    else:
        form = MembershipApplicationForm()
    
    return render(request, 'club/join.html', {'form': form})

def join_success(request):
    return render(request, 'club/join_success.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'club/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user_profile)
    
    user_posts = Post.objects.filter(user=request.user)
    
    return render(request, 'club/profile.html', {
        'profile': user_profile,
        'form': form,
        'posts': user_posts,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('home')
    
    return redirect('home')

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'club/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user != post.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'The post has been deleted.')
        return redirect('home')
    
    return render(request, 'club/delete_post_confirm.html', {'post': post})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    
    if request.user != comment.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('post_detail', post_id=post_id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'The comment has been deleted.')
    
    return redirect('post_detail', post_id=post_id)

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def admin_applications(request):
    pending_applications = MembershipApplication.objects.filter(approved=False)
    approved_applications = MembershipApplication.objects.filter(approved=True)
    
    return render(request, 'club/admin_applications.html', {
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
    })

@user_passes_test(is_admin)
def approve_application(request, application_id):
    application = get_object_or_404(MembershipApplication, id=application_id)
    
    if application.approved:
        messages.info(request, 'This application has already been approved.')
        return redirect('admin_applications')
    
    if request.method == 'POST':
        form = ApproveApplicationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if username is already taken
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken. Please choose another one.')
                return render(request, 'club/approve_application.html', {'application': application, 'form': form})
            
            # Create user account
            user = User.objects.create_user(username=username, password=password)
            
            # Create profile
            profile = Profile.objects.create(
                user=user,
                school=application.school,
                classroom=application.classroom
            )
            
            # Update application
            application.approved = True
            application.approved_date = timezone.now()
            application.approved_by = request.user
            application.user = user
            application.save()
            
            messages.success(request, f'Application approved! Account created for {username}.')
            return redirect('admin_applications')
    else:
        form = ApproveApplicationForm()
    
    return render(request, 'club/approve_application.html', {
        'application': application,
        'form': form,
    })