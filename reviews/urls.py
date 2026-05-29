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

    path(
    'reviews/edit/<int:review_id>/',
    views.edit_critic_review,
    name='edit-critic-review'
),

path(
    'reviews/delete/<int:review_id>/',
    views.delete_critic_review,
    name='delete-critic-review'
),
]