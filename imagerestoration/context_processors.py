from django.conf import settings

def replicate_token(request):
    return {
        'colab_api_url_provided': settings.COLAB_API_URL != '',
    }