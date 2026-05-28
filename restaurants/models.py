from django.db import models
from django.contrib.auth.models import User

owner = models.ForeignKey(
 User,
 on_delete=models.CASCADE,
 related_name='owned_restaurants',
 null=True,
 blank=True
)


class Restaurant(models.Model):

    name = models.CharField(
        max_length=255
    )

    city = models.CharField(
        max_length=100
    )

    address = models.CharField(
        max_length=255
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='restaurants/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def average_rating(self):

        posts = self.posts.all()

        if posts.count() == 0:
            return 0

        total = sum(post.rating for post in posts)

        return round(total / posts.count(), 1)

    def __str__(self):
        return self.name
    
    

