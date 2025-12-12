# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds the notion of cars.

See :doc:`/plugins/cars`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Cars")
    partner_model = "contacts.Partner"

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('cars.Cars')
        m.add_action('cars.Brands')
