from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from foodposts.models import FoodPost
from django.contrib import messages
from .models import Restaurant
from .forms import RestaurantForm


def restaurant_list(request):

    restaurants = Restaurant.objects.all()

    search_query = request.GET.get('search', '')
    city_filter = request.GET.get('city', '')

    min_rating = request.GET.get('rating')

    if search_query:
        restaurants = restaurants.filter(
            name__icontains=search_query
        )

    if city_filter:
        restaurants = restaurants.filter(
            city__icontains=city_filter
        )

    if min_rating:
        restaurants = [

            r for r in restaurants

            if r.average_rating()
            >= float(min_rating)

    ] 

    context = {
        'restaurants': restaurants,
        'search_query': search_query,
        'city_filter': city_filter,
        'rating': min_rating,
    }
    

    return render(
        request,
        'restaurants/list.html',
        context
    )



def restaurant_detail(request, restaurant_id):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    posts = restaurant.posts.all()

    top_user = None

    if posts.exists():

        top_user = max(
            posts,
            key=lambda x: x.rating
        ).author

    context = {
        'restaurant': restaurant,
        'posts': posts,
        'top_user': top_user,
    }

    return render(
        request,
        'restaurants/detail.html',
        context
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

            messages.success(request, 'Restaurant successfully created!')

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