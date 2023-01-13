from django.urls import path
from .views import getNews, index

urlpatterns = [
    path('news_list/', getNews),
]