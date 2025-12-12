# Copyright 2010-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for managing photo albums.
See :doc:`/plugins/albums`.


"""
from lino import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Albums")
    # menu_group = "office"
    menu_group = "publisher"
    needs_plugins = ['lino.modlib.uploads']

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('albums.MyAlbums')

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('albums.Albums')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('albums.AlbumItems')
