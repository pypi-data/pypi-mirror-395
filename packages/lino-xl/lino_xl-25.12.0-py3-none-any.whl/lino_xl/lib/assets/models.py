# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino_xl.lib.invoicing.mixins import InvoiceGenerator


assets = dd.plugins.assets


class PartnerAsset(InvoiceGenerator):

    class Meta:
        app_label = 'assets'
        verbose_name = assets.asset_name
        verbose_name_plural = assets.asset_name_plural
        abstract = dd.is_abstract_model(__name__, 'PartnerAsset')
        ordering = ["partner", "name"]
        unique_together = ("partner", "name")

    partner = dd.ForeignKey(assets.partner_model, blank=True, null=True)
    name = dd.CharField(_("Designation"), blank=True, max_length=200)
    # name = dd.CharField(assets.asset_name_short, blank=True, max_length=200)

    def __str__(self):
        return self.name

    @classmethod
    def create_invoiceable_choice(cls, item, text, ar):
        return cls.lookup_or_create('name', text, partner=item.voucher.partner)

    def get_invoiceable_end_date(self):
        return None


class PartnerAssets(dd.Table):
    model = 'assets.PartnerAsset'
    required_roles = dd.login_required(dd.SiteStaff)
    column_names = 'partner name *'
    # order_by = ["ref", "partner", "designation"]

    insert_layout = """
    name
    """

    # detail_layout = """
    # id name
    # partner
    # """


class AssetsByPartner(PartnerAssets):
    master_key = 'partner'
    column_names = 'name *'
