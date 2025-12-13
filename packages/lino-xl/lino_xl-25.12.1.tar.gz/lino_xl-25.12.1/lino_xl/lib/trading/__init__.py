# Copyright 2014-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for trading.
See :doc:`/plugins/trading`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Sales")

    # The VAT menu should appear *after* the Sales menu.  But Sales needs VAT
    # and therefore the VAT menu items will incorporate into the Sales menu.  One
    # possibility is to remove vat from the needs_plugins of trading.

    needs_plugins = [
        'lino.modlib.memo', 'lino_xl.lib.products', 'lino_xl.lib.vat'
    ]
    # needs_plugins = ['lino_xl.lib.products']

    print_items_table = "trading.ItemsByInvoicePrint"

    items_column_names = "product title unit_price qty discount_rate amount invoiceable *"
    columns_to_print = "invoiceable title unit_price qty amount"
    # print_items_column_names = "asset title unit_price qty amount"

    # out-of-the-box alternatives:
    # print_items_table = "trading.ItemsByInvoicePrintNoQtyColumn"

    subtotal_demo = False
    # a quick temporary option I created to avoid having to change 20 doctests

    # def pre_site_startup(self, site):
    #     if isinstance(self.print_items_column_names, str):
    #         self.print_items_column_names = self.print_items_column_names.split()
    #     super().pre_site_startup(site)

    def setup_reports_menu(self, site, user_type, m, ar=None):
        # mg = site.plugins.accounting
        mg = self
        # mg = site.plugins.vat
        m = m.add_menu(mg.app_label, mg.verbose_name)
        if site.is_installed("finan"):
            m.add_action('trading.DueInvoices')
        # m.add_action('trading.PrintableInvoicesByJournal')

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self
        # mg = site.plugins.vat
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('trading.PaperTypes')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self
        # mg = site.plugins.vat
        m = m.add_menu(mg.app_label, mg.verbose_name)
        # m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('trading.TradingRules')
        m.add_action('trading.Invoices')
        m.add_action('trading.InvoiceItems')

    def get_quicklinks(self):
        if self.site.get_plugin_setting('accounting', 'has_payment_methods'):
            yield 'trading.CashInvoice.start_new_sale'
