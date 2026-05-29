from django.shortcuts import render
from django.views.decorators.http import require_POST


def landing_page(request):
    return render(request, "core/landing.html")
