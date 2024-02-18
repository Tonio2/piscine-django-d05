from django import forms


class MovieForm(forms.Form):
    movie = forms.CharField()
