from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.core.files.storage import FileSystemStorage
from . import forms
from django.contrib import messages
from django.conf import settings
import base64
from django.core.files.base import ContentFile
import requests
import os
from imagerestoration.utils import check_valid_colab_api_url

restoration_api_url = f'{settings.COLAB_API_URL}/restore'

class IndexView(generic.FormView):
    template_name = 'restoration/index.html'
    form_class = forms.ImageUploadForm
    success_url = reverse_lazy('restoration:mask')

    @check_valid_colab_api_url('restoration:index')
    def form_valid(self, form):
        image = form.cleaned_data['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        self.request.session['uploaded_file_name'] = filename
        self.request.session['uploaded_file_url'] = uploaded_file_url

        self.request.session['restore_image_uploaded'] = True

        return super().form_valid(form)
    


class MaskView(generic.FormView):
    template_name = 'restoration/mask.html'
    form_class = forms.MaskForm
    success_url = reverse_lazy('restoration:result')

    def get(self, request, *args, **kwargs):
        if not self.request.session.get('restore_image_uploaded', False):
            messages.error(request, "You must upload an image before accessing the mask page.")
            return redirect('restoration:index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploaded_file_url'] = self.request.session['uploaded_file_url']
        return context
    
    def form_valid(self, form):
        image = self.request.session['uploaded_file_name']
        mask_data = form.cleaned_data['mask']
        prompt = form.cleaned_data['prompt']
        guidance_scale = form.cleaned_data['guidance_scale']
        num_inference_steps = form.cleaned_data['num_inference_steps']
        strength = form.cleaned_data['strength']
        seed = form.cleaned_data['seed']
        
        format, imgstr = mask_data.split(';base64,')
        fs = FileSystemStorage()
        mask_data = ContentFile(base64.b64decode(imgstr), name='mask_' + image)
        mask = fs.save(mask_data.name, mask_data)

        files = {'image': fs.open(image), 'mask': fs.open(mask)}
        data = {
            'prompt': prompt,
            'guidance_scale': guidance_scale,
            'num_inference_steps': num_inference_steps,
            'strength': strength,
            'seed': seed
        }

        try:
            response = requests.post(restoration_api_url, files=files, data=data, timeout=120)
        except requests.RequestException as e:
            messages.error(self.request, "Network error occurred. Please check your connection and try again.")
            return redirect('restoration:index')

        if response.status_code != 200:
            messages.error(self.request, "Failed to restore the image. Please try again.")
            return redirect('restoration:index')

        # Ensure the output path is in the media directory
        base_dir = os.path.dirname(fs.path(image))
        output_filename = 'restored_' + os.path.basename(fs.path(image))
        restored_image = os.path.join(base_dir, output_filename)

        with open(restored_image, 'wb') as f:
            f.write(response.content)

        restored_image_url = fs.url(output_filename)

        self.request.session['restored_image_url'] = restored_image_url
        self.request.session['restoration_done'] = True
        
        return super().form_valid(form)
    
    


class ResultView(generic.TemplateView):
    template_name = 'restoration/result.html'

    def get(self, request, *args, **kwargs):
        if not self.request.session.get('restoration_done', False):
            messages.error(request, "You must upload an image and a mask before accessing the result page.")
            return redirect('restoration:index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploaded_file_url'] = self.request.session.get('uploaded_file_url')
        context['restored_image_url'] = self.request.session.get('restored_image_url')
        return context
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # Set a warning message and clear the session data when leaving the page
        if request.method == 'GET' and 'restoration_done' in request.session:
            request.session.pop('restore_image_uploaded', None)
            request.session.pop('uploaded_file_name', None)
            request.session.pop('uploaded_file_url', None)
            request.session.pop('restored_image_url', None)
            request.session.pop('restoration_done', None)
        return response
