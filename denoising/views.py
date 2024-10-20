from django.views.generic.edit import FormView
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .forms import ImageUploadForm
from .image_denoising import denoise_image

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

        return super().form_valid(form)


class ResultView(generic.TemplateView):
    template_name = 'denoising/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploaded_file_url'] = self.request.session.get('uploaded_file_url', '')
        context['denoised_image_url'] = self.request.session.get('denoised_image_url', '')
        return context