from django.db import models
from users.models import UserProfile


class Post(models.Model):
    preview_pic = models.ImageField(blank=True, upload_to="post_preview_pics")
    title = models.CharField(max_length=64)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['pk']

