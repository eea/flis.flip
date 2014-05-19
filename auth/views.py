from functools import partial

from django.shortcuts import render

from .auth_settings import (VIEW_ROLES, VIEW_GROUPS, EDIT_GROUPS, EDIT_ROLES,
                            SKIP_EDIT_AUTHORIZATION)


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        dispatch = partial(super(LoginRequiredMixin, self).dispatch,
                           request, *args, **kwargs)
        if SKIP_EDIT_AUTHORIZATION:
            return dispatch()

        has_perm = self._has_perm(request.user_roles,
                                  request.user_groups,
                                  roles=VIEW_ROLES + EDIT_ROLES,
                                  groups=VIEW_GROUPS + EDIT_GROUPS)
        if not (request.user_id and has_perm):
            return render(request, 'restricted.html')

        return dispatch()

    def _has_perm(self, user_roles, user_groups, roles, groups):
        for user_role in user_roles:
            if user_role in roles:
                return True
        for user_group in user_groups:
            if user_group[0] in groups:
                return True
        return False
