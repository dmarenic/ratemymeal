from django.urls import path
from .views import feed_view, create_post, post_detail


urlpatterns = [

    path(
        'feed/',
        feed_view,
        name='feed'
    ),

    path(
    'create-post/',
    create_post,
    name='create-post'
),
    path(
    'posts/<int:post_id>/',
    post_detail,
    name='post-detail'
),
]