from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from project.settings import DEFAULT_FROM_EMAIL

from .models import Post, PostCategory

# def send_notifications(instance, subscribers):
#     html_content = (
#         f'Новость: {instance.postTitle}<br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на пост</a>')
#     msg = EmailMultiAlternatives(subject = instance.postTitle, body = '', from_email = DEFAULT_FROM_EMAIL, to = subscribers)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == "post_add":
        categories = instance.postCategory.all()
        # print(categories)
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [s.email for s in subscribers]
        # print(subscribers)
        users = User.objects.all()
        for u in users:
            html_content = (
                f'Новость: {instance.postTitle}<br>'
                f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
                f'Ссылка на пост</a>')
            msg = EmailMultiAlternatives(
                subject=instance.postTitle, body='', from_email=DEFAULT_FROM_EMAIL, to=[u.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
