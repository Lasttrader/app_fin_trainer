from django.contrib import admin
from NewsPortal.models import Category, Post, Author
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

# создаём новый класс для представления товаров в админке
class PostAdmin(TranslationAdmin):
    model = Post
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    #list_display = [field.name for field in Post._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения
    list_display = ['postTitle','postRating','author','get_absolute_url']
    list_filter = ('postTitle', 'postRating', 'author') # добавляем примитивные фильтры в нашу админку
    search_fields = ('postTitle', 'author') # тут всё очень похоже на фильтры из запросов в базу

class CategoryAdmin(TranslationAdmin):
    model = Category


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin) # добавить класс чтобы в админке были поля
admin.site.register(Author)

