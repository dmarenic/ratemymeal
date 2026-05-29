from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from foodposts.models import FoodPost, Favorite
from .models import UserProfile
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import (
    ProfileUpdateForm,
    RegisterForm,
    UserUpdateForm,
)


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Account successfully created! You can now log in."
            )
            return redirect("login")

    else:
        form = RegisterForm()

    context = {"form": form}

    return render(request, "users/register.html", context)


class CustomLoginView(LoginView):

    template_name = "users/login.html"

    def form_invalid(self, form):

        messages.error(self.request, "Invalid username or password.")

        return super().form_invalid(form)

    def get_success_url(self):

        user = self.request.user

        messages.success(self.request, f"Welcome back, {user.username}!")

        if user.is_staff or user.is_superuser:
            return reverse_lazy("admin-dashboard")

        return reverse_lazy("feed")


@login_required
def profile_view(request, username):

    profile_user = User.objects.get(username=username)

    profile = profile_user.userprofile

    posts = FoodPost.objects.filter(author=profile_user).order_by("-created_at")

    favorites = Favorite.objects.filter(user=profile_user).order_by("-created_at")

    is_following = profile.followers.filter(id=request.user.id).exists()

    context = {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "favorites": favorites,
        "is_following": is_following,
    }

    return render(request, "users/profile.html", context)


@login_required
def edit_profile(request):

    if request.method == "POST":

        user_form = UserUpdateForm(request.POST, instance=request.user)

        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect("profile", username=request.user.username)

    else:

        user_form = UserUpdateForm(instance=request.user)

        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {"user_form": user_form, "profile_form": profile_form}

    return render(request, "users/edit_profile.html", context)


@login_required
@require_POST
def toggle_follow(request, username):

    profile = get_object_or_404(UserProfile, user__username=username)

    if request.user in profile.followers.all():

        profile.followers.remove(request.user)
        messages.info(request, f"You unfollowed {profile.user.username}.")

    else:

        profile.followers.add(request.user)
        messages.success(request, f"You are now following {profile.user.username}.")

    return redirect("profile", username=username)
