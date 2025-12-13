# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for managing chatbot notifications on preferably Element.io app.

See :doc:`/specs/matrix`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Matrix")
    broadcast_room_id = "!BhOVybUXrTqHDfwjWd:matrix.org"

    credentials_file = None
    user_id = None
    user_password = None

    def pre_site_startup(self, site):
        super().pre_site_startup(site)
        cred_file = site.site_dir / "secrets" / "matrix_credentials.txt"
        # userid pasword
        # cred_file = site.site_dir / "secrets" / "matrix_credentials_file.json"
        if cred_file.exists():
            self.user_id, self.user_password = cred_file.read_text().strip().split(maxsplit=1)
            # self.credentials_file = cred_file
