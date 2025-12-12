# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds nicknames.

See :doc:`/plugins/nicknames`.


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Nicknames")

    # settings
    named_model = None

    def pre_site_startup(self, site):
        # print("votes.pre_site_startup")
        super().pre_site_startup(site)
        if self.named_model is None:
            return
        self.named_model = site.resolve_model(self.named_model)

    def get_menu_group(self):
        p = getattr(self.site.plugins, self.named_model._meta.app_label)
        return p.get_menu_group()

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        if self.named_model is None:
            return
        mg = self.get_menu_group()
        # p = site.plugins.tickets
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('nicknames.Namings')
