# -*- coding: UTF-8 -*-
# Copyright 2016-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.ad import Plugin, _


class Plugin(Plugin):

    verbose_name = _("Vedi")

    menu_group = "publisher"

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        # mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immo.MyEntries')

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immo.EntryTypes')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('immo.Entries')
        # m.add_action('blogs.AllTaggings')

    def get_dashboard_items(self, user):
        yield self.site.models.immo.LatestEntries
        # yield self.site.models.blogs.PublicEntries
        # from lino.core.dashboard import ActorItem
        # yield ActorItem(
        #     self.site.models.blogs.LatestEntries, display_mode="list")
