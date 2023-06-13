from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from post_board.models import Comment, Post, Category
from django.core.mail import send_mail, EmailMessage
from .token import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_http_methods
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import ProfileModel
import os
# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('users/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'users/sign_up.html', context)


@login_required
def profile(request):
    # определяем формы контекста
    if request.method == 'GET':
        posts = Post.objects.filter(author=request.user)
        comments = Comment.objects.all()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        # p_form = ProfileUpdateForm(
        #     request.POST or None, request.FILES or None, instance=request.user.profilemodel)
        if u_form.is_valid():  # and p_form.is_valid():
            u_form.save()
            # p_form.save()
            return redirect('users:users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
       # p_form = ProfileUpdateForm(instance=request.user.profilemodel)
    # передаем контектс
    context = {
        'u_form': u_form,
        # 'p_form': p_form,
        'posts': posts,
        'comments': comments,
    }

    return render(request, 'users/profile.html', context)


def activate(request, uidb64, token):
    User = request.user()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
