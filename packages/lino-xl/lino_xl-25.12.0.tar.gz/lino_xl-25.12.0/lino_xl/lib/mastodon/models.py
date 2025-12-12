# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from urllib.parse import urlencode, unquote
from django.conf import settings
from social_core.backends.oauth import BaseOAuth2
from lino.api import rt, dd

MASTODON_HOST=settings.MASTODON_HOST


class MastodonOAuth2(BaseOAuth2):
    name = "mastodon"
    AUTHORIZATION_URL = f"https://{MASTODON_HOST}/oauth/authorize"
    ACCESS_TOKEN_URL = f"https://{MASTODON_HOST}/oauth/token"
    ACCESS_TOKEN_METHOD = "POST"
    REVOKE_TOKEN_URL = f"https://{MASTODON_HOST}/oauth/revoke"
    REVOKE_TOKEN_METHOD = "POST"

    STATE_PARAMETER = False
    REDIRECT_STATE = False

    def get_user_details(self, response):
        return {}

    def get_redirect_uri(self, state=None):
        return settings.MASTODON_REDIRECT_URI
