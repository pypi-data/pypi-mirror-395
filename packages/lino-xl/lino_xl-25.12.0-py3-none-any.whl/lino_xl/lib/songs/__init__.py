# -*- coding: UTF-8 -*-
# Copyright 2016-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.ad import Plugin, _


class Plugin(Plugin):
    verbose_name = _("Songs")
    menu_group = "publisher"
    needs_plugins = ['lino.modlib.languages']
    use_lilypond = True

    def get_requirements(self, site):
        if self.use_lilypond:
            yield 'lilyponddist'

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        # mg = site.plugins.office
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('songs.MySongs')

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('songs.SongTypes')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('songs.Songs')
        # m.add_action('blogs.AllTaggings')

    def get_dashboard_items(self, user):
        yield self.site.models.songs.LatestSongs
