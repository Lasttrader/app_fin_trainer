from django.urls import path
from .views import GetNews, PostDetail, PostFilter, index, NewsCreate, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete, subscriptions, PostCategoryListView
from django.views.decorators.cache import cache_page


app_name = 'news' # имя приложения, этоу читывается в шаблонах и во views
urlpatterns = [
    path('', index, name = 'index'),
    path('news/', cache_page(60) (GetNews.as_view()), name='newslist'),#нужно убрать запятую между кэш и view
    path('news/search/', GetNews.as_view(), name = 'search'),
    path('news/create/', NewsCreate.as_view(), name = 'create'),
    path('news/<int:pk>/', PostDetail, name='postDetail'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name = 'news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name = 'news_delete'),
    path('news/subscriptions/<int:pk>/', subscriptions, name='subscriptions'),
    path('news/category/<int:pk>/', PostCategoryListView.as_view(), name = 'category')

    # path('multiply/', multiply, name = 'multiply'),
    # path('articles/create/', create_article.as_view(), name = 'article_create'),
    # path('news/<int:pk>/edit/', edit_article.as_view(), name = 'article_edit'),
    # path('news/<int:pk>/delete/', delete_article.as_view(), name = 'article_delete'),

]