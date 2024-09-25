from django.db import models

from authors.models import Profile

# Create your models here.


class Tweet(models.Model):
    content = models.TextField(max_length=250)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]


class Comments(models.Model):
    content = models.TextField(max_length=250)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    for_tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
