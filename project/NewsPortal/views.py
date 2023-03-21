from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, resolve


from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, PostCategory, Subscription


from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page # импортируем декоратор для кэширования отдельного представления
from .tasks import news_notification

# Create your views here.

def index(request):
    return redirect('news:newslist') # имя приложения:имя ссылки


#список новостей
class GetNews(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news/newslist.html'
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
       self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['filterset'] = self.filterset
       return context


class PostCategoryListView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news/post_category.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'Posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        '''
        запрос к БД. сервисная функция, чтобы получить данные по фильтру
        '''
        self.id = resolve(self.request.path_info).kwargs['pk']
        queryset = Post.objects.filter(postCategory = Category.objects.get(id=self.id))
        return queryset

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Добавляем в контекст объект фильтрации.
       context['post_category'] = Category.objects.get(id = self.id) #передаем в  шаблон
       return context


# def getNews(request):
#     posts = Post.objects.order_by('-dateCreation')
#     return render(request, 'newslist.html', context = {'posts': posts}) 
@cache_page(300) #в аргументы к декоратору передаём количество секунд, которые хотим, чтобы страница держалась в кэше.
def PostDetail(request, pk):
    post = Post.objects.get(pk = pk)
    return render(request, 'news/postDetail.html', context = {'post': post})


# Добавляем новое представление для создания новостей.
class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        post.save()
        #уведомление для подписчиков о создании новой новости через 5 сек после создания
        news_notification.apply_async([post.pk], countdown = 1)
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'


# Представление удаляющее новость.
class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news:newslist') 


# Добавляем новое представление для создания новостей.
class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news/news_create.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'


# Представление удаляющее новость.
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('newslist')


@login_required
@csrf_protect
def subscriptions(request, pk):
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
