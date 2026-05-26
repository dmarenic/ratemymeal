from django.urls import path

from . import views


urlpatterns = [
    path(
        'critic/dashboard/',
        views.critic_dashboard,
        name='critic-dashboard'
    ),

    path(
        'reviews/create/<int:post_id>/',
        views.create_critic_review,
        name='create-critic-review'
    ),
]