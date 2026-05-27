from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Restaurant
from .forms import RestaurantForm


def restaurant_list(request):

    restaurants = Restaurant.objects.all()

    return render(
        request,
        'restaurants/list.html',
        {
            'restaurants': restaurants
        }
    )


def restaurant_detail(request, restaurant_id):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    return render(
        request,
        'restaurants/detail.html',
        {
            'restaurant': restaurant
        }
    )


@login_required
def create_restaurant(request):

    if request.method == 'POST':

        form = RestaurantForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                'restaurant-list'
            )

    else:

        form = RestaurantForm()

    return render(
        request,
        'restaurants/create.html',
        {
            'form': form
        }
    )