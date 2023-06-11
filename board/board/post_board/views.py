# import

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
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

from .models import Post, Category, Subscription, Comment

from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# # Blog app imports.
# from post_board.token import account_activation_token
# from post_board.forms.account.register_forms import UserRegisterForm

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
from django.shortcuts import redirect, get_object_or_404


# # Blog app imports
# from blog.forms.account.login_forms import UserLoginForm


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
        user = self.request.user
        if not user:
            return redirect('post_board:index') #TODO 404 ошибку сделать
        post.author = user
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



def wait_comment(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    obj.status = 'Waiting'
    obj.save()
    return HttpResponseRedirect(reverse_lazy('post_board:index'))


def decline_comment(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    obj.status = 'Decline'
    obj.save()
    return HttpResponseRedirect(reverse_lazy('post_board:index'))


def approved_comment(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    obj.status = 'Approved'
    obj.save()
    return HttpResponseRedirect(reverse_lazy('post_board:index'))



