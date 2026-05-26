from django import forms

from .models import CriticReview


class CriticReviewForm(forms.ModelForm):

    class Meta:
        model = CriticReview
        fields = [
            'taste_rating',
            'price_rating',
            'presentation_rating',
            'service_rating',
            'atmosphere_rating',
            'review_text',
            'is_featured',
        ]