from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def set_active(context, *url_names):
    request = context['request']
    current_path = request.path
    for url_name in url_names:
        target_path = reverse(url_name)
        if current_path == target_path:
            return 'active'
    return ''