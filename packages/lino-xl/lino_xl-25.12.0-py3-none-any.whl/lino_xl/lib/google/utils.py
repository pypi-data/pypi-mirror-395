# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import json
import datetime
from pathlib import Path
from lino import logger

try:
    from google.oauth2.credentials import Credentials
    from google.auth.exceptions import RefreshError
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build as discovery_build
    from googleapiclient.errors import HttpError
    from httplib2.error import ServerNotFoundError
    from social_django.models import UserSocialAuth
except ImportError:

    class UserSocialAuth:
        pass


from django.conf import settings

from lino.api import dd

User = settings.SITE.user_model


def build(*args, **kwargs):
    return discovery_build(*args, **kwargs)


def update_creds(user, creds):
    suser = user.social_auth.get(provider='google')
    suser.extra_data['access_token'] = creds.token
    suser.extra_data['expiry'] = datetime.datetime.timestamp(creds.expiry)
    suser.extra_data['refresh_token'] = creds.refresh_token
    suser.extra_data['rapt_token'] = creds.rapt_token
    suser.full_clean()
    suser.save()


def get_credentials(user):
    try:
        suser = user.social_auth.get(provider='google')
    except UserSocialAuth.DoesNotExist:
        raise Exception(f"{user} does not have a connected google account")

    if suser.extra_data.get('refresh_token') is None:
        raise Exception(f"{user} does not have a refresh_token")

    with open(dd.plugins.google.client_secret_file) as f:
        client_secret = json.load(f)

    def get_expiry(creds_data):
        if creds_data['expiry']:
            return datetime.datetime.fromtimestamp(creds_data['expiry'])
        return datetime.datetime.fromtimestamp(
            creds_data['auth_time']) + datetime.timedelta(
                seconds=creds_data['expires_in'])

    creds = Credentials(token_uri=client_secret['web']['token_uri'],
                        client_id=client_secret['web']['client_id'],
                        client_secret=client_secret['web']['client_secret'],
                        token=suser.extra_data['access_token'],
                        refresh_token=suser.extra_data['refresh_token'],
                        rapt_token=suser.extra_data['rapt_token'],
                        id_token=suser.extra_data['id_token'],
                        expiry=get_expiry(suser.extra_data),
                        scopes=scps.split() if isinstance(
                            scps := suser.extra_data['scopes'], str) else scps)

    return creds


def get_resource(user: User, people: bool = False):
    """
    Deprecated: Use `get_credentials` and `build` instead.
    """
    creds = get_credentials(user)
    if people:
        return build('people', 'v1', credentials=creds), creds
    return build('calendar', 'v3', credentials=creds), creds


def make_api_call(make_request_fn,
                  args=tuple(),
                  kwargs=None,
                  msg_fn=None,
                  silent=False,
                  _retry=0):
    if kwargs is None:
        kwargs = {}

    try:
        return make_request_fn(
            *args, **kwargs).execute(num_retries=dd.plugins.google.num_retries)
    except HttpError as e:
        if msg_fn is not None:
            logger.error(msg_fn(e, *args, **kwargs))
        else:
            logger.error(e.reason)
        if e.status_code >= 500:
            # TODO: something wrong in the backend. Disable the related system tasks?
            pass
        if not silent:
            raise e
    except ServerNotFoundError as e:
        if _retry < dd.plugins.google.num_retries:
            return make_api_call(make_request_fn, args, kwargs, msg_fn, silent,
                                 _retry + 1)
        # TODO: disable the related system tasks?
        raise e
    return


# def _get_resource(user: User, people: bool = False):
#     """
#     TODO: Move this code to book.
#     Do not use this in any production code.
#     """
#     try:
#         user.social_auth.get(provider='google')
#     except UserSocialAuth.DoesNotExist:
#         try:
#             import lino_book
#         except ImportError:
#             return None
#         with (Path(lino_book.__file__).parent / 'projects' / 'noi1e' /
#               'tests' / 'demo_google_user.json').open('r') as f:
#             user_data = json.load(f)
#         social_user = UserSocialAuth(provider='google', user=user, **user_data)
#         social_user.full_clean()
#         social_user.save()
#     return get_resource(user, people)
