from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=10)
    birthdate = models.DateField(null=True, blank=True)  # null과 blank 허용

    def __str__(self):
        return self.username
