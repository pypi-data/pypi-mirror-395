# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
See :doc:`/plugins/topics`.


"""

from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Topics")

    needs_plugins = ['lino_xl.lib.xl', 'lino.modlib.gfks']

    # partner_model = 'users.User'
    # partner_model = 'contacts.Partner'
    partner_model = None

    # menu_group = 'contacts'

    def setup_config_menu(self, site, user_type, m, ar=None):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('topics.AllTopics')
        # m.add_action('topics.TopicGroups')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('topics.Tags')
        if self.partner_model is not None:
            m.add_action('topics.AllInterests')
