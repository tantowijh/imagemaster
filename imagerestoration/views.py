# views.py
import os
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.sessions.models import Session

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