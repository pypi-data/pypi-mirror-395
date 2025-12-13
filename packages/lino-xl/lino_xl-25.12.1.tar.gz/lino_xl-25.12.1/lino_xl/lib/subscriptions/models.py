# -*- coding: UTF-8 -*-
# Copyright 2019-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# TODO: maybe subscriptions shouldn't even be in a journal.

from html import escape
# from decimal import Decimal
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.utils.text import format_lazy

from lino.api import dd, rt
from lino.utils import ONE_DAY
from lino.mixins.ref import Referrable
from lino.mixins.clonable import Clonable
from lino.mixins.periods import DateRange
from lino.mixins.periods import rangefmt
from lino_xl.lib.accounting.choicelists import VoucherStates
from lino_xl.lib.excerpts.mixins import Certifiable
from lino_xl.lib.excerpts.mixins import ExcerptTitle
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.uploads.mixins import UploadController
from lino.modlib.printing.mixins import Printable
# from lino.modlib.printing.utils import PrintableObject
from lino.modlib.summaries.mixins import Summarized
# from lino_xl.lib.cal.mixins import Reservation
from lino_xl.lib.cal.utils import day_and_month
from lino_xl.lib.cal.mixins import EventGenerator
from lino_xl.lib.invoicing.mixins import InvoiceGenerator, Periodicities
from lino_xl.lib.contacts.mixins import PartnerRelated
from lino_xl.lib.accounting.models import Voucher
from lino_xl.lib.accounting.mixins import SequencedVoucherItem, LedgerRegistrable
from lino_xl.lib.trading.mixins import TradingPrintable, TradingVoucherItem
from lino_xl.lib.excerpts.mixins import Certifiable
# from lino_xl.lib.storage.mixins import ProvisionFiller
from .ui import *


class Subscription(Voucher, LedgerRegistrable, PartnerRelated, TradingPrintable,
                   DateRange, Clonable, Referrable, Summarized):

    class Meta:
        app_label = 'subscriptions'
        abstract = dd.is_abstract_model(__name__, 'Subscription')
        verbose_name = _("Subscription")
        verbose_name_plural = _('Subscriptions')

    hide_editable_number = False

    quick_search_fields = "ref subject"

    state = VoucherStates.field(default='draft')
    # subject = models.CharField(_("Our reference"), max_length=200, blank=True)
    # description = dd.TextField(_("Description"), blank=True)
    # start_date = models.DateField(_("Start date"), blank=True, null=True)
    # end_date = models.DateField(_("End date"), blank=True, null=True)
    subscription_periodicity = Periodicities.field(blank=True, null=True)
    invoiceable_product = dd.ForeignKey('products.Product',
                                        blank=True,
                                        null=True)

    # def full_clean(self, *args, **kwargs):
    #     # if self.entry_date is None:
    #     #     self.entry_date = dd.today()
    #     if self.partner is None:
    #         raise Warning(_("Either company or person must be given."))
    #     super().full_clean(*args, **kwargs)

    def __str__(self):
        s = super().__str__()
        if self.ref:
            return "{} ({})".format(s, self.ref)
        if p := self.company or self.person:
            return "{} ({})".format(s, p)
        return s

    def get_wanted_movements(self, ar=None):
        return []

    def get_invoiceable_partner(self):
        return self.partner

    def compute_summary_values(self):
        if self.state == VoucherStates.draft:
            return
        sp = self.subscription_periodicity
        if sp is None:
            return
        add_duration = sp.renew_unit.add_duration
        renew_before = timedelta(days=sp.renew_before)
        start_date = self.start_date
        # get the last existing subscription period
        qs = SubscriptionPeriod.objects.filter(master=self)
        last_sp = qs.order_by('end_date').last()
        if last_sp is not None:
            # When there is at least one period, potential next
            # period starts one day after
            start_date = last_sp.end_date + ONE_DAY
        end_date = add_duration(start_date, sp.renew_every) - ONE_DAY
        while start_date - renew_before < dd.today():
            # print("20230630 {} compute_summary_values() {}-{}".format(
            #     self, start_date, end_date))
            if self.end_date:
                if start_date > self.end_date:
                    return
                if end_date > self.end_date:
                    end_date = self.end_date
            kw = dict(master=self, start_date=start_date, end_date=end_date)
            obj = SubscriptionPeriod(**kw)
            obj.full_clean()
            obj.save()
            start_date = add_duration(start_date, sp.renew_every)
            end_date = add_duration(start_date, sp.renew_every) - ONE_DAY

        # lsp = SubscriptionPeriod.objects.filter(
        #     master=self).order_by('start_date').last()
        # if lsp is None:
        #     obj = SubscriptionPeriod(master=self, start_date=self.start_date)
        #     obj.full_clean()
        #     obj.save()
        #     return
        # if lsp.invoice is None:
        #     return
        # assert lsp.end_date is not None
        # obj = SubscriptionPeriod(master=self, start_date=lsp.end_date+ONE_DAY)
        # obj.full_clean()
        # obj.save()


# dd.update_field(Subscription, "ref", verbose_name=_("Nickname"))


class SubscriptionItem(SequencedVoucherItem):

    class Meta:
        app_label = 'subscriptions'
        abstract = dd.is_abstract_model(__name__, 'SubscriptionItem')
        verbose_name = _("Subscription item")
        verbose_name_plural = _("Subscription items")

    allow_cascaded_delete = 'voucher'

    voucher = dd.ForeignKey('subscriptions.Subscription', related_name='items')
    product = dd.ForeignKey('products.Product', blank=True, null=True)
    qty = dd.QuantityField(_("Quantity"), blank=True, null=True)
    discount = dd.PercentageField(_("Discount"), blank=True, null=True)
    unit_price = dd.PriceField(_("Unit price"), blank=True, null=True)
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    def as_paragraph(self, ar, **kwargs):
        if ar is None:
            return str(self)
        if ar.is_obvious_field('voucher'):
            rv = "({}) ".format(ar.obj2htmls(self, str(self.seqno)))
        else:
            rv = "({}) ".format(
                ar.obj2htmls(self.voucher.get_mti_leaf(), str(self)))
        rv += ar.obj2htmls(self.product)
        if self.qty:
            rv += " {}&nbsp;{} ".format(
                escape(str(self.qty)),
                escape(str(self.product.delivery_unit or "x")))
        if self.unit_price:
            rv += _(" à {} {}").format(
                self.unit_price, escape(dd.plugins.accounting.currency_symbol))
        if self.remark:
            rv += " ({})".format(escape(self.remark))
        return rv


class SubscriptionPeriod(DateRange, InvoiceGenerator):

    class Meta:
        app_label = 'subscriptions'
        abstract = dd.is_abstract_model(__name__, 'Subscription')
        verbose_name = _("Subscription period")
        verbose_name_plural = _('Subscription periods')

    # target_invoicing_area = 'subscriptions'
    target_voucher_model = "trading.VatProductInvoice"

    master = dd.ForeignKey(Subscription, related_name="periods_by_master")

    must_invoice = models.BooleanField(_("Must invoice"), default=True)

    # invoice = dd.ForeignKey(
    #     'accounting.Voucher',
    #     verbose_name=_("Invoice"),
    #     null=True, blank=True,
    #     on_delete=models.SET_NULL)

    def full_clean(self):
        super().full_clean()
        info = self.compute_invoicing_info(None, dd.today())
        if info.invoiceable_product is None:
            self.must_invoice = False
        else:
            self.must_invoice = True
            # self.save()

    def after_invoicing(self, ar, invoice):
        self.full_clean()

    def __str__(self):
        # return "{} {}".format(self.master, self.get_period_text())
        return _("{} in {}").format(rangefmt((self.start_date, self.end_date)),
                                    self.master)

    def get_invoiceable_partner(self):
        return self.master.partner

    def get_invoiceable_end_date(self):
        return self.end_date

    @classmethod
    def get_partner_filter_field(cls, partner):
        return "master__" + Subscription.get_partner_filter_field(partner)

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        # dd.logger.info("20240107 get_generators_for_plan() %s", cls)
        # pre-select which subscriptions may potentially generate an invoice for
        # the given plan.

        qs = super().get_generators_for_plan(plan, partner)

        # if plan.invoicing_area is None:
        #     raise Exception("20221217")

        qs = qs.filter(must_invoice=True)

        max_date = plan.get_max_date()
        if max_date:
            qs = qs.filter(start_date__lte=max_date)
        if plan.min_date:
            qs = qs.filter(start_date__gte=plan.min_date)

        if plan.order is None:
            qs = qs.exclude(master__state=VoucherStates.cancelled)
            qs = qs.exclude(master__state=VoucherStates.draft)
        elif issubclass(dd.plugins.invoicing.order_model, Subscription):
            qs = qs.filter(master_id=plan.order.id)
        else:
            raise Exception("20210731 {}".format(
                dd.plugins.invoicing.order_model))

        if partner is None:
            partner = plan.partner

        if partner is not None:
            fldname = cls.get_partner_filter_field(partner)
            qs = cls.filter_by_invoice_recipient(qs, partner, fldname)

        # dd.logger.info("20240107 %s (%d rows)", qs.query, qs.count())
        return qs.order_by('id')

    # def get_wanted_invoice_items(self, info, invoice, ar):
    #     # dd.logger.info("20181116a %s", self)
    #     # print("20221222 get_wanted_invoice_items()", self.items.all())
    #     if info.asset_to_buy is not None:
    #         kwargs = dict(
    #             # 20210804 invoiceable=self,
    #             product=self.get_invoiceable_product(self.entry_date),
    #             unit_price=self.total_base)
    #         i = invoice.add_voucher_item(**kwargs)
    #         i.product_changed(ar)
    #         i.unit_price_changed(ar)
    #         # i.reset_totals(ar)
    #         if i.total_incl is None:
    #             raise Exception("20210731 invoice item without amount:", i.__class__, i)
    #         yield i

    def get_wanted_invoice_items(self, info, invoice, ar):
        # dd.logger.info("20181116a %s", self)
        # print("20230630 get_wanted_invoice_items()", self.master.items.all())
        # if info.asset_to_buy is None:
        #     return
        sp = self.master.subscription_periodicity
        if sp is None:
            return
        # for i in super().get_wanted_invoice_items(info, invoice, ar):
        #     # print("20210731 a", i)
        #     yield i
        # print("20230710 gonna yield", self.get_invoiceable_product())
        yield invoice.add_voucher_item(title=str(self),
                                       product=self.get_invoiceable_product())
        # print("20221222 asset_to_buy is", info.number_of_events, info.asset_to_buy)
        # if info.number_of_events is None:
        for oi in self.master.items.all():
            kwargs = dict(
                # 20210804 invoiceable=self,
                product=oi.product,
                discount_rate=oi.discount,
                unit_price=oi.unit_price,
                qty=oi.qty)
            i = invoice.add_voucher_item(**kwargs)
            i.product_changed(ar)
            # i.reset_totals(ar)
            # if i.total_incl is None:
            #     print("20210731 invoice item without amount:", i.__class__, i)
            yield i

    def get_invoiceable_product(self, max_date=None):
        return self.master.invoiceable_product

    # def get_invoiceable_qty(self):
    #     return self.default_invoiceable_qty

    # def get_invoicing_pass_type(self, product=None):
    #     if product is not None:
    #         return product.tariff
    #     return None

    # def get_invoiceable_start_date(self, max_date):
    #     return self.start_date
    #
    # def get_invoiceable_end_date(self):
    #     return self.end_date
    #
    # def get_invoicing_periodicity(self, product):
    #     return self.subscription_periodicity

    # def get_invoiceable_title(self, number=None):
    #     return str(self)
