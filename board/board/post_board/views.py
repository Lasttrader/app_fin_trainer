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

from .models import Post, Category, PostCategory, Subscription

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
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'board/index.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'Posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = BoardFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
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


class BoardCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('post_board.add_post')
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'board/board_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        post.save()
        # уведомление для подписчиков о создании новой новости через 5 сек после создания
        news_notification.apply_async([post.pk], countdown=1)
        return super().form_valid(form)


class BoardEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('post_board.change_post')
    form_class = PostForm
    model = Post
    template_name = 'board/board_edit.html'


class BoardDelete(PermissionRequiredMixin, DeleteView):
    pass


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
        {'categories': categories_with_subscriptions},
    )


class UserLoginView(View):
    """
     Logs author into dashboard.
    """
    template_name = 'account/login.html'
    context_object = {"login_form": UserLoginForm}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        login_form = UserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Login Successful ! "
                                          f"Welcome {user.username}.")
                return redirect('post_board:list')
            else:
                messages.error(request,
                               f"Invalid Login details: {username}, {password} "
                               f"are not valid username and password !!! Please "
                               f"enter a valid username and password.")
                return render(request, self.template_name, self.context_object)
        else:
            messages.error(request, f"Invalid username and password")
            return render(request, self.template_name, self.context_object)


class UserLogoutView(View):
    """
     Logs user out of the dashboard.
    """
    template_name = 'account/logout.html'

    def get(self, request):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return render(request, self.template_name)


class UserRegisterView(View):
    """
      View to let users register
    """
    template_name = 'account/register.html'
    context_object = {
        "register_form": UserRegisterForm()
    }

    def get(self, request):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Bona Blog Account'
            message = render_to_string('account/account_activation_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': account_activation_token.make_token(user),
                                       })
            user.email_user(subject, message)
            return redirect('post_board:account_activation_sent')
        else:
            messages.error(request, "Please provide valid information.")
            # Redirect user to register page
            return render(request, self.template_name, self.context_object)


class AccountActivationSentView(View):

    def get(self, request):
        return render(request, 'account/account_activation_sent.html')


class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            username = user.username
            messages.success(request, f"Congratulations {username} !!! "
                                      f"Your account was created and activated "
                                      f"successfully"
                             )
            return redirect('post_board:login')
        else:
            return render(request, 'account/account_activation_invalid.html')
