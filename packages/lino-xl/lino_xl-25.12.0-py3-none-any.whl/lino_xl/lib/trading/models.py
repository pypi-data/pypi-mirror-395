# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.utils.html import format_html, mark_safe
# from django.core.exceptions import ValidationError

from lino.utils.html import E, tostring
from lino.utils.mldbc.mixins import BabelNamed
from lino.mixins.ref import Referrable
from lino_xl.lib.accounting.mixins import Matching, SequencedVoucherItem
from lino_xl.lib.accounting.choicelists import TradeTypes
from lino_xl.lib.invoicing.mixins import InvoiceGenerator
from lino_xl.lib.invoicing.mixins import InvoicingTargetVoucher, InvoicingTargetItem
from lino_xl.lib.storage.mixins import StorageTransferer
from lino_xl.lib.peppol.mixins import PeppolSendable
# from lino_xl.lib.invoicing.mixins import InvoicingAreas
from lino.api import dd, rt, _
from .mixins import TradingVoucher, TradingVoucherItem
# from .actions import WriteElectronicInvoice
from .ui import *

has_payment_methods = dd.get_plugin_setting('accounting', 'has_payment_methods',
                                            False)
has_purchases = dd.get_plugin_setting('accounting', 'has_purchases', False)

TradeTypes.sales.update(price_field_name='sales_price',
                        price_field_label=_("Sales price"),
                        base_account_field_name='sales_account',
                        base_account_field_label=_("Sales account"))

if has_purchases:
    TradeTypes.purchases.update(
        price_field_name='purchases_price',
        price_field_label=_("Purchases price"),
        base_account_field_name='purchases_account',
        base_account_field_label=_("Purchases account"))


class PaperType(Referrable):

    templates_group = 'trading/VatProductInvoice'

    class Meta:
        app_label = 'trading'
        abstract = dd.is_abstract_model(__name__, 'PaperType')
        verbose_name = _("Paper type")
        verbose_name_plural = _("Paper types")

    designation = models.CharField(_("Designation"), max_length=200, blank=True)
    template = models.CharField(_("Template"), max_length=200, blank=True)
    columns_to_print = models.CharField(
        _("Columns to print"), max_length=200, blank=True)

    def __str__(self):
        return self.designation or super()._str__()

    @dd.chooser(simple_values=True)
    def template_choices(cls):
        bm = rt.models.printing.BuildMethods.get_system_default()
        return rt.find_template_config_files(bm.template_ext,
                                             cls.templates_group)


class TradingRule(dd.Model):

    class Meta:
        app_label = 'trading'
        abstract = dd.is_abstract_model(__name__, 'TradingRule')
        verbose_name = _("Trading rule")
        verbose_name_plural = _("Trading rules")

    allow_cascaded_delete = 'partner'

    partner = dd.ForeignKey(
        'contacts.Partner', blank=True, null=True,
        related_name='tradingrules_by_partner')
    trade_type = TradeTypes.field()
    invoice_recipient = dd.ForeignKey('contacts.Partner',
                                      verbose_name=_("Invoicing address"),
                                      related_name='tradingrules_by_recipient',
                                      blank=True,
                                      null=True)
    payment_term = dd.ForeignKey(
        'accounting.PaymentTerm', blank=True, null=True,
        help_text=_("The default payment term for invoices to this partner."))

    paper_type = dd.ForeignKey('trading.PaperType', null=True, blank=True)


class VatProductInvoice(TradingVoucher, Matching, InvoicingTargetVoucher,
                        StorageTransferer, PeppolSendable):
    # edit_totals = True
    quick_search_fields = "partner__name subject"

    class Meta:
        app_label = 'trading'
        abstract = dd.is_abstract_model(__name__, 'VatProductInvoice')
        verbose_name = _("Trading invoice")
        verbose_name_plural = _("Trading invoices")

    # write_xml = WriteElectronicInvoice()

    # show_items = dd.ShowSlaveTable('trading.ItemsByInvoice')

    # make_copy = MakeCopy()

    # def register_voucher(self, ar=None, do_clear=None):
    #     super().register_voucher(ar, do_clear)
    #     if self.payment_method is None:
    #         self.payment_method = self.get_default_payment_method(ar)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        yield 'due_date'
        yield 'voucher_date'
        yield 'entry_date'
        yield 'user'
        # yield 'item_vat'

    def make_xml_file(self, ar):
        # ar.info("Send %s", self)
        self.do_print.run_from_ui(ar)
        return super().make_xml_file(ar)

    # def report_assets(self):
    #     # Whether to print a column "Asset" in invoices
    #     if dd.is_installed('assets'):
    #         qs = rt.models.assets.PartnerAsset.objects.filter(partner=self.partner)
    #         return qs.exists()

    def get_print_items(self, ar):
        # used by appy_pod
        dv = rt.models.resolve(dd.plugins.trading.print_items_table)
        return dv.create_request(self)

    @dd.virtualfield(dd.PriceField(_("Balance before")))
    def balance_before(self, ar):
        if self.id is None:
            # RemovedInDjango50Warning:  Passing unsaved model instances to
            # related filters is deprecated.
            return None
        Movement = rt.models.accounting.Movement
        qs = Movement.objects.filter(partner=self.get_partner(),
                                     cleared=False,
                                     value_date__lte=self.entry_date)
        qs = qs.exclude(voucher=self)
        # qs = qs.exclude(match=self.get_match())
        return Movement.get_balance(self.journal.dc.opposite(), qs)

    @dd.virtualfield(dd.PriceField(_("This voucher")))
    def voucher_movements(self, ar):
        if self.id is None:
            # RemovedInDjango50Warning:  Passing unsaved model instances to
            # related filters is deprecated.
            return None
        Movement = rt.models.accounting.Movement
        qs = Movement.objects.filter(partner=self.get_partner(),
                                     cleared=False,
                                     voucher=self)
        return Movement.get_balance(self.journal.dc.opposite(), qs)

    @dd.virtualfield(dd.PriceField(_("Balance to pay")))
    def balance_to_pay(self, ar):
        Movement = rt.models.accounting.Movement
        qs = Movement.objects.filter(partner=self.get_partner(),
                                     value_date__lte=self.entry_date,
                                     cleared=False)
        return Movement.get_balance(self.journal.dc.opposite(), qs)


if has_payment_methods:

    class StartNewSale(dd.Action):
        label = _("Start new sale")
        show_in_toolbar = False

        def get_action_permission(self, ar, obj, state):
            if ar.get_user().sales_journal is None:
                return False
            return super().get_action_permission(ar, obj, state)

        def run_from_ui(self, ar):
            journal = ar.get_user().sales_journal
            instance = journal.voucher_type.table_class.create_instance(
                ar, journal=journal, partner=journal.partner)
            instance.full_clean()
            instance.save_new_instance(ar)
            ar.goto_instance(instance)

    class CashInvoice(VatProductInvoice):

        class Meta:
            app_label = 'trading'
            abstract = dd.is_abstract_model(__name__, 'CashInvoice')
            verbose_name = _("Cash invoice")
            verbose_name_plural = _("Cash invoices")

        cash_received = dd.PriceField(_("Cash received"),
                                      blank=True,
                                      null=True)
        cash_returned = dd.PriceField(_("Cash returned"),
                                      blank=True,
                                      null=True)

        start_new_sale = StartNewSale()

        def cash_received_changed(self, ar):
            self.cash_returned = self.cash_received - self.total_incl

        @dd.displayfield(_("Cash to return"))
        def cash_to_return(self, ar):
            if self.payment_method.is_cash:
                if self.total_incl and self.cash_received:
                    if self.cash_received >= self.total_incl:
                        return self.cash_received - self.total_incl

        def get_wanted_movements(self, ar=None):
            for mvt in super().get_wanted_movements(ar):
                yield mvt
            if self.payment_method.payment_account is None:
                return
            if self.payment_method.is_cash:
                amount = self.cash_received - self.cash_returned
            else:
                amount = self.total_incl
            tt = self.get_trade_type()
            if self.partner is None:
                acc = tt.get_base_account(ar)
            else:
                acc = tt.get_main_account(ar)
                # acc = tt.get_partner_invoice_account(self.partner)
            if acc is None:
                raise Exception("20220706 acc is None {} {}".format(
                    self.partner, tt))
            prj = None
            yield self.create_ledger_movement(None, (acc, None),
                                              prj,
                                              amount,
                                              partner=self.partner,
                                              match=self.get_match())
            yield self.create_ledger_movement(
                None, (self.payment_method.payment_account, None),
                prj,
                -amount,
                partner=self.partner,
                match=self.get_match())

            # sums_dict.collect(
            #     ((acc, None), self.project, None, None),
            #     cash_amount)
            #     sums_dict.collect(
            #         ((self.payment_method.payment_account, None), self.project, None, None),
            #         -amount)
            # return sums_dict

    dd.inject_field(
        'users.User', 'sales_journal',
        dd.ForeignKey('accounting.Journal',
                      on_delete=models.SET_NULL,
                      null=True,
                      blank=True,
                      verbose_name=_("Sales journal")))

else:
    dd.inject_field('users.User', 'sales_journal', dd.DummyField())


class InvoiceItem(TradingVoucherItem, SequencedVoucherItem, InvoiceGenerator,
                  InvoicingTargetItem):

    class Meta:
        app_label = 'trading'
        abstract = dd.is_abstract_model(__name__, 'InvoiceItem')
        verbose_name = _("Trading invoice item")
        verbose_name_plural = _("Trading invoice items")

    voucher = dd.ForeignKey('trading.VatProductInvoice', related_name='items')
    # asset = dd.ForeignKey(
    #     'assets.PartnerAsset', blank=True, null=True, related_name='trading_items')
    # ship_ref = models.CharField(
    #     _("Shipment reference"), max_length=200, blank=True)
    # ship_date = models.DateField(_("Shipment date"), blank=True, null=True)

    master_data_fields = {'total_incl', 'total_base'}

    @classmethod
    def get_partner_filter_field(cls, partner):
        return "voucher__" + VatProductInvoice.get_partner_filter_field(
            partner)

    def get_parent_links(self, ar):
        sar = rt.models.trading.InvoicesByJournal.create_request(
            parent=ar, master_instance=self.voucher.journal)
        yield sar.obj2htmls(self.voucher)

    # @dd.chooser()
    # def asset_choices(cls, voucher):
    #     return rt.models.assets.PartnerAsset.objects.filter(
    #         partner=voucher.partner)
    #
    # def create_asset_choice(self, text, ar=None):
    #     """
    #     Called when an unknown asset name was given.
    #
    #     This is a create_FOO_choice method, which causes
    #     the asset field to be :ref:`learning <learning_combos>`.
    #
    #     """
    #     if self.voucher is None:
    #         raise ValidationError(
    #             "Cannot auto-create asset %r if voucher is empty", text)
    #     return rt.models.assets.PartnerAsset.lookup_or_create(
    #         'name', text, partner=self.voucher.partner)
    #
    # @classmethod
    # def override_column_headers(cls, ar, **headers):
    #     if (s := dd.get_plugin_setting('assets', 'asset_name_short', None)) is not None:
    #         headers['asset'] = s
    #     return super().override_column_headers(ar, **headers)

    def get_master_data(self, ar, master_instance=None):
        if ar.master_instance.edit_totals:
            ar.master_instance.compute_totals()
        ar.master_instance.full_clean()
        ar.master_instance.save()
        return super().get_master_data(ar)

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        jnls = set(plan.invoicing_task.get_source_journals())
        if len(jnls) == 0:
            return cls.objects.none()

        # jnls = [o.source_journal
        #     for o in rt.models.invoicing.FollowUpRule.objects.filter(
        #         source_journal=plan.invoicing_area.source_journal)]
        # jnls = [o.source_journal
        #     for o in rt.models.invoicing.FollowUpRule.objects.filter(
        #         invoicing_area=plan.invoicing_area)]
        # qs = cls.objects.filter(voucher__journal__in=plan.invoicing_area.get_source_journals())
        qs = cls.objects.filter(voucher__journal__in=jnls)
        if plan.order_id:
            qs = qs.filter(asset_id=plan.order_id)
        if partner is not None:
            # qs = qs.filter(voucher__partner=partner)
            fldname = cls.get_partner_filter_field(partner)
            qs = cls.filter_by_invoice_recipient(qs, partner, fldname)
        return qs

        # trs = rt.models.invoicing.FollowUpRule.objects.filter(
        #     source_journal=plan.area.journal)
        # if trs.exist():
        # jnls = []
        # for tr in trs:
        #     trs = trs.filter(from_state=)
        #     tr.from_state
        #     qs = cls.objects.filter(voucher__journal__in=jnls)
        #     yield qs

    def get_invoiceable_product(self, max_date=None):
        # if self.product and self.product.subtotal:
        return self.product

    def get_invoiceable_qty(self):
        return self.qty

    def get_invoiceable_title(self, number=None):
        return self.title

    def get_invoiceable_end_date(self):
        return None

    # def get_invoiceable_start_date(self, max_date):
    #     # don't look at events before this date.
    #     return None
    #
    def get_invoiceable_events(self, start_date, max_date):
        return []

    def get_invoiceable_free_events(self):
        return 0

    def get_invoiceable_partner(self):
        return self.voucher.partner

    def get_invoiceable_payment_term(self):
        return None

    def get_invoiceable_paper_type(self):
        return None

    # def setup_invoice_from_suggestion(self, invoice, plan, info):
    #     if info.invoicing_max_date is not None:
    #         invoice.invoicing_min_date = info.invoicing_min_date
    #         invoice.invoicing_max_date = info.invoicing_max_date
    #     else:
    #         invoice.invoicing_min_date = plan.min_date
    #         invoice.invoicing_max_date = plan.get_max_date()

    def setup_invoice_item(self, item):
        pass

    def as_paragraph(self, ar, **kwargs):
        text = format_html("{}) {}", self.seqno, self.title)
        s = ar.obj2htmls(self, text)  # "↗"
        s += mark_safe(" &mdash;")
        # if self.product_id is not None:
        #     s += format_html(
        #         _(" ({product})"), product=ar.obj2htmls(self.product))
        if self.qty is None or self.unit_price is None:
            total_intro = _("for")
        else:
            total_intro = "="
            if self.product.delivery_unit is None:
                s += format_html(
                    _(" {} x {}"), self.qty, dd.format_currency(self.unit_price))
            else:
                s += format_html(
                    _(" {} {} à {}"),
                    self.qty, self.product.delivery_unit.text,
                    dd.format_currency(self.unit_price))
        if self.discount_rate is not None:
            s += format_html(_(" - {}%"), self.discount_rate)
        if self.discount_amount is not None:
            s += format_html(_(" - {}"), dd.format_currency(self.discount_amount))
        if self.total_vat:
            if dd.plugins.vat.item_vat:
                s += format_html(
                    _(" {} {} ({} + VAT {})"),
                    total_intro, dd.format_currency(self.total_incl),
                    dd.format_currency(self.total_base),
                    dd.format_currency(self.total_vat))
            else:
                s += format_html(
                    _(" {} {} + VAT {} = {}"),
                    total_intro, dd.format_currency(self.total_base),
                    dd.format_currency(self.total_vat),
                    dd.format_currency(self.total_incl))
        elif self.total_base:
            s += format_html(
                _(" {} {}"), total_intro, dd.format_currency(self.total_base))
        if self.description:
            s += format_html("<br/>{}", self.description)
        return mark_safe(s)


# InvoicingAreas.add_item('sales', _("Invoicing"), 'default',
#     voucher_model=VatProductInvoice, voucher_item=InvoiceItem)
