# -*- coding: UTF-8 -*-
# Copyright 2013-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for managing courses or other activities.

See :doc:`/specs/orders`.

"""

from django.utils.text import format_lazy

from lino.api import ad, _


class Plugin(ad.Plugin):
    verbose_name = _("Orders")
    worker_model = 'contacts.Person'
    worker_name_fields = "worker__name"
    needs_plugins = ['lino_xl.lib.cal']
    menu_group = 'invoicing'

    def pre_site_startup(self, site):
        from lino.mixins import Contactable
        from lino_xl.lib.courses.mixins import Enrollable
        self.worker_model = site.models.resolve(self.worker_model)
        super().pre_site_startup(site)

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self  # self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('orders.WaitingOrders')
        m.add_action('orders.ActiveOrders')
        m.add_action('orders.UrgentOrders')
        m.add_separator()
        # for i in site.models.orders.OrderAreas.get_list_items():
        #     m.add_action(i.orders_table)

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self  # self.get_menu_group()
        # mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('orders.AllOrders')
        m.add_action('orders.AllEnrolments')

    def get_dashboard_items(self, user):
        for i in super().get_dashboard_items(user):
            yield i
        yield self.site.models.orders.WaitingOrders
        yield self.site.models.orders.ActiveOrders
        yield self.site.models.orders.UrgentOrders
