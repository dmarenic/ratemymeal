from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.restaurant_list,
        name='restaurant-list'
    ),

    path(
        '<int:restaurant_id>/',
        views.restaurant_detail,
        name='restaurant-detail'
    ),

    path(
        'create/',
        views.create_restaurant,
        name='create-restaurant'
    ),

    path(
    'owner/dashboard/',
    views.owner_dashboard,
    name='restaurant-owner-dashboard'
    ),

    path(
    '<int:restaurant_id>/edit/',
    views.edit_restaurant,
    name='edit-restaurant'
    ),

    path(
    'owner/posts/',
    views.owner_posts,
    name='owner-posts'
    ),

]