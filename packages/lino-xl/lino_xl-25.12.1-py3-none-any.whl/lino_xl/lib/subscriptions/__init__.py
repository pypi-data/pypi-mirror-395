# -*- coding: UTF-8 -*-
# Copyright 2013-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for managing subscriptions.

See :doc:`/plugins/subscriptions`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Subscriptions")
    needs_plugins = ['lino_xl.lib.invoicing']
    menu_group = 'trading'

    # def setup_main_menu(self, site, user_type, main, ar=None):
    #     mg = self.get_menu_group()
    #     m = main.add_menu(mg.app_label, mg.verbose_name)
    #     m.add_action('subscriptions.RefSubscriptions')

    def setup_explorer_menu(self, site, user_type, main, ar=None):
        mg = self.get_menu_group()
        m = main.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('subscriptions.AllSubscriptions')
        m.add_action('subscriptions.SubscriptionPeriods')

    # def setup_quicklinks(self, tb):
    #     tb.add_action('subscriptions.RefSubscriptions')
