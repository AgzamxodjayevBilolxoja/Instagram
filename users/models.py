from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class User(AbstractUser, BaseModel):
    GENDER_CHOICES = (
        ('undefined', 'Undefined'),
        ('male', 'Male'),
        ('female', 'Female'),
    )
    photo = models.ImageField(upload_to='media/user/photo/')
    gender = models.CharField(choices=GENDER_CHOICES, default='undefined', max_length=10)
    date_of_birth = models.DateField(auto_now_add=True)
    username = models.CharField(max_length=57, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=53, blank=True)

class Subscribe(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribers")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_subscribes")
