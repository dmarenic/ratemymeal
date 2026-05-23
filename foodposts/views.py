from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import FoodPostForm
from django.shortcuts import get_object_or_404

from .models import FoodPost


@login_required
def feed_view(request):

    posts = FoodPost.objects.all().order_by('-created_at')

    context = {
        'posts': posts
    }

    return render(
        request,
        'foodposts/feed.html',
        context
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

    context = {
        'form': form
    }

    return render(
        request,
        'foodposts/create_post.html',
        context
    )
@login_required
def post_detail(request, post_id):

    post = get_object_or_404(
        FoodPost,
        id=post_id
    )

    context = {
        'post': post
    }

    return render(
        request,
        'foodposts/post_detail.html',
        context
    )