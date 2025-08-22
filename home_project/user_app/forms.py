
from django import forms

class ImageSearchForm(forms.Form):
    image = forms.ImageField(required=True)
