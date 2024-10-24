from django import forms
from django.conf import settings

class ImageUploadForm(forms.Form):
    image = forms.ImageField()