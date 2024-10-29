# views.py
from django.shortcuts import render, redirect
from .forms import ConfigurationForm
from .models import Configuration
from django.contrib import messages

def configure(request):
    try:
        config = Configuration.objects.get(key='COLAB_API_URL')
    except Configuration.DoesNotExist:
        config = Configuration(key='COLAB_API_URL')

    if request.method == 'POST':
        form = ConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuration saved successfully.')
            return redirect('configuration:configure')  # Redirect to the same page after saving
    else:
        form = ConfigurationForm(instance=config)

    return render(request, 'configuration/configure.html', {'form': form})