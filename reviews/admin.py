from django.contrib import admin

from .models import CriticReview


@admin.register(CriticReview)
class CriticReviewAdmin(admin.ModelAdmin):
    list_display = ("critic", "post", "is_featured", "created_at")
    search_fields = ("critic__username", "post__title", "review_text")
    list_filter = ("is_featured", "created_at")