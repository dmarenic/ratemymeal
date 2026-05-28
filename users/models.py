from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('CRITIC', 'Food Critic'),
        ('RESTAURANT_OWNER', 'Restaurant Owner'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.png'
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='USER'
    )

    followers = models.ManyToManyField(
        User,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.user.username