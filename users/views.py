from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from foodposts.models import FoodPost, Favorite 
from .models import UserProfile
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

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

class CustomLoginView(LoginView):

    template_name = 'users/login.html'

    def get_success_url(self):

        user = self.request.user

        if user.is_staff or user.is_superuser:
            return reverse_lazy('admin-dashboard')

        return reverse_lazy('feed')


@login_required
def profile_view(request, username):

    profile_user = User.objects.get(
        username=username
    )

    profile = profile_user.userprofile

    posts = FoodPost.objects.filter(
        author=profile_user
    ).order_by('-created_at')

    favorites = Favorite.objects.filter(
        user=profile_user
    ).order_by('-created_at')

    is_following = profile.followers.filter(
        id=request.user.id
    ).exists()

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'favorites': favorites,
        'is_following': is_following,
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

@login_required
def toggle_follow(request, username):

    profile = get_object_or_404(
        UserProfile,
        user__username=username
    )

    if request.user in profile.followers.all():

        profile.followers.remove(
            request.user
        )

    else:

        profile.followers.add(
            request.user
        )

    return redirect(
        'profile',
        username=username
    )