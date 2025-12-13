# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.http import HttpResponseRedirect


def redirect_ifn_refresh_token(backend, response, social, *args, **kwargs):
    if backend.name == 'google' and social and response.get('refresh_token') is None and \
            social.extra_data.get('refresh_token') is None:
        return HttpResponseRedirect(
            "/oauth/login/google/?approval_prompt=force")


def intercept_extra_data(backend, user, response, *args, **kwargs):
    return kwargs
