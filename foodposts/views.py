from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

from .forms import CommentForm, FoodPostForm, ReportForm
from .models import Comment, Cuisine, Favorite, FoodPost, Like, Report

from django.contrib import messages


@login_required
def feed_view(request):

    if request.user.userprofile.role == "RESTAURANT_OWNER":
        return redirect("restaurant-owner-dashboard")

    posts = FoodPost.objects.all().order_by("-created_at")
    cuisines = Cuisine.objects.all()

    search_query = request.GET.get("search", "")
    cuisine_filter = request.GET.get("cuisine", "")
    post_type_filter = request.GET.get("post_type", "")

    if search_query:
        posts = posts.filter(title__icontains=search_query)

    if cuisine_filter:
        posts = posts.filter(cuisine__id=cuisine_filter)

    if post_type_filter:
        posts = posts.filter(post_type=post_type_filter)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "cuisines": cuisines,
        "post_types": FoodPost.POST_TYPES,
    }

    return render(request, "foodposts/feed.html", context)


@login_required
def trending_view(request):

    if request.user.userprofile.role == "RESTAURANT_OWNER":
        return redirect("restaurant-owner-dashboard")

    posts = FoodPost.objects.all()

    posts = sorted(
        posts,
        key=lambda post: (
            post.likes.count() * 2 + post.comments.count() * 3 + post.rating
        ),
        reverse=True,
    )

    context = {"posts": posts}

    return render(request, "foodposts/trending.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = FoodPostForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Post successfully created!")

            return redirect("feed")

    else:
        form = FoodPostForm(user=request.user)

    return render(request, "foodposts/create_post.html", {"form": form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(FoodPost, id=post_id)

    comments = post.comments.all().order_by("-created_at")

    is_liked = Like.objects.filter(user=request.user, post=post).exists()

    is_favorited = Favorite.objects.filter(user=request.user, post=post).exists()

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            messages.success(request, "Comment successfully created!")

            return redirect("post-detail", post_id=post.id)

    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "is_liked": is_liked,
        "is_favorited": is_favorited,
    }

    return render(request, "foodposts/post_detail.html", context)


@login_required
def edit_post(request, post_id):

    post = get_object_or_404(FoodPost, id=post_id)

    if request.user != post.author and not request.user.is_staff:

        messages.error(request, "You do not have permission to edit this post.")

        return redirect("post-detail", post_id=post.id)

    if request.method == "POST":

        form = FoodPostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():

            form.save()

            messages.success(request, "Post successfully updated!")

            return redirect("post-detail", post_id=post.id)

    else:
        form = FoodPostForm(instance=post)

    context = {
        "form": form,
        "post": post,
    }

    return render(request, "foodposts/edit_post.html", context)


@login_required
def delete_post(request, post_id):

    post = get_object_or_404(FoodPost, id=post_id)

    if request.user != post.author and not request.user.is_staff:

        messages.error(request, "You do not have permission to delete this post.")

        return redirect("post-detail", post_id=post.id)

    if request.method == "POST":

        post.delete()

        messages.success(request, "Post successfully deleted!")

        return redirect("feed")

    return render(request, "foodposts/delete_post.html", {"post": post})


@login_required
def toggle_like(request, post_id):

    post = get_object_or_404(FoodPost, id=post_id)

    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():

        like.delete()

    else:

        Like.objects.create(user=request.user, post=post)

    return redirect("post-detail", post_id=post.id)


@login_required
def toggle_favorite(request, post_id):

    post = get_object_or_404(FoodPost, id=post_id)

    favorite = Favorite.objects.filter(user=request.user, post=post)

    if favorite.exists():

        favorite.delete()

    else:

        Favorite.objects.create(user=request.user, post=post)

    return redirect("post-detail", post_id=post.id)


@login_required
def favorite_posts(request):

    if request.user.userprofile.role == "RESTAURANT_OWNER":
        return redirect("restaurant-owner-dashboard")

    favorites = Favorite.objects.filter(user=request.user).order_by("-created_at")

    context = {"favorites": favorites}

    return render(request, "foodposts/favorites.html", context)


@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author and not request.user.is_staff:
        return redirect("post-detail", post_id=comment.post.id)

    post_id = comment.post.id

    comment.delete()

    messages.success(request, "Comment successfully deleted!")

    return redirect("post-detail", post_id=post_id)


@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author and not request.user.is_staff:
        return redirect("post-detail", post_id=comment.post.id)

    if request.method == "POST":

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():

            form.save()

            messages.success(request, "Comment successfully updated!")

            return redirect("post-detail", post_id=comment.post.id)

    else:
        form = CommentForm(instance=comment)

    context = {
        "form": form,
        "comment": comment,
    }

    return render(request, "foodposts/edit_comment.html", context)


@login_required
def following_feed(request):

    if request.user.userprofile.role == "RESTAURANT_OWNER":
        return redirect("restaurant-owner-dashboard")

    followed_profiles = request.user.following.all()

    followed_users = [profile.user for profile in followed_profiles]

    posts = FoodPost.objects.filter(author__in=followed_users).order_by("-created_at")

    context = {"posts": posts}

    return render(request, "foodposts/following_feed.html", context)


@login_required
def report_post(request, post_id):

    post = get_object_or_404(FoodPost, id=post_id)

    if request.method == "POST":

        form = ReportForm(request.POST)

        if form.is_valid():

            report, created = Report.objects.get_or_create(
                reporter=request.user,
                post=post,
                defaults={
                    "reason": form.cleaned_data["reason"],
                    "description": form.cleaned_data["description"],
                },
            )

            if not created:

                report.reason = form.cleaned_data["reason"]

                report.description = form.cleaned_data["description"]

                report.save()

            messages.success(request, "Post successfully reported!")

            return redirect("post-detail", post_id=post.id)

    else:

        form = ReportForm()

    context = {"form": form, "post": post}

    return render(request, "foodposts/report_post.html", context)


@staff_member_required
def admin_dashboard(request):

    context = {
        "user_count": User.objects.count(),
        "post_count": FoodPost.objects.count(),
        "comment_count": Comment.objects.count(),
        "report_count": Report.objects.count(),
        "latest_reports": Report.objects.all().order_by("-created_at")[:5],
    }

    return render(request, "foodposts/admin_dashboard.html", context)
