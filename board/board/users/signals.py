from django.contrib.auth.models import User
from .models import ProfileModel
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = ProfileModel(user=user)
        profile.save()
