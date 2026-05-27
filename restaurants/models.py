from django.db import models


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

    def __str__(self):
        return self.name