# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds functionality for multiple **ledgers**, i.e. separating scope of
stuff defined in :mod:`accounting <lino_xl.lib.accounting>` plugin.

See :doc:`/plugins/ledgers`.

"""

from lino.api.ad import Plugin, _


class Plugin(Plugin):
    verbose_name = _("Ledgers")
    needs_plugins = ['lino_xl.lib.accounting']

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = site.plugins.ledgers
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledgers.Ledgers')
        m.add_action('ledgers.MyLedger')

