from django import forms
from .models import Movies


class MovieForm(forms.Form):
    movie = forms.ModelChoiceField(queryset=Movies.objects.all(), empty_label=None)
