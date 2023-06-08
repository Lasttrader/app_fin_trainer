from django.urls import path, include
from .views import (index,
                    BoardList,
                    BoardCreate,
                    BoardDetail,
                    BoardCreate,
                    BoardEdit,
                    BoardDelete,
                    subscriptions,
                    UserLoginView,
                    UserLogoutView,
                    UserRegisterView,
                    AccountActivationSentView,
                    ActivateView)
from django.views.decorators.cache import cache_page


app_name = 'post_board'  # имя приложения, это учитывается в шаблонах и во views
urlpatterns = [
    path('', index, name='index'),
    path('main/', BoardList.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('account_activation_sent/', AccountActivationSentView.as_view(),
         name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),

    path('board_create/', BoardCreate.as_view(), name='board_create'),
    path('board_detail/<int:pk>/', BoardDetail, name='board_detail'),
    path('board_edit/<int:pk>/', BoardEdit.as_view(), name='board_edit'),
    path('board_delete/<int:pk>/', BoardDelete.as_view(), name='board_delete'),

]
