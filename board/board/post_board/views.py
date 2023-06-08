# import

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (View,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy, resolve

from .models import Post, Category, Subscription

from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Blog app imports.
from blog.token import account_activation_token
from blog.forms.account.register_forms import UserRegisterForm

from .filters import BoardFilter
from .forms import PostForm, CommentForm
from .tasks import news_notification

from functools import reduce
import operator

# Core Django imports.
from django.contrib import messages
from django.db.models import Q
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect


# Blog app imports
from blog.forms.account.login_forms import UserLoginForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# список новостей


class BoardList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'board/index.html'
    context_object_name = 'Posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BoardFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def BoardDetail(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.commentUser = request.user
            instance.commentPost = post
            instance.save()
            return redirect('post_board:board_detail', pk=post.id)
    else:
        c_form = CommentForm()
    context = {
        'post': post,
        'c_form': c_form, }

    return render(request, 'board/board_detail.html', context)


class BoardCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'board/board_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'Танки'

        post.save()
        news_notification.apply_async([post.pk], countdown=1)
        return super().form_valid(form)


class BoardEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'board/board_edit.html'


class BoardDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('post_board.change_post')
    model = Post
    template_name = 'board/board_delete.html'
    success_url = reverse_lazy('post_board:index')


@login_required
@csrf_protect
def subscriptions(request, pk):
    """
    subscriptions
    """
    print(pk)
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()
    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'news/subscriptions.html',
        {'categories': categories_with_subscriptions},)
