# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.utils.text import format_lazy

from lino.utils.html import E
from lino.mixins.registrable import RegistrableState
from lino.core.choicelists import PointingChoice, MissingRow
from lino.api import dd, rt, _, gettext
# from lino_xl.lib.accounting.utils import DC
from .roles import LedgerStaff

if dd.is_installed('ledgers'):
    ledgers = dd.plugins.ledgers
else:
    ledgers = None


class Debit(dd.Choice):
    value = 'D'
    text = _("Debit")
    names = 'debit'

    def normalized_amount(self, n):
        return -n   # 20240621

    def opposite(self):
        return self.choicelist.credit

    def __not__(self):
        raise Exception("20201013")


class Credit(dd.Choice):
    value = 'C'
    text = _("Credit")
    names = 'credit'

    def normalized_amount(self, n):
        return n   # 20240621

    def opposite(self):
        return self.choicelist.debit

    def __not__(self):
        raise Exception("20201013")


class DC(dd.ChoiceList):
    verbose_name = _("Booking direction")
    verbose_name_plural = _("Booking directions")
    required_roles = dd.login_required(LedgerStaff)


add = DC.add_item_instance
add(Debit())
add(Credit())


class JournalGroup(dd.Choice):
    menu_group = None
    # def __init__(self, value, text, name, menu_group=None, **kwargs):
    #     self.menu_group = dd.plugins.get(menu_group)
    #     super(JournalGroup, self).__init__(value, text, name, **kwargs)


class JournalGroups(dd.ChoiceList):
    item_class = JournalGroup
    verbose_name = _("Journal group")
    verbose_name_plural = _("Journal groups")
    required_roles = dd.login_required(LedgerStaff)


add = JournalGroups.add_item
add('10', _("Sales"), 'sales')
add('20', _("Purchases"), 'purchases')
add('30', _("Wages"), 'wages')
add('40', _("Financial"), 'financial')
# add('40', _("Money and banks"), 'money')
add('50', _("VAT"), 'vat')
add('60', _("Miscellaneous transactions"), 'misc')

if dd.is_installed("trading"):
    JournalGroups.sales.menu_group = dd.plugins.trading
    # JournalGroups.purchases.menu_group = dd.plugins.accounting


class CommonAccount(PointingChoice):
    pointing_field_name = 'accounting.Account.common_account'
    show_values = True
    clearable = False
    needs_partner = False

    # sheet_item = ''  # filled by lino_xl.lib.sheets if installed

    def __init__(self, value, text, name, clearable, **kwargs):
        # the class attribute `name` ís used as value
        super().__init__(value, text, name, **kwargs)
        # self.sheet_item = CommonItems.get_by_name(actype)
        # self.clearable = clearable
        self.clearable = clearable
        self.needs_partner = clearable

    def create_object(self, **kwargs):
        kwargs.update(dd.str2kw('name', self.text))
        kwargs.update(clearable=self.clearable)
        kwargs.update(needs_partner=self.needs_partner)
        kwargs.update(common_account=self)
        kwargs.setdefault('ref', self.value)
        # if dd.is_installed('sheets'):
        #     kwargs.update(sheet_item=self.sheet_item.get_object())
        # else:
        #     kwargs.pop('sheet_item', None)
        return self.pointing_field.model(**kwargs)


class CommonAccounts(dd.ChoiceList):
    verbose_name = _("Common account")
    verbose_name_plural = _("Common accounts")
    item_class = CommonAccount
    column_names = 'value name text clearable db_object'
    required_roles = dd.login_required(LedgerStaff)

    # @dd.virtualfield(models.CharField(_("Sheet item"), max_length=20))
    # def sheet_item(cls, choice, ar):
    #     return choice.sheet_item

    @dd.virtualfield(dd.ForeignKey('accounting.Account'))
    def db_object(cls, choice, ar):
        filter = dict()
        if ledgers:
            filter.update(ledger=ar.get_user().ledger)
        obj = choice.get_object(**filter)
        if obj is None or isinstance(obj, MissingRow):
            return None
        return obj

    @dd.virtualfield(models.BooleanField(_("Clearable")))
    def clearable(cls, choice, ar):
        return choice.clearable


add = CommonAccounts.add_item

add('1000', _("Net income (loss)"), 'net_income_loss', True)

add('4000', _("Customers"), 'customers', True)
# add('4010', _("Advance credit"),   'advance_credit', True)
add('4100', _("Suppliers"), 'suppliers', True)
add('4200', _("Employees"), 'employees', True)
add('4300', _("Pending payment orders"), 'pending_po', True)
add('4500', _("Tax offices"), 'tax_offices', True)

add('4510', _("VAT due"), 'vat_due', False)
add('4520', _("VAT deductible"), 'vat_deductible', False)
add('4530', _("VAT returnable"), 'vat_returnable', False)
add('4513', _("VAT declared"), 'due_taxes', False)

add('4800', _("Internal clearings"), 'clearings', True)
add('4900', _("Waiting account"), 'waiting', True)

add('5500', _("Bestbank"), 'best_bank', False)
add('5700', _("Cash"), 'cash', False)

if dd.get_plugin_setting('accounting', 'has_payment_methods', False):

    add('5701', _("Online payments"), 'online_payments', False)
    add('5702', _("Credit card payments"), 'credit_card_payments', False)

add('6040', _("Purchase of goods"), 'purchase_of_goods', False)
add('6010', _("Purchase of services"), 'purchase_of_services', False)
add('6020', _("Purchase of investments"), 'purchase_of_investments', False)

add('6300', _("Wages"), 'wages', False)
add('6900', _("Net income"), 'net_income', False)

add('7000', _("Sales"), 'sales', False)
add('7900', _("Net loss"), 'net_loss', False)


class VoucherType(dd.Choice):

    def __init__(self, table_class, text=None):
        self.table_class = table_class
        model = dd.resolve_model(table_class.model)
        self.model = model
        # value = dd.full_model_name(model)
        value = str(table_class)
        if text is None:
            # text = model._meta.verbose_name + ' (%s)' % dd.full_model_name(model)
            # text = model._meta.verbose_name + ' (%s.%s)' % (
            text = format_lazy("{} ({})", model._meta.verbose_name, value)
        #     model.__module__, model.__name__)
        name = None
        super().__init__(value, text, name)

    def get_items_table(self):
        lh = self.table_class.detail_layout.get_layout_handle()
        from lino.modlib.extjs.elems import GridElement
        for e in lh.walk():
            # print(repr(e), e.__class__)
            if isinstance(e, GridElement):
                return e

    def get_journals(self, **kwargs):
        """Return a list of the :class:`Journal` objects that work on this
        voucher type.

        """
        kwargs.update(voucher_type=self)
        return rt.models.accounting.Journal.objects.filter(**kwargs)

    def get_journal_kwargs(self, trade_type=None, account=None, **kw):
        kw.update(voucher_type=self)
        if isinstance(trade_type, str):
            trade_type = TradeTypes.get_by_name(trade_type)
        kw.update(trade_type=trade_type)
        if isinstance(account, str):
            account = rt.models.accounting.Account.get_by_ref(account)
        if account is not None:
            kw.update(account=account)
        return kw

    def create_journal(self, *args, **kw):
        kw = self.get_journal_kwargs(*args, **kw)
        return rt.models.accounting.Journal(**kw)


class VoucherTypes(dd.ChoiceList):
    required_roles = dd.login_required(LedgerStaff)
    verbose_name = _("Voucher type")
    verbose_name_plural = _("Voucher types")
    column_names = "value name text model_name"

    item_class = VoucherType
    max_length = 100

    @classmethod
    def get_for_model(cls, model):
        """
        Return the :class:`VoucherType` for the given model.
        """
        return cls.find_first(lambda i: issubclass(i.model, model))

    @classmethod
    def get_for_table(cls, table_class):
        """
        Return the :class:`VoucherType` for the given table.
        """
        # return cls.find_first(lambda i: issubclass(table_class, i.table_class))
        return cls.find_first(lambda i: i.table_class is table_class)

    @classmethod
    def find_first(cls, func, default=None):
        """Find the first choice that matches the condition. Return default if
        no choice matches."""
        for o in cls.get_list_items():
            if func(o):
                return o
        return default

    @dd.displayfield(_("Model"))
    def model_name(cls, vt, ar):
        return str(vt.model)

    # @classmethod
    # def add_item(cls, *args, **kwargs):
    #     return cls.add_item_instance(VoucherType(*args, **kwargs))


class TradeType(dd.Choice):
    price_field_name = None
    price_field_label = None
    main_account = None
    base_account = None
    base_account_field_name = None
    base_account_field_label = None
    invoice_account_field_name = None
    invoice_account_field_label = None
    dc = DC.debit

    def get_base_account(self, ar=None):
        filter = {}
        if ar is not None and ledgers:
            filter.update(ledger=ar.get_user().ledger)
        return self.base_account.get_object(**filter)

    def get_main_account(self, ar=None):
        if self.main_account:
            filter = {}
            if ar is not None and ledgers:
                filter.update(ledger=ar.get_user().ledger)
            return self.main_account.get_object(**filter)

    def get_product_base_account(self, product, ar=None):
        # TODO: remove ar from signature because you have the ledger in the journal
        filter = {}
        if ar is not None and ledgers:
            filter.update(ledger=ar.get_user().ledger)
        if self.base_account_field_name is None:
            return self.base_account.get_object(**filter)
            # raise Exception("%s has no base_account_field_name" % self)
        return getattr(product, self.base_account_field_name, None) or \
            self.base_account.get_object(**filter)

    def get_partner_invoice_account(self, partner):
        if self.invoice_account_field_name is None:
            return None
        return getattr(partner, self.invoice_account_field_name, None)

    def get_catalog_price(self, product):
        return getattr(product, self.price_field_name)

    def get_allowed_accounts(self, **kw):
        kw[self.name + '_allowed'] = True
        return rt.models.accounting.Account.objects.filter(**kw)


def ca_fmt(ar, ca):
    if ar is None or ca is None:
        return ''
    elems = []
    filter = {}
    if ledgers:
        filter.update(ledger=ar.get_user().ledger)
    obj = ca.get_object(**filter)
    if obj is None:
        elems.append(gettext("(undefined)"))
    else:
        # elems.append(ar.obj2html(obj))
        elems.append(str(obj))
    elems.append(" ({})".format(ca))
    return E.div(*elems)


class TradeTypes(dd.ChoiceList):
    required_roles = dd.login_required(LedgerStaff)
    verbose_name = _("Trade type")
    verbose_name_plural = _("Trade types")
    item_class = TradeType
    help_text = _("The type of trade, e.g. 'sales' or 'purchases' or 'wages'.")
    column_names = "value name text main_account base_account "\
                   "product_account_field invoice_account_field"

    @dd.displayfield(_("Main account"))
    def main_account(cls, tt, ar):
        return ca_fmt(ar, tt.main_account)

    @dd.displayfield(_("Base account"))
    def base_account(cls, tt, ar):
        return ca_fmt(ar, tt.base_account)

    @dd.displayfield(_("Product account field"))
    def product_account_field(cls, tt, ar):
        if tt.base_account_field_name:
            return "{} ({})".format(tt.base_account_field_label,
                                    tt.base_account_field_name)

    @dd.displayfield(_("Price field"))
    def product_price_field(cls, tt, ar):
        if tt.price_field_name:
            return "{} ({})".format(tt.price_field_label, tt.price_field_name)

    @dd.displayfield(_("Invoice account field"))
    def invoice_account_field(cls, tt, ar):
        if tt.invoice_account_field_name:
            return "{} ({})".format(tt.invoice_account_field_label,
                                    tt.invoice_account_field_name)

    # @dd.displayfield(_("Description"))
    # def description(cls, tt, ar):
    #     if ar is None:
    #         return ''
    #     elems = []
    #     if tt.base_account:
    #         elems += [gettext("Default base account"), ": "]
    #         elems += [str(tt.base_account)]
    #         elems += [" (", ar.obj2html(tt.get_base_account()), ")"]
    #     if tt.base_account_field_name:
    #         if len(elems): elems.append(", ")
    #         elems += [gettext("Product base account field"), ": "]
    #         elems += [str(tt.base_account_field_name)]
    #     if tt.invoice_account_field_name:
    #         if len(elems): elems.append(", ")
    #         elems += [gettext("Invoice account field"), ": "]
    #         elems += [str(tt.invoice_account_field_name)]
    #     return E.div(*elems)


TradeTypes.add_item('S',
                    _("Sales"),
                    'sales',
                    dc=DC.debit,
                    base_account=CommonAccounts.sales,
                    main_account=CommonAccounts.customers)
TradeTypes.add_item('P',
                    _("Purchases"),
                    'purchases',
                    dc=DC.credit,
                    base_account=CommonAccounts.purchase_of_goods,
                    main_account=CommonAccounts.suppliers,
                    invoice_account_field_name='purchase_account',
                    invoice_account_field_label=_("Purchase account"))
TradeTypes.add_item('W',
                    _("Wages"),
                    'wages',
                    dc=DC.credit,
                    base_account=CommonAccounts.wages,
                    main_account=CommonAccounts.employees)
TradeTypes.add_item('T',
                    _("Taxes"),
                    'taxes',
                    dc=DC.debit,
                    base_account=CommonAccounts.due_taxes,
                    main_account=CommonAccounts.tax_offices)
TradeTypes.add_item('C',
                    _("Clearings"),
                    'clearings',
                    dc=DC.debit,
                    main_account=CommonAccounts.clearings)
TradeTypes.add_item('B',
                    _("Bank payment orders"),
                    'bank_po',
                    dc=DC.debit,
                    main_account=CommonAccounts.pending_po)

# Note that :mod:`lino_xl.lib.trading.models` and/or
# :mod:`lino_xl.lib.accounting.models` (if installed) will modify
# `TradeTypes.sales` at module level so that the following
# `inject_vat_fields` will inject the required fields to
# system.SiteConfig and products.Product (if these are installed).


@dd.receiver(dd.pre_analyze)
def inject_tradetype_fields(sender, **kw):
    """This defines certain database fields related to your
    :class:`TradeTypes`.

    """
    # print(20200622, list([i.invoice_account_field_name for i in TradeTypes.items()]))
    for tt in TradeTypes.items():
        if tt.invoice_account_field_name is not None:
            dd.inject_field(
                'contacts.Partner', tt.invoice_account_field_name,
                dd.ForeignKey('accounting.Account',
                              verbose_name=tt.invoice_account_field_label,
                              on_delete=models.PROTECT,
                              related_name='partners_by_'
                              + tt.invoice_account_field_name,
                              blank=True,
                              null=True))
        if tt.base_account_field_name is not None:
            dd.inject_field(
                'products.Product', tt.base_account_field_name,
                dd.ForeignKey('accounting.Account',
                              verbose_name=tt.base_account_field_label,
                              on_delete=models.PROTECT,
                              related_name='products_by_'
                              + tt.base_account_field_name,
                              blank=True,
                              null=True))
        if tt.price_field_name is not None:
            dd.inject_field(
                'products.Product', tt.price_field_name,
                dd.PriceField(verbose_name=tt.price_field_label,
                              blank=True,
                              null=True))


class VoucherState(RegistrableState):
    is_editable = False


class VoucherStates(dd.Workflow):
    item_class = VoucherState
    verbose_name = _("Voucher state")
    verbose_name_plural = _("Voucher states")
    column_names = "value name text is_editable"
    old2new = {'40': '30', '30': '20'}

    @classmethod
    def get_editable_states(cls):
        return [o for o in cls.objects() if o.is_editable]

    @dd.virtualfield(models.BooleanField(_("Editable")))
    def is_editable(cls, choice, ar):
        return choice.is_editable


add = VoucherStates.add_item
add('10', _("Draft"), 'draft', is_editable=True)
add('20', _("Registered"), 'registered')
# add('30', _("Sent"), 'sent')
add('30', _("Cancelled"), 'cancelled')


@dd.receiver(dd.pre_analyze)
def setup_vat_workflow(sender=None, **kw):
    if False:
        VoucherStates.registered.add_transition(_("Register"),
                                                required_states='draft',
                                                icon_name='accept')
        VoucherStates.draft.add_transition(_("Deregister"),
                                           required_states="registered",
                                           icon_name='pencil')
    elif False:
        VoucherStates.registered.add_transition(
            # unichr(0x25c6),  # ◆
            _("Register"),
            help_text=_("Register"),
            required_states='draft')
        VoucherStates.draft.add_transition(
            _("Deregister"),
            # unichr(0x25c7),  # ◇
            help_text=_("Deregister"),
            required_roles=dd.login_required(LedgerStaff),
            required_states="registered")
    else:
        VoucherStates.registered.add_transition(
            # unichr(0x25c6),  # ◆
            # _("Register"),
            # help_text=_("Register"),
            required_states='draft')
        VoucherStates.draft.add_transition(
            # unichr(0x25c7),  # ◇
            # _("Deregister"),
            # help_text=_("Deregister"),
            required_roles=dd.login_required(LedgerStaff),
            required_states="registered cancelled")
        VoucherStates.cancelled.add_transition(
            # unichr(0x25c6),  # ◆
            # _("Cancel"),
            # help_text=_("Cancel"),
            required_states='draft')


# class ItemsLayouts(TableLayouts):
#     verbose_name = _("Voucher items layout")
#     verbose_name_plural = _("Voucher items layouts")
#
#
# add = ItemsLayouts.add_item
# add(
#     '10', _("Default"),
#     "product title unit_price qty discount_rate {TOTAL} invoiceable *")
# add(
#     '20', _("With absolute discount"),
#     "product unit_price qty discount_rate discount_amount {TOTAL} invoiceable *")
