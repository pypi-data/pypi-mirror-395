# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db.models import Q, Sum

from lino import logger
from lino.api import dd, _
# from lino.utils.quantities import ZERO_DURATION
from lino.mixins import Sequenced
from lino_xl.lib.accounting.mixins import MovementBase, SequencedVoucherItem
from lino_xl.lib.accounting.mixins import LedgerRegistrable
from lino_xl.lib.accounting.models import Voucher
from lino_xl.lib.accounting.choicelists import VoucherStates
from lino_xl.lib.contacts.mixins import PartnerRelated
from lino_xl.lib.invoicing.mixins import InvoiceGenerator
from lino_xl.lib.invoicing.mixins import InvoicingTargetVoucher, InvoicingTargetItem
from lino_xl.lib.excerpts.mixins import Certifiable

from .mixins import StorageTransferer
from .choicelists import ProvisionStates
from .ui import *

NO_TRANSFER_RULE = "No transfer rule for {}. Available rules are {}"


class Movement(MovementBase):
    allow_cascaded_delete = ['voucher']

    class Meta:
        app_label = 'storage'
        verbose_name = _("Storage movement")
        verbose_name_plural = _("Storage movements")

    observable_period_prefix = 'voucher__'

    # provision_state = ProvisionStates.field()
    product = dd.ForeignKey('products.Product')
    qty = dd.QuantityField()
    amount = dd.PriceField(blank=True,
                           null=True,
                           max_digits=14,
                           decimal_places=2)

    @dd.virtualfield(dd.PriceField(_("Debit")),
                     sortable_by=['qty', 'value_date'])
    def debit(self, ar):
        return -self.qty if self.qty < 0 else None

    @dd.virtualfield(dd.PriceField(_("Credit")),
                     sortable_by=['-qty', 'value_date'])
    def credit(self, ar):
        return self.qty if self.qty > 0 else None

    @dd.chooser(simple_values=True)
    def match_choices(cls, partner, product):
        qs = cls.objects.filter(partner=partner,
                                product=product,
                                cleared=False)
        qs = qs.order_by('value_date')
        return qs.values_list('match', flat=True)

    def get_siblings(self):
        return self.voucher.storage_movement_set_by_voucher.all()
        #~ return self.__class__.objects.filter().order_by('seqno')


class Component(dd.Model):

    class Meta:
        app_label = 'storage'
        verbose_name = _("Component")
        verbose_name_plural = _("Components")

    parent = dd.ForeignKey("products.Product",
                           verbose_name=_("Parent"),
                           related_name="parents_by_component")
    child = dd.ForeignKey("products.Product",
                          verbose_name=_("Child"),
                          related_name="children_by_component")
    qty = dd.QuantityField(default=1)


class Provision(dd.Model):

    class Meta:
        app_label = 'storage'
        verbose_name = _("Provision")
        verbose_name_plural = _("Provisions")

    partner = dd.ForeignKey("contacts.Partner")
    product = dd.ForeignKey("products.Product")
    provision_state = ProvisionStates.field()
    qty = dd.QuantityField(max_length=dd.plugins.summaries.duration_max_length)

    def __str__(self):
        return "{partner} {qty} {product} {state}".format(
            state=self.provision_state.text,
            partner=self.partner,
            product=self.product,
            qty=self.qty)


class TransferRule(Sequenced):

    class Meta:
        app_label = 'storage'
        verbose_name = _("Transfer rule")
        verbose_name_plural = _("Transfer rules")

    journal = JournalRef()
    from_state = ProvisionStates.field(_("From"), blank=True, null=True)
    to_state = ProvisionStates.field(_("To"), blank=True, null=True)

    def __str__(self):
        return "{} : {} -> {}".format(self.journal.ref, self.from_state,
                                      self.to_state)

    @classmethod
    def find_source_state(cls, voucher):
        for tr in cls.objects.filter(journal=voucher.journal):
            if tr.from_state:
                return tr.from_state

    @classmethod
    def find_target_state(cls, voucher):
        for tr in cls.objects.filter(journal=voucher.journal):
            if tr.to_state:
                return tr.to_state


class DeliveryNote(Voucher, PartnerRelated, StorageTransferer,
                   LedgerRegistrable, InvoicingTargetVoucher, Certifiable):

    class Meta:
        app_label = 'storage'
        verbose_name = _("Delivery note")
        verbose_name_plural = _("Delivery notes")

    state = VoucherStates.field(default='draft')

    def get_print_language(self):
        return self.partner.language

    def get_provision(self, state, product, before=False):
        # called twice from storage/DeliveryNote/base.weasy.html
        # before: True to get the provision *before* this voucher, False to get
        # the provision *after* this voucher.

        ps = ProvisionStates.get_by_name(state)
        # from_journals = set([r.journal
        #     for r in TransferRule.objects.filter(from_state=ps)])
        # to_journals = set([r.journal
        #     for r in TransferRule.objects.filter(to_state=ps)])
        journals = set([
            r.journal for r in TransferRule.objects.filter(
                Q(from_state=ps) | Q(to_state=ps))
        ])
        qs = Movement.objects.filter(partner=self.partner,
                                     product=product,
                                     value_date__lte=self.voucher_date,
                                     voucher__journal__in=journals)
        # logger.debug("20240203 qty_from : %s", qs.query)
        if before:
            qs = qs.exclude(voucher=self)
        qty = product.delivery_unit.zero  # ZERO_DURATION
        for i in qs:
            qty += i.qty
        return qty
        # We can't use aggregate() because QuantityField is a CHAR for the db
        # return qs.aggregate(Sum("qty", default=float(),
        #     output_field=dd.DurationField()))['qty__sum']

    # def unused_get_wanted_movements(self, ar=None):
    #     # for mvt in super().get_wanted_movements(ar):
    #     #     yield mvt
    #     state = TransferRule.find_target_state(self)
    #     if state is None:
    #         raise Warning(NO_TRANSFER_RULE.format(
    #             self.journal, list(map(str, TransferRule.objects.all()))))
    #     for i in self.items.all():
    #         yield self.create_storage_movement(i, i.product, i.qty, state)
    #
    # def unused_create_storage_movement(self, item, product, qty, state, **kw):
    #     kw['voucher'] = self
    #     kw['provision_state'] = state
    #     kw['value_date'] = self.entry_date
    #     kw['product'] = product
    #     kw['amount'] = amount
    #     kw['qty'] = qty
    #
    #     # if account.clearable:
    #     #     kw.update(cleared=False)
    #     # else:
    #     #     kw.update(cleared=True)
    #     return rt.models.storage.Movement(**kw)


class DeliveryItem(SequencedVoucherItem, InvoicingTargetItem):
    """An item of an :class:`AccountInvoice`."""

    class Meta:
        app_label = 'storage'
        verbose_name = _("Delivery item")
        verbose_name_plural = _("Delivery items")

    voucher = dd.ForeignKey('storage.DeliveryNote', related_name='items')
    product = dd.ForeignKey('products.Product')
    qty = dd.QuantityField(_("Quantity"),
                           blank=True,
                           null=True,
                           max_length=dd.plugins.summaries.duration_max_length)


# InvoicingAreas.add_item('reporting', _("Reporting"), 'reporting',
#     voucher_model=DeliveryNote, voucher_item=DeliveryItem,
#     max_date_offset=1, today_offset=1)


class Filler(PartnerRelated, InvoiceGenerator):

    class Meta:
        app_label = 'storage'
        abstract = dd.is_abstract_model(__name__, 'Filler')
        verbose_name = _("Storage filler")
        verbose_name_plural = _('Storage fillers')
        unique_together = ['partner', 'provision_state', 'provision_product']

    hide_editable_number = False
    # target_invoicing_area = 'default'
    target_voucher_model = "trading.VatProductInvoice"

    provision_state = ProvisionStates.field(blank=True, null=True)
    provision_product = dd.ForeignKey('products.Product',
                                      verbose_name=_("Wanted product"),
                                      related_name="pprods_by_filler")
    # filler_min = dd.QuantityField(_("Minimum quantity"))
    min_asset = dd.QuantityField(_("Minimum asset"))
    fill_asset = dd.QuantityField(_("Fill asset"))

    # filler_product = dd.ForeignKey('products.Product',
    #     verbose_name=_("Provision filler"),
    #     blank=True, null=True, related_name="fprods_by_filler")

    def __str__(self):
        return "Filler {} {} {}".format(self.partner, self.provision_state,
                                        self.provision_product)

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        qs = super().get_generators_for_plan(plan, partner)
        p = partner or plan.partner
        if p:
            qs = qs.filter(partner=p)
        # print("20230620 get_generators_for_plan()", qs)
        return qs

    def get_invoiceable_partner(self):
        return self.get_partner()

    def get_invoiceable_product(self, max_date=None):
        return self.provision_product

    def get_invoiceable_qty(self):
        return self.default_invoiceable_qty

    def get_invoiceable_end_date(self):
        return None

    def get_wanted_invoice_items(self, info, invoice, ar):
        # dd.logger.info("20230622 get_wanted_invoice_items() %s", self)
        for i in super().get_wanted_invoice_items(info, invoice, ar):
            # print("20210731 a", i)
            yield i

        qs = rt.models.storage.Provision.objects.filter(
            partner=self.partner,
            provision_state=self.provision_state,
            product=self.provision_product)
        assert qs.count() <= 1
        # if qs.count() > 1:
        #     raise Exception(
        #         "20230623 Multiple storage provisions: {}".format(qs))
        prov = qs.last()
        if prov is None:
            ok = True
            qty = self.fill_asset
        else:
            ok = False
            if prov.qty < self.min_asset:
                ok = True
            qty = self.fill_asset - prov.qty
            # print("20230623 {} : {} < {} -> {}".format(
            #     self.partner, prov.qty, self.min_asset, ok))
        if ok:
            yield invoice.add_voucher_item(title=str(self))
            kwargs = dict(product=self.provision_product, qty=qty)
            i = invoice.add_voucher_item(**kwargs)
            i.product_changed(ar)
            # i.reset_totals(ar)
            # if i.total_incl is None:
            #     print("20210731 invoice item without amount:", i.__class__, i)
            yield i
        # else:
        #     print("20230622 has {} but needs {}".format(
        #         prov.qty, self.min_asset))


Filler.set_widget_options('min_asset', hide_sum=True)
Filler.set_widget_options('fill_asset', hide_sum=True)
