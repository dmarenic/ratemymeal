from django.contrib import admin

from .models import Cuisine, FoodPost, Comment, Like, Favorite, Report


admin.site.register(Cuisine)
admin.site.register(FoodPost)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Report)