from django.urls import path

from . import views


urlpatterns = [

    path(
        'feed/',
        views.feed_view,
        name='feed'
    ),

    path(
        'create-post/',
        views.create_post,
        name='create-post'
    ),

    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name='post-detail'
    ),

    path(
        'posts/<int:post_id>/edit/',
        views.edit_post,
        name='edit-post'
    ),

    path(
        'posts/<int:post_id>/delete/',
        views.delete_post,
        name='delete-post'
    ),
    path(
    'posts/<int:post_id>/like/',
    views.toggle_like,
    name='toggle-like'
),

    path(
    'posts/<int:post_id>/favorite/',
    views.toggle_favorite,
    name='toggle-favorite'
),
    path(
    'favorites/',
    views.favorite_posts,
    name='favorites'
),

    path(
    'comments/<int:comment_id>/delete/',
    views.delete_comment,
    name='delete-comment'
),

    path(
    'comments/<int:comment_id>/edit/',
    views.edit_comment,
    name='edit-comment'
),

    path('trending/', views.trending_view, name='trending'),

    path(
        'following/',
        views.following_feed,
        name='following-feed'
),
]