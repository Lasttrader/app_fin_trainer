from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from post_board.models import Comment, Post
from django.core.mail import send_mail

from django.views.decorators.http import require_http_methods

import os
# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('users:users-login')
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'users/sign_up.html', context)


@login_required
def profile(request):
    if request.method == 'GET':
        posts = Post.objects.filter(author=request.user) # 
        comments = Comment.objects.all()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST or None, request.FILES or None, instance=request.user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('users:users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profilemodel)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'comments':comments
    }

    return render(request, 'users/profile.html', context)

