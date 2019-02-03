from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    favorite_streamer = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []


class Streamer(models.Model):
    display_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name

class Event(models.Model):
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.text