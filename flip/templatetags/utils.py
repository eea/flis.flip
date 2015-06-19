import re
from datetime import datetime
from flip.models import Study
import os

from django import template
from django.conf import settings

from flip_auth.views import is_admin, _has_perm
from flip_auth.auth_settings import EDIT_GROUPS, EDIT_ROLES


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


@register.filter
def filename(file_id):
    return os.path.basename(file_id.file.name)


@register.assignment_tag(takes_context=True)
def can_edit_study(context, study):
    request = context['request']
    if is_admin(request):
        return True
    if _has_perm(request.user_roles, request.user_groups, roles=EDIT_ROLES,
                 groups=EDIT_GROUPS) and request.user_id == study.user_id:
        return True
    return False


@register.assignment_tag(name='is_admin', takes_context=True)
def do_is_admin(context):
    return True if is_admin(context['request']) else False


@register.assignment_tag(name='get_metadata_url')
def do_get_metadata_url():
    if hasattr(settings, 'METADATA_URL'):
        return settings.METADATA_URL
    return None


@register.assignment_tag(takes_context=True)
def new_studies(context):
    request = context['request']
    last_viewed = request.session.get('last_viewed')
    if not last_viewed:
        return 0

    return Study.objects.filter(
        created_on__gt=datetime.fromtimestamp(last_viewed)
    ).exclude(
        user_id=request.user_id
    ).count()
