from django.shortcuts import render
from .models import FoodPost


def feed_view(request):

    posts = FoodPost.objects.all().order_by('-created_at')

    context = {
        'posts': posts
    }

    return render(
        request,
        'posts/feed.html',
        context
    )