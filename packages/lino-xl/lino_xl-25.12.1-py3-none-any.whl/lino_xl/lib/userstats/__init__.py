# Copyright 2018-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# Documentation: :doc:`/plugins/userstats`.

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("User statistics")

    needs_plugins = ['lino.modlib.users']

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('userstats.UserStats')
