from django.forms import ModelForm
from .models import Review
from django import forms


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('reviewer_name', 'review_text', 'rating_stars')
        #widgets = {'place': forms.HiddenInput()}