from django.contrib import admin
from post_board.models import Category, Post,  Comment


# создаём новый класс для представления товаров в админке


# Register your models here.
admin.site.register(Category)
# добавить класс чтобы в админке были поля
admin.site.register(Post)
admin.site.register(Comment)
