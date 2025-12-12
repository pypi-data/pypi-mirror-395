# Copyright 2012-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _

from lino_xl.lib.accounting.ui import (PartnerVouchers, ByJournal,
                                   PrintableByJournal, Movements,
                                   MovementsByVoucher)

from lino_xl.lib.accounting.choicelists import TradeTypes, VoucherTypes
from lino_xl.lib.accounting.roles import LedgerUser, LedgerStaff
from lino_xl.lib.accounting.ui import VouchersByPartnerBase
from lino_xl.lib.accounting.mixins import ItemsByVoucher

from .choicelists import VatRegimes, VatAreas
from .mixins import VatDeclaration, VatDocument, VatVoucher
from lino.core import constants


class InvoiceDetail(dd.DetailLayout):

    main = "general more"


    general = dd.Panel("""
    general1 general2 general3
    ItemsByInvoice
    """, label=_("General"))

    general1 = """
    number partner
    entry_date accounting_period
    your_ref:20 vat_regime:20
    """

    general2 = """
    match
    payment_term
    due_date
    """

    general3 = """
    workflow_buttons
    total_base
    total_vat
    total_incl
    """

    more = dd.Panel("""
    more1 more2
    vat.MovementsByVoucher
    """, label=_("More"))

    more1 = """
    journal user
    narration id
    """

    more2 = """
    uploads.UploadsByController:60
    """

class Invoices(PartnerVouchers):
    required_roles = dd.login_required(LedgerUser)
    model = 'vat.VatAccountInvoice'
    order_by = ["-id"]
    column_names = "entry_date id number_with_year partner total_incl user *"
    detail_layout = InvoiceDetail()
    insert_layout = """
    journal partner
    entry_date total_incl
    """
    # start_at_bottom = True


class InvoicesByJournal(ByJournal, Invoices):
    # ByJournal must be before Invoices the get the right order_by
    params_layout = "partner state start_period end_period user"
    column_names = "number_with_year entry_date due_date " \
        "your_ref partner " \
        "total_incl " \
        "total_base total_vat user workflow_buttons *"
    #~ "ledger_remark:10 " \
    insert_layout = """
    partner
    entry_date total_incl
    """


class PrintableInvoicesByJournal(PrintableByJournal, Invoices):
    label = _("Purchase journal")


VoucherTypes.add_item_lazy(InvoicesByJournal)


class ItemsByInvoice(ItemsByVoucher):
    model = 'vat.InvoiceItem'
    default_display_modes = {None: constants.DISPLAY_MODE_GRID}
    column_names = "account title vat_class total_incl total_base total_vat"


class VouchersByPartner(VouchersByPartnerBase):
    label = _("Trade vouchers")
    column_names = "entry_date voucher total_incl total_base total_vat"
    _voucher_base = VatDocument

    @dd.virtualfield('vat.VatAccountInvoice.total_incl')
    def total_incl(self, row, ar):
        return row.total_incl

    @dd.virtualfield('vat.VatAccountInvoice.total_base')
    def total_base(self, row, ar):
        return row.total_base

    @dd.virtualfield('vat.VatAccountInvoice.total_vat')
    def total_vat(self, row, ar):
        return row.total_vat


class MovementsByVoucher(MovementsByVoucher):
    column_names = 'account project partner debit credit vat_class match_link cleared *'


class VatInvoices(PartnerVouchers):
    abstract = True
    _trade_type = None
    editable = False
    model = VatVoucher
    column_names = 'detail_link partner partner_vat_id vat_regime total_base total_vat total_incl'
    # order_by = ['entry_date', 'partner']
    # order_by = ['entry_date', 'id']
    # order_by = ['entry_date', 'number']
    order_by = ['accounting_period', 'number']
    hidden_elements = frozenset(
        """entry_date journal__trade_type journal number
        journal__trade_type state user""".split())

    parameters = dict(intracom=dd.YesNo.field(_("Show intracom vouchers"),
                                              blank=True),
                      **PartnerVouchers.parameters)

    params_layout = "partner project start_period end_period cleared intracom"
    intracom_regimes = set(
        [r for r in VatRegimes.get_list_items() if r.vat_area == VatAreas.eu])

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        assert not kwargs
        fkw = dict()
        if cls._trade_type is not None:
            fkw.update(journal__trade_type=cls._trade_type)
        if (pv := ar.param_values) is not None:
            if pv.intracom == dd.YesNo.yes:
                fkw.update(vat_regime__in=cls.intracom_regimes)
                # note that we cannot use qs.filter() because this table is on an abstract model
        return super().get_request_queryset(ar, **fkw)
        # raise Exception("20170905 {}".format(qs.query))

    @dd.virtualfield(dd.ForeignKey('contacts.Partner'))
    def partner(cls, obj, ar=None):
        return obj.partner

    @dd.virtualfield('contacts.Partner.vat_id')
    def partner_vat_id(cls, obj, ar=None):
        return obj.partner.vat_id


dd.update_field(VatInvoices, 'detail_link', verbose_name=_("Invoice"))


class ByDeclaration(dd.Table):

    abstract = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(ByDeclaration, self).param_defaults(ar, **kw)
        mi = ar.master_instance
        if mi is not None:
            kw.update(start_period=mi.start_period, end_period=mi.end_period)
        # print("20191205", kw)
        return kw


class MovementsByDeclaration(ByDeclaration, Movements):
    label = _("Declared movements")
    master = VatDeclaration
    # exclude = dict(vat_class="")
    column_names = "value_date voucher_link description debit credit account__vat_column vat_class vat_regime *"


class SalesByDeclaration(ByDeclaration, VatInvoices):
    _trade_type = TradeTypes.sales
    label = _("VAT sales")
    master = VatDeclaration


class PurchasesByDeclaration(ByDeclaration, VatInvoices):
    _trade_type = TradeTypes.purchases
    label = _("VAT purchases")
    master = VatDeclaration


class IntracomInvoices(VatInvoices):
    abstract = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(IntracomInvoices, self).param_defaults(ar, **kw)
        kw.update(intracom=dd.YesNo.yes)
        return kw


class IntracomSales(IntracomInvoices):
    _trade_type = TradeTypes.sales
    label = _("Intra-Community sales")
    # model = "trading.VatProductInvoice"


class IntracomPurchases(IntracomInvoices):
    _trade_type = TradeTypes.purchases
    label = _("Intra-Community purchases")
