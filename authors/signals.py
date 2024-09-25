from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(author=instance).save()


@receiver(post_save, sender=Profile)
def add_following_self(sender, instance, created, *args, **kwargs):
    if created:
        profile = instance
        profile.following.add(profile)
