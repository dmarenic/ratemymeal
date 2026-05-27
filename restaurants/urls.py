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

]