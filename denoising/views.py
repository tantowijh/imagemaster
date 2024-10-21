from django.views.generic.edit import FormView
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .forms import ImageUploadForm
from .image_denoising import denoise_image
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
class IndexView(FormView):
    template_name = 'denoising/index.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('denoising:result')

    def form_valid(self, form):
        image = form.cleaned_data['image']
        denoise_method = form.cleaned_data['denoise_method']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        denoise_image_filename = denoise_image(fs.path(filename), denoise_method)
        denoised_image_url = fs.url(denoise_image_filename)

        self.request.session['uploaded_file_url'] = uploaded_file_url
        self.request.session['denoised_image_url'] = denoised_image_url

        self.request.session['denoise_image_uploaded'] = True

        return super().form_valid(form)


class ResultView(generic.TemplateView):
    template_name = 'denoising/result.html'

    def get(self, request, *args, **kwargs):
        if not self.request.session.get('denoise_image_uploaded', False):
            messages.error(request, "You must upload an image before accessing the result page.")
            return redirect('denoising:index')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploaded_file_url'] = self.request.session.get('uploaded_file_url', '')
        context['denoised_image_url'] = self.request.session.get('denoised_image_url', '')
        return context
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # Set a warning message and clear the session data when leaving the page
        if request.method == 'GET' and 'denoise_image_uploaded' in request.session:
            request.session.pop('denoise_image_uploaded', None)
            request.session.pop('uploaded_file_url', None)
            request.session.pop('denoised_image_url', None)
        return response