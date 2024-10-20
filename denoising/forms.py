# forms.py
from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    denoise_method = forms.ChoiceField(
        choices=[
            ('fastNlMeansDenoisingColored', 'Fast Non-Local Means Denoising (Colored)'),
            ('GaussianBlur', 'Gaussian Blur'),
            ('medianBlur', 'Median Blur'),
        ],
    )