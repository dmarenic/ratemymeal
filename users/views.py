from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from foodposts.models import FoodPost, Favorite 

from .forms import (
    ProfileUpdateForm,
    RegisterForm,
    UserUpdateForm,
)


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'users/register.html', context)


@login_required
def profile_view(request, username):

    profile_user = User.objects.get(
        username=username
    )

    posts = FoodPost.objects.filter(
        author=profile_user
    ).order_by('-created_at')

    favorites = Favorite.objects.filter(
        user=profile_user
    ).order_by('-created_at')

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'favorites': favorites,
    }

    return render(
        request,
        'users/profile.html',
        context
    )


@login_required
def edit_profile(request):

    if request.method == 'POST':

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect(
                'profile',
                username=request.user.username
            )

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile
        )

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(
        request,
        'users/edit_profile.html',
        context
    )