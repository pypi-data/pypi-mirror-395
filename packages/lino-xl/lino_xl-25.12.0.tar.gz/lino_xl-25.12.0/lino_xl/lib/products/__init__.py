# Copyright 2008-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds functionality for managing products.

See :doc:`/plugins/products`.

"""

from lino import ad, _


class Plugin(ad.Plugin):
    """The config descriptor for this plugin."""

    verbose_name = _("Products")
    needs_plugins = ['lino_xl.lib.xl']
    menu_group = 'products'
    price_selector = 'cal.EventType'
    barcode_driver = None
    barcodes_dir = None

    def prep_barcode_features(self, site):
        if self.barcode_driver:
            self.barcodes_dir = site.media_root / "barcodes"
            self.barcodes_dir.mkdir(parents=True, exist_ok=True)
    
    def on_initdb(self, site, force=False, verbosity=1):
        self.prep_barcode_features(site)
        super().on_initdb(site, force, verbosity)

    def before_analyze(self):
        self.prep_barcode_features(self.site)
        super().before_analyze()

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        # if site.is_installed('sales'):
        #     mg = site.plugins.sales
        # else:
        #     mg = self
        m = m.add_menu(mg.app_label, mg.verbose_name)
        for pt in site.models.products.ProductTypes.get_list_items():
            m.add_action(pt.table_name, label=pt.text)
        # m.add_action('products.Products')
        m.add_action('products.Categories')

        # mg = site.plugins.sales
        # m2 = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('products.PriceRules')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('products.PriceFactors')
        # m.add_action('products.ProductTypes')

    def get_requirements(self, site):
        if self.barcode_driver:
            yield "python-barcode"
