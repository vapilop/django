from django import forms

from .models import ReviewsFilm


class ReviewForm(forms.ModelForm):
    # Форма для обработки отзывов
    class Meta:
        model = ReviewsFilm
        fields = ('name', 'email', 'text')
