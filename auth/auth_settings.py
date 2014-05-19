from django.conf import settings

VIEW_ROLES = (
    'Administrator',
    'Contributor',
)
EDIT_ROLES = (
    'Administrator',
    'Contributor',
)
VIEW_GROUPS = (
    'eionet-nfp',
)
EDIT_GROUPS = (
    'eionet-nrc-forwardlooking',
)

ROLES = VIEW_ROLES + EDIT_ROLES
GROUPS = VIEW_GROUPS + EDIT_GROUPS

SKIP_EDIT_AUTHORIZATION = settings, 'SKIP_EDIT_AUTHORIZATION', False
