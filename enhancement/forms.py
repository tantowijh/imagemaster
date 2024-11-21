from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        max_size = 5 * 1024 * 1024  # 5 MB limit

        if image.size > max_size:
            raise ValidationError(f"Image file too large ( > {max_size / (1024 * 1024)} MB )")
        
        return image