from django.contrib import admin

from .models import Cuisine, FoodPost, Comment, Like, Favorite, Report

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(FoodPost)
class FoodPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "cuisine",
        "post_type",
        "rating",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "author__username",
    )

    list_filter = (
        "cuisine",
        "post_type",
        "rating",
        "created_at",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "post",
        "created_at",
    )

    search_fields = (
        "author__username",
        "post__title",
        "text",
    )

    list_filter = ("created_at",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
    )

    search_fields = (
        "user__username",
        "post__title",
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
        "created_at",
    )

    search_fields = (
        "user__username",
        "post__title",
    )

    list_filter = ("created_at",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "reporter",
        "post",
        "reason",
        "created_at",
    )

    search_fields = (
        "reporter__username",
        "post__title",
        "reason",
        "description",
    )

    list_filter = (
        "reason",
        "created_at",
    )

