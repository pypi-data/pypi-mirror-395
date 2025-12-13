# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds the notion of "partner assets".

See :doc:`/plugins/assets`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Partner assets")
    asset_name = _("Partner asset")
    asset_name_plural = _("Partner assets")
    # asset_name_short = _("Asset")
    partner_model = "contacts.Partner"

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('assets.PartnerAssets')
