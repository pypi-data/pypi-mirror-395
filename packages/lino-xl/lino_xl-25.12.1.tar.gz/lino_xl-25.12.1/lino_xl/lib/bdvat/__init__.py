# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Bangladeshi VAT declarations.  See :doc:`/plugins/bdvat`.

"""

from lino import ad


class Plugin(ad.Plugin):
    "This is a subclass of :class:`lino.core.plugin.Plugin`."

    needs_plugins = ['lino_xl.lib.vat']

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        m = m.add_menu("vat", site.plugins.vat.verbose_name)
        m.add_action('bdvat.Declarations')
        m.add_action('bdvat.DeclarationFields')
