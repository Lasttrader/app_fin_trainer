from django.urls import path, include
from .views import (index,
                    BoardList,
                    BoardCreate,
                    BoardDetail,
                    BoardCreate,
                    BoardEdit,
                    BoardDelete,
                    approved_comment,
                    decline_comment,
                    wait_comment)


app_name = 'post_board'  # имя приложения, это учитывается в шаблонах и во views
urlpatterns = [
    path('main/', BoardList.as_view(), name='index'),

    path('board_create/', BoardCreate.as_view(), name='board_create'),
    path('board_detail/<int:pk>/', BoardDetail, name='board_detail'),
    path('board_edit/<int:pk>/', BoardEdit.as_view(), name='board_edit'),
    path('board_delete/<int:pk>/', BoardDelete.as_view(), name='board_delete'),
    
    path('wait_comment/<int:pk>/', wait_comment, name='wait'),
    path('decline_comment/<int:pk>/', decline_comment, name='decline'),
    path('approved_comment/<int:pk>/', approved_comment, name='approved'),
]
