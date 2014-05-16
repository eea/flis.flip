import re
import markup
import os

from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern):
    request = context['request']
    pattern = '^%s/' + pattern
    if getattr(settings, 'FORCE_SCRIPT_NAME', None):
        pattern = pattern % settings.FORCE_SCRIPT_NAME
    else:
        pattern = pattern % ''

    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.assignment_tag
def assign(value):
    return value


@register.simple_tag
def active_if_blossom(object):
    if not object.blossom:
        return 'disabled'
    return ''


@register.simple_tag
def url_if_blossom(object, url, text):
    page = markup.page()
    opt = {}
    if object.blossom:
        opt['href'] = url
    page.a(text, **opt)
    return page


@register.filter
def filename(file_id):
    return os.path.basename(file_id.file.name)
