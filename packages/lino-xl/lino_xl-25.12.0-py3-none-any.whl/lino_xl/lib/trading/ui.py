# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core import actions
from lino.core import constants
from lino.utils.html import E
from lino.modlib.memo.mixins import body_subject_to_elems
from lino_xl.lib.accounting.choicelists import VoucherTypes
from lino_xl.lib.accounting.ui import PartnerVouchers, ByJournal, PrintableByJournal
from lino_xl.lib.accounting.roles import LedgerStaff, LedgerUser
from lino_xl.lib.invoicing.ui import InvoicingsByGenerator
from lino.api import dd, rt, _


class PaperTypes(dd.Table):
    model = 'trading.PaperType'
    required_roles = dd.login_required(LedgerStaff)
    column_names = 'ref designation template columns_to_print *'


class TradingRules(dd.Table):
    model = 'trading.TradingRule'
    required_roles = dd.login_required(LedgerStaff)
    default_display_modes = {None: constants.DISPLAY_MODE_GRID}
    detail_layout = dd.DetailLayout("""
    partner trade_type
    invoice_recipient
    paper_type
    payment_term
    """, window_size=(40, 'auto'))


class RulesByPartner(TradingRules):
    master_key = 'partner'
    button_text = "ir"
    required_roles = dd.login_required(LedgerUser)
    column_names = "trade_type invoice_recipient paper_type payment_term * "
    window_size = (80, 20)


class PartnersByInvoiceRecipient(TradingRules):
    help_text = _("Show partners having this as invoice recipient.")
    details_of_master_template = _("%(master)s used as invoice recipient")
    button_text = "♚"  # 265A
    master_key = 'invoice_recipient'
    column_names = "partner partner__id partner__address_column *"
    window_size = (80, 20)


# class TradingVouchers(PartnerVouchers):
#     pass


# class MakeCopy(dd.Action):
#     button_text = u"\u2042"  # ASTERISM (⁂)

#     label = _("Make copy")
#     show_in_workflow = True
#     show_in_toolbar = False
#     copy_item_fields = set('product total_incl unit_price qty'.split())

#     parameters = dict(
#         partner=dd.ForeignKey('contacts.Partner'),
#         product=dd.ForeignKey('products.Product', blank=True),
#         subject=models.CharField(
#             _("Subject"), max_length=200, blank=True),
#         your_ref=models.CharField(
#             _("Your ref"), max_length=200, blank=True),
#         entry_date=models.DateField(_("Entry date")),
#         total_incl=dd.PriceField(_("Total incl VAT"), blank=True),
#     )
#     params_layout = """
#     entry_date partner
#     your_ref
#     subject
#     product total_incl
#     """

#     def action_param_defaults(self, ar, obj, **kw):
#         kw = super(MakeCopy, self).action_param_defaults(ar, obj, **kw)
#         kw.update(your_ref=obj.your_ref)
#         kw.update(subject=obj.subject)
#         kw.update(entry_date=obj.entry_date)
#         kw.update(partner=obj.partner)
#         # qs = obj.items.all()
#         # if qs.count():
#         #     kw.update(product=qs[0].product)
#         # kw.update(total_incl=obj.total_incl)
#         return kw

#     def run_from_ui(self, ar, **kw):
#         VoucherStates = rt.models.accounting.VoucherStates
#         obj = ar.selected_rows[0]
#         pv = ar.action_param_values
#         kw = dict(
#             journal=obj.journal,
#             user=ar.get_user(),
#             partner=pv.partner, entry_date=pv.entry_date,
#             subject=pv.subject,
#             your_ref=pv.your_ref)

#         new = obj.__class__(**kw)
#         new.fill_defaults()
#         new.full_clean()
#         new.save()
#         if pv.total_incl:
#             if not pv.product:
#                 qs = obj.items.all()
#                 if qs.count():
#                     pv.product = qs[0].product
#             item = new.add_voucher_item(
#                 total_incl=pv.total_incl, product=pv.product)
#             item.total_incl_changed(ar)
#             item.full_clean()
#             item.save()
#         else:
#             for olditem in obj.items.all():
#                 # ikw = dict()
#                 # for k in self.copy_item_fields:
#                 #     ikw[k] = getattr(olditem, k)
#                 ikw = { k: getattr(olditem, k)
#                         for k in self.copy_item_fields}
#                 item = new.add_voucher_item(**ikw)
#                 item.total_incl_changed(ar)
#                 item.full_clean()
#                 item.save()

#         new.full_clean()
#         new.register_voucher(ar)
#         new.state = VoucherStates.registered
#         new.save()
#         ar.goto_instance(new)
#         ar.success()


class InvoiceDetail(dd.DetailLayout):
    main = "general more accounting storage"

    general = dd.Panel("""
    entry_date project partner total_incl workflow_buttons
    ItemsByInvoice
    """, label=_("General"))
    # general = dd.Panel("""
    # panel1:20 panel2:30 panel3:25 totals:20
    # ItemsByInvoice
    # """, label=_("General"))

    # panel1 = dd.Panel("""
    # entry_date
    # """)
    #
    # panel2 = dd.Panel("""
    # partner
    # vat_regime
    # """)
    #
    # panel3 = dd.Panel("""
    # """)  # sales_remark
    #
    # totals = """
    # total_incl
    # workflow_buttons
    # """

    more = dd.Panel("""
    more1 more2 more3 more4
    intro
    """, label=_("More"))
    more1 = """
    invoicing_min_date invoicing_max_date
    subject
    """
    more2 = """
    language
    your_ref
    """
    more3 = """
    paper_type
    default_discount
    """

    more4 = """
    printed
    sent_to_peppol
    """

    accounting = dd.Panel("""
    accounting1 accounting2 accounting3 accounting4
    vat.MovementsByVoucher
    """, label=dd.plugins.accounting.verbose_name)

    accounting1 = """
    #voucher_date journal number #narration
    fiscal_year accounting_period
    id user
    """

    accounting2 = """
    vat_regime payment_method
    payment_term due_date
    match
    """

    accounting3 = """
    total_base
    total_vat
    total_incl
    """

    accounting4 = """
    balance_before
    voucher_movements
    balance_to_pay
    """

    if dd.is_installed("storage"):
        storage = dd.Panel("""
        storage.MovementsByVoucher
        """, label=dd.plugins.storage.verbose_name)
    else:
        storage = dd.DummyPanel()


class Invoices(PartnerVouchers):
    model = 'trading.VatProductInvoice'
    required_roles = dd.login_required(LedgerUser)
    order_by = ["-id"]
    # order_by = ["journal", "accounting_period__year", "number"]
    column_names = "id entry_date partner total_incl user *"
    detail_layout = 'trading.InvoiceDetail'
    insert_layout = dd.InsertLayout("""
    journal
    partner entry_date
    subject
    """,
                                    window_size=(40, 'auto'))
    # items_columns_spec = "product title unit_price qty discount_rate {TOTAL} invoiceable *"

    # start_at_bottom = True

    # @classmethod
    # def get_request_queryset(cls, ar):
    #     qs = super(Invoices, cls).get_request_queryset(ar)
    #     pv = ar.param_values
    #     if pv.state:
    #         qs = qs.filter(state=pv.state)
    #     return qs


class InvoicesByJournal(ByJournal, Invoices):
    quick_search_fields = "partner subject"
    order_by = ["fiscal_year", "number"]
    # start_at_bottom = True
    insert_layout = """
    partner entry_date
    subject
    """
    params_panel_hidden = True
    params_layout = "partner start_period end_period #year state cleared "
    column_names = "number_with_year entry_date #due_date " \
        "invoicing_min_date invoicing_max_date " \
        "partner " \
        "subject:10 total_incl " \
        "workflow_buttons *"


VoucherTypes.add_item_lazy(InvoicesByJournal)

if dd.get_plugin_setting('accounting', 'has_payment_methods', False):

    class CashInvoiceDetail(InvoiceDetail):
        main = "sales_tab general more accounting"

        sales_tab = dd.Panel("""
        partner payment_method total_incl
        cash_received cash_to_return balance_to_pay
        ItemsByInvoice
        """, label=_("Sales"))

        panel3 = dd.Panel("""
        match
        # payment_method
        paper_type
        printed
        """)  # sales_remark

    class CashInvoices(Invoices):
        model = 'trading.CashInvoice'

    class CashInvoicesByJournal(CashInvoices, ByJournal):
        column_names = "number_with_year entry_date " \
            "partner " \
            "total_incl payment_method cash_received cash_returned " \
            "workflow_buttons *"
        insert_layout = """
        partner
        user
        """
        detail_layout = 'trading.CashInvoiceDetail'

    VoucherTypes.add_item_lazy(CashInvoicesByJournal)


# class DiscountInvoicesByJournal(InvoicesByJournal):
#     items_columns_spec = "product unit_price qty discount_rate discount_amount {TOTAL} invoiceable *"
#
#
# VoucherTypes.add_item_lazy(DiscountInvoicesByJournal)


class PrintableInvoicesByJournal(PrintableByJournal, Invoices):
    label = _("Sales invoice journal")


class DueInvoices(Invoices):
    label = _("Due invoices")
    order_by = ["due_date"]

    column_names = "due_date journal__ref number_with_year " \
        "partner " \
        "total_incl balance_before balance_to_pay *"

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(cleared=dd.YesNo.no)
        return kw


class InvoiceItemDetail(dd.DetailLayout):
    main = """
    seqno product discount_rate discount_amount
    unit_price qty total_base total_vat total_incl
    invoiceable_type:15 invoiceable_id:15 invoiceable:50
    title #peppol_vat_category:5
    description"""

    window_size = (80, 20)


class InvoiceItems(dd.Table):
    """Shows all sales invoice items."""
    model = 'trading.InvoiceItem'
    required_roles = dd.login_required(LedgerStaff)
    auto_fit_column_widths = True
    # hidden_columns = "seqno description total_base total_vat"

    detail_layout = 'trading.InvoiceItemDetail'

    insert_layout = """
    product qty
    discount_rate discount_amount
    title
    """

    stay_in_grid = True


class ItemsByInvoice(InvoiceItems):
    label = _("Content")
    master_key = 'voucher'
    order_by = ["seqno"]
    required_roles = dd.login_required(LedgerUser)
    # extra_display_modes = {constants.DISPLAY_MODE_LIST}
    # column_names = "product title discount unit_price qty item_total *"
    # if dd.plugins.vat.item_vat:
    #     column_names = "product title unit_price qty discount_rate total_incl invoiceable *"
    # else:
    #     column_names = "product title unit_price qty discount_rate total_base invoiceable *"

    # @classmethod
    # def get_handle_name(self, ar):
    #     hname = constants._handle_attr_name
    #     voucher = ar.master_instance
    #     if voucher is not None:
    #         hname += voucher.journal.items_layout.value
    #     return hname

    @classmethod
    def get_row_classes(cls, self, ar):
        if self.product and self.product.subtotal:
            yield 'lightgrey'
            # Better would be 'grey' or 'lightgrey' but react currently knows
            # only 'yellow'

    @classmethod
    def get_column_names(self, ar):
        # if dd.plugins.vat.item_vat:
        #     TOTAL = "total_incl"
        # else:
        #     TOTAL = "total_base"
        # # if not issubclass(self.parent_layout, Invoices):
        # #     raise Exception(
        # #         f"20250502 {self.parent_layout} is not a subclass of Invoices")
        # # print(f"20250502 parent of {self} is {self.parent_layout}")
        # return dd.plugins.trading.items_column_names.format(TOTAL=TOTAL)
        return dd.plugins.trading.items_column_names
        # return self.parent_layout.items_columns_spec.format(TOTAL=TOTAL)


"""
The following two classes are used by the `trading.print_items_table` plugin
setting.
"""


class ItemsByInvoicePrint(ItemsByInvoice):
    # column_names = "description_print unit_price qty item_total"
    if dd.plugins.vat.item_vat:
        column_names = "description_print unit_price qty total_incl"
    else:
        column_names = "description_print unit_price qty total_base"
    include_qty_in_description = False

    @dd.displayfield(_("Description"))
    def description_print(cls, self, ar):
        title = self.title or str(self.product)
        elems = body_subject_to_elems(ar, title, self.description)
        # dd.logger.info("20160511a %s", cls)
        if cls.include_qty_in_description:
            if self.qty is not None and self.qty != 1:
                elems += [
                    " ",
                    _("({qty}*{unit_price}/{unit})").format(
                        qty=self.quantity,
                        unit=self.product.delivery_unit,
                        unit_price=self.unit_price)
                ]
        e = E.div(*elems)
        # dd.logger.info("20160704d %s", tostring(e))
        return e


class ItemsByInvoicePrintNoQtyColumn(ItemsByInvoicePrint):
    if dd.plugins.vat.item_vat:
        column_names = "description_print total_incl"
    else:
        column_names = "description_print total_base"
    include_qty_in_description = True
    hide_sums = True


# 20220512 VatProductInvoice.print_items_table = ItemsByInvoicePrint


class InvoiceItemsByProduct(InvoiceItems):
    master_key = 'product'
    column_names = "voucher voucher__partner qty title \
description:20x1 discount_rate discount_amount unit_price \
total_incl total_base total_vat *"

    editable = False
    # auto_fit_column_widths = True


class InvoiceItemsByGenerator(InvoicingsByGenerator):
    model = 'trading.InvoiceItem'
    column_names = "voucher qty title description:20x1 #discount " \
                   "unit_price total_incl #total_base #total_vat *"


class SignAction(actions.Action):
    label = "Sign"

    def run_from_ui(self, ar):

        def ok(ar):
            for row in ar.selected_rows:
                row.instance.user = ar.get_user()
                row.instance.save()
            ar.success(refresh=True)

        ar.confirm(
            ok,
            _("Going to sign %d documents as user %s. Are you sure?") %
            (len(ar.selected_rows), ar.get_user()))


class DocumentsToSign(Invoices):
    use_as_default_table = False
    filter = dict(user__isnull=True)
    # can_add = perms.never
    column_names = "number:4 #order entry_date " \
        "partner:10 " \
        "subject:10 total_incl total_base total_vat "
    # actions = Invoices.actions + [ SignAction() ]


class InvoicesByPartner(Invoices):
    # model = 'trading.VatProductInvoice'
    order_by = ["-entry_date", '-id']
    master_key = 'partner'
    column_names = "entry_date detail_link total_incl "\
                   "workflow_buttons *"
    # column_names = "entry_date journal__ref number total_incl "\
    #                "workflow_buttons *"


class ProductDetailMixin(dd.DetailLayout):
    sales = dd.Panel("""
    trading.InvoiceItemsByProduct
    """,
                     label=dd.plugins.trading.verbose_name)
