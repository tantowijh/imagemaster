from django.conf import settings

def colab_api_url(request):
    return {
        'colab_api_url_provided': settings.COLAB_API_URL != '',
    }