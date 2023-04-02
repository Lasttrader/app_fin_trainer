from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse

# Create your models here.


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE) #id и связь с user
    ratingAuthor = models.SmallIntegerField(default=0) #rating

    def update_rating(self): # вместо цикл for лучше использовать aggregate 
        postRat = self.post_set.aggregate(postedRating = Sum('postRating'))
        pRating = 0
        pRating += postRat.get('postedRating')
        commentRat = self.authorUser.comment_set.aggregate(commentRating = Sum('commentRating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.ratingAuthor = (pRating + cRat) / 2 #изменил формулу
        self.save()
    
    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True) #ctagory name
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name = 'Категории'


class Post(models.Model): #post
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST = 'PST'
    CASES = 'CS'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
        (POST, 'Пост'),
        (CASES, 'Кейс')
    )
    categoryType = models.CharField(max_length= 4, choices=CATEGORY_CHOICES, default=POST )
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory') #связь many2many с классом PostCategory
    postTitle = models.CharField(max_length = 255)
    postText = models.TextField() 
    postRating = models.SmallIntegerField(default=0) #rating из класса автор
    slug = models.SlugField(max_length=128, unique=False, null=True)

    def __str__(self):
        return f'{self.name.title()}: {self.description[:10]}'

    def get_absolute_url(self):
        return reverse('news:postDetail', kwargs = {'pk' : self.pk}) # здесь тоже пишем через :
    
    #методы после создания атрибутов, можно приступить к описанию методов
    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return f'{self.postText[0:100]}{" ..."}' #форматирование лучший вариант нежели просто конкатенация

    def __str__(self):
        return self.postTitle


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete = models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.Case)
    commentText = models.TextField()
    commentDateCreation = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default = 0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()


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
