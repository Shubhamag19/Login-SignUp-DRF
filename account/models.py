from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
# from rest_auth.registration.serializers import RegisterSerializer


class CustomUser(AbstractUser):

    sapid = models.IntegerField(unique=True, null=True)
    dept = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    # email = models.EmailField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
