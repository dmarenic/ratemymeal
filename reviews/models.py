from django.db import models
from django.contrib.auth.models import User

from foodposts.models import FoodPost


class CriticReview(models.Model):
    post = models.ForeignKey(
        FoodPost,
        on_delete=models.CASCADE,
        related_name='critic_reviews'
    )
    critic = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    taste_rating = models.IntegerField()
    price_rating = models.IntegerField()
    presentation_rating = models.IntegerField()
    service_rating = models.IntegerField()
    atmosphere_rating = models.IntegerField()
    review_text = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Critic review by {self.critic.username}'