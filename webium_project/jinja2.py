from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment
from django.middleware.csrf import get_token

def environment(**options):
    env = Environment(**options)
    
    # Register global functions for static assets and URL reversing in Jinja2 templates
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    
    return env
