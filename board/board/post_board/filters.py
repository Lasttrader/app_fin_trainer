from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Category

# на шаблоне первой страницы где подвыборка постов
# Создаем свой набор фильтров для модели post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class BoardFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='postCategory',  # поле из модели
        queryset=Category.objects.all(),
        label='Category',
        conjoined=True)

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.

        fields = {
            # поиск по названию
            'postTitle': ['icontains']}
