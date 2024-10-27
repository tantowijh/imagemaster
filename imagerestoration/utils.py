# views.py
import os
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
import re
import requests
import logging
from django.contrib import messages
from functools import wraps

def cleanup_media_and_redirect(request, redirect_url_name):
    media_dir = settings.MEDIA_ROOT

    # Delete all files in the media directory
    for root, dirs, files in os.walk(media_dir):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

    # Clear all sessions
    Session.objects.all().delete()

    # Redirect to the desired page
    return redirect(redirect_url_name)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to validate URL
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, url) is None:
        return False
    try:
        response = requests.get(url, timeout=5)  # Set a timeout of 5 seconds
        return response.status_code == 200
    except requests.RequestException as e:
        logger.error(f"Error validating URL {url}: {e}")
        return False

# Function to check COLAB_API_URL
def valid_colab_api_url():
    colab_api_url = settings.COLAB_API_URL
    return is_valid_url(colab_api_url)

def check_valid_colab_api_url(redirect_url):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            # Determine if the first argument is `self` (class-based view) or `request` (function-based view)
            if hasattr(args[0], 'request'):
                request = args[0].request  # class-based view
            else:
                request = args[0]  # function-based view

            if not valid_colab_api_url():
                messages.error(request, "Invalid COLAB_API_URL. Please check the configuration and restart the app.")
                return redirect(redirect_url)
            return view_func(*args, **kwargs)
        return _wrapped_view
    return decorator