from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (get_object_or_404, redirect, render,)

from .forms import FoodPostForm, CommentForm
from .models import FoodPost, Comment, Like, Favorite, Cuisine
from django.core.paginator import Paginator


@login_required
def feed_view(request):

    posts = FoodPost.objects.all().order_by('-created_at')

    return render(
        request,
        'foodposts/feed.html',
        {'posts': posts}
    )


@login_required
def create_post(request):

    if request.method == 'POST':

        form = FoodPostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            post.save()

            return redirect('feed')

    else:

        form = FoodPostForm()

    return render(
        request,
        'foodposts/create_post.html',
        {'form': form}
    )


@login_required
def post_detail(request, post_id):

    post = get_object_or_404(
        FoodPost,
        id=post_id
    )

    comments = post.comments.all().order_by(
        '-created_at'
    )

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.author = request.user

            comment.post = post

            comment.save()

            return redirect(
                'post-detail',
                post_id=post.id
            )

    else:

        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(
        request,
        'foodposts/post_detail.html',
        context
    )


@login_required
def edit_post(request, post_id):

    post = get_object_or_404(
        FoodPost,
        id=post_id
    )

    if request.user != post.author and not request.user.is_staff:

        messages.error(
            request,
            'You do not have permission to edit this post.'
        )

        return redirect(
            'post-detail',
            post_id=post.id
        )

    if request.method == 'POST':

        form = FoodPostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            form.save()

            return redirect(
                'post-detail',
                post_id=post.id
            )

    else:

        form = FoodPostForm(instance=post)

    return render(
        request,
        'foodposts/edit_post.html',
        {
            'form': form,
            'post': post
        }
    )


@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        FoodPost,
        id=post_id
    )

    if request.user != post.author and not request.user.is_staff:

        messages.error(
            request,
            'You do not have permission to delete this post.'
        )

        return redirect(
            'post-detail',
            post_id=post.id
        )

    if request.method == 'POST':

        post.delete()

        return redirect('feed')

    return render(
        request,
        'foodposts/delete_post.html',
        {'post': post}
    )

@login_required
def toggle_like(request, post_id):

    post = get_object_or_404(
        FoodPost,
        id=post_id
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    )

    if like.exists():

        like.delete()

    else:

        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect(
        'post-detail',
        post_id=post.id
    )

@login_required
def toggle_favorite(request, post_id):

    post = get_object_or_404(
        FoodPost,
        id=post_id
    )

    favorite = Favorite.objects.filter(
        user=request.user,
        post=post
    )

    if favorite.exists():

        favorite.delete()

    else:

        Favorite.objects.create(
            user=request.user,
            post=post
        )

    return redirect(
        'post-detail',
        post_id=post.id
    )

@login_required
def favorite_posts(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {
        'favorites': favorites
    }

    return render(
        request,
        'foodposts/favorites.html',
        context
    )

@login_required
def feed_view(request):

    posts = FoodPost.objects.all().order_by(
        '-created_at'
    )

    cuisines = Cuisine.objects.all()

    search_query = request.GET.get(
        'search',
        ''
    )

    cuisine_filter = request.GET.get(
        'cuisine',
        ''
    )

    if search_query != '':

        posts = posts.filter(
            title__icontains=search_query
        )

    if cuisine_filter != '':

        posts = posts.filter(
            cuisine__id=cuisine_filter
        )

    paginator = Paginator(
        posts,
        6
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {
        'page_obj': page_obj,
        'cuisines': cuisines,
    }

    return render(
        request,
        'foodposts/feed.html',
        context
    )

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if (
        request.user != comment.author
        and
        not request.user.is_staff
    ):

        return redirect(
            'post-detail',
            post_id=comment.post.id
        )

    post_id = comment.post.id

    comment.delete()

    return redirect(
        'post-detail',
        post_id=post_id
    )