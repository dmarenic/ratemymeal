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

        widgets = {
            'taste_rating': forms.NumberInput(
                attrs={'min': 1, 'max': 5}
            ),

            'price_rating': forms.NumberInput(
                attrs={'min': 1, 'max': 5}
            ),

            'presentation_rating': forms.NumberInput(
                attrs={'min': 1, 'max': 5}
            ),

            'service_rating': forms.NumberInput(
                attrs={'min': 1, 'max': 5}
            ),

            'atmosphere_rating': forms.NumberInput(
                attrs={'min': 1, 'max': 5}
            ),
        }