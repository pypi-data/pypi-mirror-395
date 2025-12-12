# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Manage your source references (bibliography).

See :doc:`/plugins/sources`.
"""

from lino import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Sources")
    menu_group = 'publisher'
    user_agent = None
    author_model = 'sources.Author'

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('sources.Sources')

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('sources.Licenses')
        m.add_action('sources.Authors')
