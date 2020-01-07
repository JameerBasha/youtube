from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    title = models.CharField(max_length=250, default='Video')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='videos')


class Category(models.Model):
    category_name = models.CharField(max_length=250)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='categories')


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
