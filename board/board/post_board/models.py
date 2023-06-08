from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Author(models.Model):
    authorUser = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='author_user')  # id и связь с user
    ratingAuthor = models.SmallIntegerField('rating', default=0)  # rating

    def update_rating(self):  # вместо цикл for лучше использовать aggregate
        postRat = self.post_set.aggregate(postedRating=Sum('postRating'))
        pRating = 0
        pRating += postRat.get('postedRating')
        commentRat = self.authorUser.comment_set.aggregate(
            commentRating=Sum('commentRating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.ratingAuthor = (pRating + cRat) / 2  # изменил формулу
        self.save()

    def __str__(self):
        return self.authorUser.username

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'  # множдественное число


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
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
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
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    postTitle = models.CharField(max_length=255)
    postText = models.TextField()
    postRating = models.SmallIntegerField(default=0)  # rating из класса автор
    slug = models.SlugField(max_length=128, unique=False, null=True)

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


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.Case)
    commentText = models.TextField()
    commentDateCreation = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

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
