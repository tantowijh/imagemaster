import os
import requests
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from django.views import generic
from django.contrib import messages
from imagerestoration.utils import check_valid_colab_api_url, get_colab_api_url

class IndexView(generic.FormView):
    template_name = 'enhancement/index.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('enhancement:result')

    @check_valid_colab_api_url('configuration:configure')
    def form_valid(self, form):
        enhance_api_url = f'{get_colab_api_url()}/enhance'
        image = form.cleaned_data['image']
        files = {'image': image.read()}  # Read the image file content
        fs = FileSystemStorage()
        uploaded_image = fs.save(image.name, image)
        uploaded_file_url = fs.url(uploaded_image)
        filename = fs.path(uploaded_image)

        try:
            response = requests.post(enhance_api_url, files=files, timeout=120)
        except requests.RequestException:
            messages.error(self.request, "Failed to connect to the enhancement service. Please try again.")
            return redirect('enhancement:index')

        if response.status_code != 200:
            messages.error(self.request, "Failed to enhance the image. Please try again.")
            return redirect('enhancement:index')
        
        # Ensure the output path is in the media directory
        base_dir = os.path.dirname(filename)
        output_filename = 'enhanced_' + os.path.basename(filename)
        enhance_image = os.path.join(base_dir, output_filename)

        with open(enhance_image, 'wb') as f:
            f.write(response.content)

        enhanced_image_url = fs.url(output_filename)

        self.request.session['uploaded_image_url'] = uploaded_file_url
        self.request.session['enhanced_image_url'] = enhanced_image_url

        return super().form_valid(form)
    
class ResultView(generic.TemplateView):
    template_name = 'enhancement/result.html'

    def get(self, request, *args, **kwargs):
        if 'uploaded_image_url' not in request.session or 'enhanced_image_url' not in request.session:
            messages.error(request, "You must upload an image before accessing the result page.")
            return redirect('enhancement:index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploaded_image_url'] = self.request.session.get('uploaded_image_url', '')
        context['enhanced_image_url'] = self.request.session.get('enhanced_image_url', '')
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # Clear the session data when leaving the page
        if request.method == 'GET' and 'uploaded_image_url' in request.session:
            request.session.pop('uploaded_image_url', None)
            request.session.pop('enhanced_image_url', None)
        return response