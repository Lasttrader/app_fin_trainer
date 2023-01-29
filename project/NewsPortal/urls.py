from django.urls import path
from .views import getNews, post, multiply, PostFilter, index, create_news, edit_news, delete_news, create_article, edit_article, delete_article, subscriptions

urlpatterns = [
    path('newslist/', getNews.as_view(), name='newslist'),
    path('postDetail/<int:pk>', post, name='postDetail'),
    path('multiply/', multiply, name = 'multiply'),
    path('search/', getNews.as_view(), name = 'search'),
    path('news/create/', create_news.as_view(), name = 'news_create'),
    path('postDetail/<int:pk>/edit/', edit_news.as_view(), name = 'news_edit'),
    path('postDetail/<int:pk>/delete/', delete_news.as_view(), name = 'news_delete'),
    path('articles/create/', create_article.as_view(), name = 'article_create'),
    path('postDetail/<int:pk>/edit/', edit_article.as_view(), name = 'article_edit'),
    path('postDetail/<int:pk>/delete/', delete_article.as_view(), name = 'article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]