from django import forms

from .models import FoodPost, Comment


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
        ]
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