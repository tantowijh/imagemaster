from imagerestoration.utils import get_colab_api_url

def colab_api_url(request):
    return {
        'colab_api_url_provided': get_colab_api_url() != '',
    }