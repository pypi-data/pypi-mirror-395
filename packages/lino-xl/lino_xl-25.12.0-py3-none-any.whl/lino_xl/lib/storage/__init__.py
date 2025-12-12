# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
See :doc:`/plugins/storage`.

"""

from django.utils.functional import lazystr

from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Storage")
    needs_plugins = ['lino_xl.lib.products', 'lino.modlib.summaries']
    # qty_length = 10
    menu_group = "products"

    # def setup_main_menu(self, site, user_type, m, ar=None):
    #     mg = self.get_menu_group()
    #     m = m.add_menu(mg.app_label, mg.verbose_name)

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('storage.TransferRules')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('storage.ProvisionStates')
        m.add_action('storage.Fillers')
        m.add_action('storage.DeliveryNotes')
        m.add_action('storage.DeliveryItems')
        m.add_action('storage.Movements')
        m.add_action('storage.Provisions')
        m.add_action('storage.Components')
