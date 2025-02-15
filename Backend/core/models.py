from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=255)
    budgets = models.FloatField(default=100,editable=False,null=False)
    points = models.FloatField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Players(models.Model):
    name = models.CharField(max_length=255, unique=True)
    position = models.CharField(max_length=3)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Clubs(models.Model):
    club_name = models.CharField(max_length=255)
    kit_image_url = models.ImageField(upload_to='images')
    players = models.ManyToManyField(Players)

    def __str__(self):
        return self.club_name
    
class Team(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,name='user',editable=False)    
    players = models.ManyToManyField(Players)