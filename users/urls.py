from django.urls import path
from . import views

urlpatterns = [
    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'users/<str:username>/',
        views.profile_view,
        name='profile'
    ),

    path(
        'profile/edit/',
        views.edit_profile,
        name='edit-profile'
    ),
]


