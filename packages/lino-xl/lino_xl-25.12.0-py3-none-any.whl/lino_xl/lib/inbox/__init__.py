# Copyright 2013-2016 Rumma & Ko Ltd
#
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for receiving and handing them inside a Lino application.

.. autosummary::
   :toctree:

"""

from lino import ad
from django.utils.translation import gettext_lazy as _


class Plugin(ad.Plugin):

    verbose_name = _("Inbox")
    needs_plugins = ['lino.modlib.comments']

    subaddress_separator = "+"
    mailbox_path = None
    mailbox_type = "mailbox.mbox"
    discard_processed_message = False
    upload_area = 'general'
    upload_volume = 'inbox'

    # def post_site_startup(self, site):
    #     super().post_site_startup(site)
    #     site.makedirs_if_missing(self.get_uploads_root())

    def get_upload_volume(self):
        return self.site.models.uploads.Volume.get_by_ref(
            self.upload_volume, None)
