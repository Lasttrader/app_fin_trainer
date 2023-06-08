from celery import shared_task
from .models import Post
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from board.settings import DEFAULT_FROM_EMAIL
import time
import datetime


@shared_task
def news_notification(oid):
    post = Post.objects.get(pk=oid)
    categories = post.postCategory.all()
    # print(categories)
    subscribers: list[str] = []
    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = [s.email for s in subscribers]
    # print(subscribers)
    users = User.objects.all()
    for u in users:
        html_content = (
            f'Новость: {post.postTitle}<br>'
            f'<a href="http://127.0.0.1{post.get_absolute_url()}">'
            f'Ссылка на пост</a>')
        msg = EmailMultiAlternatives(
            subject=post.postTitle, body='', from_email=DEFAULT_FROM_EMAIL, to=[u.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

# уведомленя о новых новостях за неделю


@shared_task
def news_last_week():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    for p in posts:
        text = '\n'.join('{} - {}'.format(p.postTitle, p.postText))
        users = User.objects.all()
        for u in users:
            html_content = (
                f'Новость: {text}<br>',
                f'<a href="http://127.0.0.1{p.get_absolute_url()}">'
                f'Ссылка на пост</a>')
            msg = EmailMultiAlternatives(
                subject='news', body='', from_email=DEFAULT_FROM_EMAIL, to=[u.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
