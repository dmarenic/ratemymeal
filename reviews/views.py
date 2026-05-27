from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from foodposts.models import FoodPost

from .forms import CriticReviewForm
from .models import CriticReview


def critic_required(user):
    return (
        user.is_authenticated
        and hasattr(user, 'userprofile')
        and user.userprofile.role == 'CRITIC'
    )


@login_required
def critic_dashboard(request):

    if not critic_required(request.user):
        return redirect('feed')

    reviews = CriticReview.objects.filter(
        critic=request.user
    ).order_by('-created_at')

    context = {
        'reviews': reviews,
        'review_count': reviews.count(),
    }

    return render(
        request,
        'reviews/critic_dashboard.html',
        context
    )


@login_required
def create_critic_review(request, post_id):

    if not critic_required(request.user):
        return redirect('feed')

    post = get_object_or_404(
        FoodPost,
        id=post_id
    )

    if request.method == 'POST':
        form = CriticReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.critic = request.user
            review.post = post
            review.save()

            return redirect('post-detail', post_id=post.id)

    else:
        form = CriticReviewForm()

    context = {
        'form': form,
        'post': post,
    }

    return render(
        request,
        'reviews/create_review.html',
        context
    )

@login_required
def edit_critic_review(request, review_id):

    review = get_object_or_404(
        CriticReview,
        id=review_id,
        critic=request.user
    )

    if request.method == 'POST':
        form = CriticReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect('post-detail', post_id=review.post.id)

    else:
        form = CriticReviewForm(instance=review)

    context = {
        'form': form,
        'post': review.post,
        'review': review,
    }

    return render(
        request,
        'reviews/edit_critic_review.html',
        context
    )


@login_required
def delete_critic_review(request, review_id):

    review = get_object_or_404(
        CriticReview,
        id=review_id,
        critic=request.user
    )

    post_id = review.post.id

    if request.method == 'POST':
        review.delete()
        return redirect('post-detail', post_id=post_id)

    context = {
        'review': review,
    }

    return render(
        request,
        'reviews/delete_critic_review.html',
        context
    )