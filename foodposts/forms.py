from django import forms

from restaurants.models import Restaurant

from .models import FoodPost, Comment, Report


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['reason', 'description']

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Explain why you are reporting this post...'
                }
            )
        }


class FoodPostForm(forms.ModelForm):

    class Meta:

        model = FoodPost

        fields = [
            'title',
            'description',
            'image',
            'cuisine',
            'post_type',
            'rating',
            'restaurant',
        ]

        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    'min': 1,
                    'max': 5,
                    'step': 1
                }
            )
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user and user.userprofile.role == 'RESTAURANT_OWNER':

            self.fields['restaurant'].queryset = (
                Restaurant.objects.filter(owner=user)
            )

    def clean_rating(self):

        rating = self.cleaned_data['rating']

        if rating < 1 or rating > 5:

            raise forms.ValidationError(
                'Rating must be between 1 and 5.'
            )

        return rating


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment

        fields = ['text']

        widgets = {

            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            )

        }