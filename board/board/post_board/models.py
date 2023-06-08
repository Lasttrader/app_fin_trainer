from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model):
    name = models.CharField('name', max_length=128,
                            unique=True, )  # ctagory name
    subscribers = models.ManyToManyField(
        User, related_name='categories', verbose_name='subscribers')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Post(models.Model):  # post
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    TANKS = 'Танки'
    HILLS = 'Хилы'
    DD = 'ДД'
    TORG = 'Торговцы'
    GILD = 'Гилдмастеры'
    KVEST = 'Квестгиверы'
    KUZNETS = 'Кузнецы'
    KOZHEV = 'Кожевники'
    ZELVAR = 'Зельевары'
    MASTERS = 'Мастера заклинаний'
    CATEGORY_CHOICES = (
        (TANKS, 'Танки'),
        (HILLS, 'Хилы'),
        (DD, 'ДД'),
        (TORG, 'Торговцы'),
        (GILD, 'Гилдмастеры'),
        (KVEST, 'Квестгиверы'),
        (KUZNETS, 'Кузнецы'),
        (KOZHEV, 'Кожевники'),
        (ZELVAR, 'Зельевары'),
        (MASTERS, 'Мастера заклинаний')
    )
    categoryType = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=TANKS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    # связь many2many с классом PostCategory
    postTitle = models.CharField(max_length=255)
    postText = models.TextField()
    upload = models.ImageField(upload_to='uploads/', null=True)

    def __str__(self):
        return f'{self.name.title()}: {self.description[:10]}'

    def get_absolute_url(self):
        # здесь тоже пишем через :
        return reverse('post_board:board_detail', kwargs={'pk': self.pk})

    def preview(self):
        # форматирование лучший вариант нежели просто конкатенация
        return f'{self.postText[0:100]}{" ..."}'

    def comment_count(self):
        return self.comment_set.all().count()

    def comments(self):
        return self.comment_set.all()

    def __str__(self):
        return self.postTitle


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.Case)
    commentText = models.TextField()
    commentDateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.commentText


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
