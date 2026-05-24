from django.db import models
from django.contrib.auth.models import User


class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FoodPost(models.Model):

    POST_TYPES = (
        ('restaurant', 'Restaurant'),
        ('home_made', 'Home Made'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    image = models.ImageField(
        upload_to='food_posts/'
    )

    cuisine = models.ForeignKey(
        Cuisine,
        on_delete=models.SET_NULL,
        null=True
    )

    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPES
    )

    rating = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    
class Comment(models.Model):

    post = models.ForeignKey(
        FoodPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f'{self.author} - {self.post}'
    
class Like(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        FoodPost,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'user',
            'post'
        )

    def __str__(self):

        return f'{self.user} likes {self.post}'
    
class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        FoodPost,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'user',
            'post'
        )

    def __str__(self):

        return f'{self.user} favorited {self.post}'