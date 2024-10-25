from django import forms
from django.core.exceptions import ValidationError

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        max_size = 5 * 1024 * 1024  # 5 MB limit

        if image.size > max_size:
            raise ValidationError(f"Image file too large ( > {max_size / (1024 * 1024)} MB )")
        
        return image
    
class MaskForm(forms.Form):
    mask = forms.CharField(widget=forms.HiddenInput(
        attrs={'id': 'mask-data'}
    ))
    prompt = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'input w-full max-w-xl',
        'rows': 3,
        'placeholder': 'Enter a prompt for the restoration process...'
    }))
    guidance_scale = forms.FloatField(initial=8.0, widget=forms.NumberInput(attrs={
        'class': 'input w-full max-w-xs',
        'step': '0.1',
        'min': '0.0'
    }))
    num_inference_steps = forms.IntegerField(initial=20, widget=forms.NumberInput(attrs={
        'class': 'input w-full max-w-xs',
        'min': '1'
    }))
    strength = forms.FloatField(initial=0.99, widget=forms.NumberInput(attrs={
        'class': 'input w-full max-w-xs',
        'step': '0.01',
        'min': '0.0',
        'max': '1.0'
    }))
    seed = forms.IntegerField(initial=0, widget=forms.NumberInput(attrs={
        'class': 'input w-full max-w-xs',
        'min': '0'
    }))