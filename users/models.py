from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to="user_avatars")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f" {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'