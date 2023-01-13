from django.urls import path
from .views import getNews, index, post

urlpatterns = [
    path('newslist/', getNews, name='newslist'),
    path('postDetail/<str:slug>', post, name='postDetail')
]