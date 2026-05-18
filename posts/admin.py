from django.contrib import admin

from .models import Cuisine, FoodPost


admin.site.register(Cuisine)
admin.site.register(FoodPost)