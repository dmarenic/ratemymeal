from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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

    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPES
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

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
    
class Report(models.Model):

    REPORT_TYPES = (
        ('spam', 'Spam'),
        ('offensive', 'Offensive'),
        ('fake', 'Fake Content'),
        ('other', 'Other'),
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        FoodPost,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    reason = models.CharField(
        max_length=50,
        choices=REPORT_TYPES
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'reporter',
            'post'
        )

    def __str__(self):

        return f'{self.reporter} reported {self.post}'