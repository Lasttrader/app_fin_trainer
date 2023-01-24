from django.contrib.auth.mixins import LoginRequiredMixin

from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, PostCategory



# Create your views here.

def index(request):
    return HttpResponse('Hello_news')


#список новостей
class getNews(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'postTitle'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'newslist.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'Posts'
    paginate_by = 2  # вот так мы можем указать количество записей на странице

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

# # def getNews(request):
# #     posts = Post.objects.order_by('-dateCreation')
# #     return render(request, 'newslist.html', context = {'posts': posts}) 

def post(request, pk):
    post = Post.objects.get(pk = pk)
    return render(request, 'postDetail.html', context = {'post': post})

# Добавляем новое представление для создания новостей.
class create_news(LoginRequiredMixin, CreateView):
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

class edit_news(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

# Представление удаляющее новость.
class delete_news(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('newslist')

# Добавляем новое представление для создания новостей.
class create_article(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)

class edit_article(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

# Представление удаляющее новость.
class delete_article(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('newslist')




#функция умножения
def multiply(request):
   """
   Перемножение 
   """
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)
