# Inside custom tag - is_active.py
from django.template import Library
from django.core.urlresolvers import reverse

register = Library()


@register.simple_tag
def is_active(request, url):
    # Main idea is to check if the url and the current path is a match
    if request.path == reverse(url):
        return "active"
    return ""
