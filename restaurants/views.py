from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from foodposts.models import FoodPost
from django.contrib import messages
from .models import Restaurant
from .forms import RestaurantForm
from django.shortcuts import render, get_object_or_404


@login_required
def restaurant_list(request):

    if request.user.userprofile.role == "RESTAURANT_OWNER":
        return redirect("restaurant-owner-dashboard")

    restaurants = Restaurant.objects.all()

    search_query = request.GET.get("search", "")
    city_filter = request.GET.get("city", "")

    min_rating = request.GET.get("rating")

    if search_query:
        restaurants = restaurants.filter(name__icontains=search_query)

    if city_filter:
        restaurants = restaurants.filter(city__icontains=city_filter)

    if min_rating:
        restaurants = [
            r for r in restaurants if r.average_rating() >= float(min_rating)
        ]

    context = {
        "restaurants": restaurants,
        "search_query": search_query,
        "city_filter": city_filter,
        "rating": min_rating,
    }

    return render(request, "restaurants/list.html", context)


@login_required
def restaurant_detail(request, restaurant_id):

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if (
        request.user.userprofile.role == "RESTAURANT_OWNER"
        and restaurant.owner != request.user
    ):
        messages.error(request, "You can only view your own restaurants.")
        return redirect("restaurant-owner-dashboard")

    posts = restaurant.posts.all()

    top_user = None

    if posts.exists():

        top_user = max(posts, key=lambda x: x.rating).author

    context = {
        "restaurant": restaurant,
        "posts": posts,
        "top_user": top_user,
    }

    return render(request, "restaurants/detail.html", context)


@login_required
def create_restaurant(request):

    if request.user.userprofile.role != "RESTAURANT_OWNER":
        return redirect("feed")

    if request.method == "POST":

        form = RestaurantForm(request.POST, request.FILES)

        if form.is_valid():

            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()

            messages.success(request, "Restaurant successfully created!")

            return redirect("restaurant-list")

    else:

        form = RestaurantForm()

    return render(request, "restaurants/create.html", {"form": form})


@login_required
def owner_dashboard(request):

    if request.user.userprofile.role != "RESTAURANT_OWNER":
        return redirect("feed")

    restaurants = Restaurant.objects.filter(owner=request.user)

    return render(
        request, "restaurants/owner_dashboard.html", {"restaurants": restaurants}
    )


@login_required
def edit_restaurant(request, restaurant_id):

    if request.user.userprofile.role != "RESTAURANT_OWNER":
        return redirect("feed")

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if (
        request.user.userprofile.role == "RESTAURANT_OWNER"
        and restaurant.owner != request.user
    ):
        messages.error(request, "You can only edit your own restaurants.")
        return redirect("restaurant-owner-dashboard")

    if request.method == "POST":

        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)

        if form.is_valid():

            form.save()

            messages.success(request, "Restaurant successfully updated!")

            return redirect("restaurant-detail", restaurant_id=restaurant.id)

    else:

        form = RestaurantForm(instance=restaurant)

    return render(request, "restaurants/create.html", {"form": form})


@login_required
def owner_posts(request):

    if request.user.userprofile.role != "RESTAURANT_OWNER":
        return redirect("feed")

    restaurants = Restaurant.objects.filter(owner=request.user)

    posts = FoodPost.objects.filter(restaurant__in=restaurants).order_by("-created_at")

    return render(request, "restaurants/owner_posts.html", {"posts": posts})
