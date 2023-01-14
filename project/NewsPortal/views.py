from django.shortcuts import render
from django.http import HttpResponse
from NewsPortal.models import Post, Author

# Create your views here.

def index(request):
    return HttpResponse('Hello_news')

#список новостей
def getNews(request):
    posts = Post.objects.order_by('-dateCreation')
    return render(request, 'newslist.html', context = {'posts': posts}) 

def post(request, pk):
    post = Post.objects.get(pk = pk)
    return render(request, 'postDetail.html', context = {'post': post})
