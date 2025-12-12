# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from django.conf import settings
from django.db import models

from lino.api import dd, rt, _
from lino.modlib.checkdata.choicelists import Checker
from lino_xl.lib.accounting.mixins import Matching, AccountVoucherItem, Payable
from lino_xl.lib.accounting.models import Voucher
from .choicelists import VatClasses, VatRegimes, VatColumns
# make them available for Menu.add_action
from .choicelists import VatAreas, VatRules, VatSubjectable
from .mixins import VatVoucher, VatItemBase
from .ui import *


class VatAccountInvoice(VatVoucher, Matching):

    class Meta:
        app_label = "vat"
        verbose_name = _("Ledger invoice")
        verbose_name_plural = _("Ledger invoices")
        # constraints = [
        #             models.UniqueConstraint(
        #                 fields=["journal", "fiscal_year", "number"],
        #                 name="vataccountinvoice_unique",
        #             ),
        #         ]

    # Override the field to change the text for the purchase invoice.
    your_ref = models.CharField(_("Provider's invoice number"),
                                max_length=200,
                                blank=True)

    # show_items = dd.ShowSlaveTable('vat.ItemsByInvoice', show_in_workflow=True)


dd.update_field(VatAccountInvoice, 'total_vat', editable=False)
dd.update_field(VatAccountInvoice, 'total_base', editable=False)


class InvoiceItem(AccountVoucherItem, VatItemBase):

    class Meta:
        app_label = 'vat'
        verbose_name = _("Ledger invoice item")
        verbose_name_plural = _("Ledger invoice items")

    voucher = dd.ForeignKey('vat.VatAccountInvoice', related_name='items')
    title = models.CharField(_("Description"), max_length=200, blank=True)

    def account_changed(self, ar):
        if self.account_id and self.account.vat_class:
            self.vat_class = self.account.vat_class


# if False:
#     """Install a post_init signal listener for each concrete subclass of
#     VatDocument.  The following trick worked...  but best is to store
#     it in VatRegime, not per voucher.
#
#     """
#
#     def set_default_item_vat(sender, instance=None, **kwargs):
#         instance.item_vat = settings.SITE.get_item_vat(instance)
#         # print("20130902 set_default_item_vat", instance)
#
#     @dd.receiver(dd.post_analyze)
#     def on_post_analyze(sender, **kw):
#         for m in rt.models_by_base(VatDocument):
#             dd.post_init.connect(set_default_item_vat, sender=m)
#             # print('20130902 on_post_analyze installed receiver for',m)

dd.inject_field('accounting.Movement', 'vat_regime',
                VatRegimes.field(blank=True))

dd.inject_field('accounting.Movement', 'vat_class',
                VatClasses.field(blank=True))

# dd.inject_field('accounting.Account',
#                 'vat_column',
#                 VatColumns.field(blank=True, null=True))


class VatColumnsChecker(Checker):
    # model = 'system.SiteConfig'

    verbose_name = _("Check VAT columns configuration")

    def get_checkdata_problems(self, ar, unused_obj, fix=False):
        for vc in VatColumns.get_list_items():
            ca = vc.common_account
            if ca is not None:
                obj = ca.get_object()
                if obj is None:
                    msg = _("No account defined as {} "
                            "(needed by VAT column {})").format(ca, vc.value)
                    yield (True, msg)
                    if fix:
                        obj = ca.create_object()
                        obj.vat_column = vc
                        obj.full_clean()
                        obj.save()
                elif obj.vat_column != vc:
                    msg = _("Account {} must have VAT column {}").format(
                        ca, vc.value)
                    yield (True, msg)
                    if fix:
                        obj.vat_column = vc
                        obj.full_clean()
                        obj.save()


VatColumnsChecker.activate()
