# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import json
from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Mastodon API")

    backend = "lino_xl.lib.mastodon.models.MastodonOAuth2"
    client_secret_file = None

    def install_django_settings(self, site):
        super().install_django_settings(site)
        if not site.get_plugin_setting("users", "third_party_authentication"):
            return

        if self.client_secret_file is None:
            self.client_secret_file = site.site_dir / "mastodon_creds.json"

        if not self.client_secret_file.exists():
            raise Exception("Unable to find client-secret's file")

        with self.client_secret_file.open() as f:
            client_secret = json.load(f)

        site.update_settings(
            SOCIAL_AUTH_MASTODON_KEY=client_secret['client_id'],
            SOCIAL_AUTH_MASTODON_SECRET=client_secret['client_secret'],
            SOCIAL_AUTH_MASTODON_SCOPE=client_secret['scopes'],
            MASTODON_HOST="mastodon.online",
            MASTODON_REDIRECT_URI=client_secret["redirect_uri"]
        )

        if not site.social_auth_backends:
            site.social_auth_backends = []
        site.social_auth_backends.append(self.backend)
