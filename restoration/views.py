from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views import generic
from django.core.files.storage import FileSystemStorage
from . import forms
from .restoration import perform_restoration
from django.contrib import messages



class IndexView(generic.FormView):
    template_name = 'restoration/index.html'
    form_class = forms.ImageUploadForm
    success_url = reverse_lazy('restoration:mask')

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
        mask_data = form.cleaned_data['mask']        
        uploaded_file_name = self.request.session['uploaded_file_name']

        restored_image_name = perform_restoration(uploaded_file_name, mask_data)
        restored_image_url = FileSystemStorage().url(restored_image_name)
        
        self.request.session['restored_image_url'] = restored_image_url

        self.request.session['restoration_done'] = True

        return redirect(reverse('restoration:result'))
    
    


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
