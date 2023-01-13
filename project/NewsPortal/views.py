from django.shortcuts import render
from django.http import HttpResponse
from NewsPortal.models import Post, Author

# Create your views here.

def index(request):
    return HttpResponse('Hello_news')


def getNews(request):
    post = Post.objects.all()
    return render(request, 'news_list.html', context = {'posts': post}) 