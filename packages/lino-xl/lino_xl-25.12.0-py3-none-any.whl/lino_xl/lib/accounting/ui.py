# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.db.models import OuterRef, Subquery, Sum

from lino import mixins
from lino.api import dd, rt, _
from lino.core import constants
from lino.utils.html import join_elems, tostring, E
# from lino.utils.report import Report
from lino.modlib.periods.mixins import PeriodRangeParameters, PeriodRangeObservable
from .choicelists import TradeTypes, VoucherTypes, JournalGroups
from .choicelists import VoucherStates
from .mixins import JournalRef, Payable
from .roles import AccountingReader, LedgerUser, LedgerStaff, LedgerPartner
from .utils import Balance
from .utils import DC, ZERO

has_payment_methods = dd.get_plugin_setting('accounting', 'has_payment_methods',
                                            False)
project_model = dd.get_plugin_setting('accounting', 'project_model', None)
multi_ledger = dd.is_installed("ledgers")


class Accounts(dd.Table):
    model = 'accounting.Account'
    required_roles = dd.login_required(LedgerStaff)
    order_by = ['ref']
    column_names = "description sheet_item needs_partner clearable ref *"
    insert_layout = """
    ref sheet_item
    name
    """
    detail_layout = """
    ref:10 common_account sheet_item id
    name
    needs_partner:30 clearable:30 default_amount:10
    accounting.MovementsByAccount
    """


class JournalDetail(dd.DetailLayout):
    main = """
    name ref:5
    journal_group:15 voucher_type:20 trade_type:20 seqno:5 id:5
    account partner build_method:20 template:20 uploads_volume #items_layout #invoicing_area
    dc make_ledger_movements make_storage_movements is_outbound last_sending
    force_sequence yearly_numbering auto_fill_suggestions auto_check_clearings must_declare preliminary
    printed_name
    MatchRulesByJournal
    """


class Journals(dd.Table):
    required_roles = dd.login_required(LedgerStaff)
    model = 'accounting.Journal'
    order_by = ["seqno"]
    column_names = "ref:5 name trade_type journal_group " \
                   "voucher_type force_sequence * seqno id"
    detail_layout = 'accounting.JournalDetail'
    insert_layout = dd.InsertLayout("""
    ref name
    journal_group
    voucher_type
    """, window_size=(60, 'auto'))


if multi_ledger:
    from lino_xl.lib.ledgers.ui import ByLedger

    class JournalsByLedger(Journals, ByLedger):
        pass


class JournalsOverview(Journals):
    required_roles = dd.login_required(LedgerUser)
    column_names = "description num_vouchers this_year this_month state_draft warnings *"
    # default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    editable = False
    default_display_modes = {None: constants.DISPLAY_MODE_TILES}

    @classmethod
    def get_filter_kw(cls, ar, **kw):
        if multi_ledger:
            kw.update(ledger=ar.get_user().ledger)
        return kw

    @classmethod
    def unused_table_as_summary(cls, ar):
        # if ar is None:
        #     return None
        items = []
        for obj in ar:  # cls.get_request_queryset(ar):
            elems = []
            table_class = obj.get_doc_report()
            sar = table_class.create_request(master_instance=obj)
            # elems.append(str(sar.get_total_count()))
            # elems.append(" ")
            # elems.append(ar.href_to_request(sar, text=str(obj)))
            text = "{} {}".format(sar.get_total_count(), obj)
            elems.append(ar.href_to_request(sar, text=text))
            if not ar.get_user().is_anonymous:
                sar = table_class.insert_action.request_from(
                    ar, master_instance=obj)
                # print(20170217, sar)
                sar.known_values.update(journal=obj)
                # txt = dd.babelattr(obj, 'printed_name')
                # btn = sar.ar2button(None, _("New {}").format(txt), icon_name=None)
                btn = sar.ar2button(
                    label="⊕",  # U+2295 Circled Plus Unicode Character.
                    icon_name=None)
                # btn = sar.ar2button()
                # btn.set("style", "padding-left:10px")
                btn.set("style", "text-decoration:none")
                elems.append(" ")
                elems.append(btn)
            # else:
            #     elems.append(" / ")
            #     elems.append(obj.insert_voucher_button(ar))
            items.append(E.li(*elems))
        return tostring(E.ul(*items))

    @dd.displayfield(_("Description"))
    def description(cls, obj, ar):
        elems = [str(obj), obj.insert_voucher_button(ar)]
        # if ar.get_user().authenticated:
        return E.p(*join_elems(elems, " / "))

    @dd.requestfield(_("Total"))
    def num_vouchers(self, obj, ar):
        tbl = obj.get_doc_report()
        return tbl.create_request(master_instance=obj)

    @dd.requestfield(_("This year"))
    def this_year(self, obj, ar):
        tbl = obj.get_doc_report()
        StoredPeriod = rt.models.periods.StoredPeriod
        # print(20190924, year)
        pv = dict()
        if issubclass(tbl.model, PeriodRangeObservable):
            pv.update(start_period=StoredPeriod.get_or_create_from_date(
                dd.today().replace(month=1, day=1)))
            pv.update(end_period=StoredPeriod.get_or_create_from_date(
                dd.today().replace(month=12, day=31)))
        return tbl.create_request(master_instance=obj, param_values=pv)

    @dd.requestfield(_("This month"))
    def this_month(self, obj, ar):
        tbl = obj.get_doc_report()
        StoredPeriod = rt.models.periods.StoredPeriod
        # print(20190924, year)
        pv = dict()
        if issubclass(tbl.model, PeriodRangeObservable):
            pv.update(
                start_period=StoredPeriod.get_or_create_from_date(dd.today()))
        return tbl.create_request(master_instance=obj, param_values=pv)

    @dd.requestfield(_("Unfinished"))
    def state_draft(self, obj, ar):
        tbl = obj.get_doc_report()
        pv = dict(state=VoucherStates.draft)
        return tbl.create_request(master_instance=obj, param_values=pv)

    @dd.displayfield(_("Warnings"))
    def warnings(cls, self, ar):
        elems = []
        # elems.append(gettext("Everything ok"))
        return E.p(*join_elems(elems, " / "))


class ByJournal(dd.Table):
    # order_by = ["-entry_date", '-id']
    order_by = ["fiscal_year", "number"]
    master_key = 'journal'
    start_at_bottom = True
    required_roles = dd.login_required(LedgerUser)
    params_layout = "start_period end_period state user"
    no_phantom_row = True
    # abstract = True  # no need to set this explicitly, see Actor.is_abstract()

    @classmethod
    def get_title_base(self, ar):
        """Without this override we would have a title like "Invoices of
        journal <Invoices>".  But we want just "Invoices".

        """
        return str(ar.master_instance)

    @classmethod
    def create_journal(cls, *args, **kw):
        vt = VoucherTypes.get_for_table(cls)
        return vt.create_journal(*args, **kw)


class PrintableByJournal(ByJournal):
    editable = False
    params_layout = "journal start_period end_period state"

    column_names = "number entry_date partner total_base total_vat total_incl vat_regime *"
    abstract = True

    @classmethod
    def setup_request(self, ar):
        ar.master_instance = ar.param_values.journal


class PaymentTerms(dd.Table):
    required_roles = dd.login_required(LedgerStaff)
    model = 'accounting.PaymentTerm'
    order_by = ["ref"]
    column_names = "ref name months days end_of_month payer informal *"
    detail_layout = """
    ref months days end_of_month payer informal
    name
    printed_text
    """


if has_payment_methods:

    class PaymentMethods(dd.Table):
        required_roles = dd.login_required(LedgerStaff)
        model = "accounting.PaymentMethod"
        column_names = "id designation payment_account is_cash *"


class VoucherDetail(dd.DetailLayout):
    main = """
    journal number entry_date accounting_period
    accounting.MovementsByVoucher
    """


class Vouchers(dd.Table):
    abstract = True
    required_roles = dd.login_required(LedgerUser)
    model = 'accounting.Voucher'
    editable = False
    order_by = ["entry_date", "number"]
    column_names = "entry_date number *"
    parameters = dict(year=dd.ForeignKey('periods.StoredYear', blank=True),
                      journal=JournalRef(blank=True))
    params_layout = "journal start_period end_period #state user"
    detail_layout = "accounting.VoucherDetail"

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        qs = super(Vouchers, cls).get_request_queryset(ar, **kwargs)
        if isinstance(qs, list):
            return qs
        if (pv := ar.param_values) is None:
            return qs
        if pv.year:
            qs = qs.filter(fiscal_year=pv.year)
        if pv.journal:
            qs = qs.filter(journal=pv.journal)
        return qs


class AllVouchers(Vouchers):
    required_roles = dd.login_required(LedgerStaff)


# class VouchersByPartnerBase(dd.VirtualTable):
class VouchersByPartnerBase(Vouchers):
    """Shows all numbered vouchers of a given partner.

    This is a :term:`virtual table` with a customized slave summary.

    """
    abstract = True
    label = _("Partner vouchers")
    required_roles = dd.login_required(LedgerUser)

    order_by = ["-entry_date", '-id']
    master = 'contacts.Partner'
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

    _master_field_name = 'partner'
    # _voucher_base = PartnerRelated
    _voucher_base = Payable
    model = 'accounting.Voucher'
    detail_layout = "accounting.VoucherDetail"

    @classmethod
    def get_data_rows(self, ar):
        obj = ar.master_instance
        rows = []
        if obj is not None:
            flt = {self._master_field_name: obj}
            for M in rt.models_by_base(self._voucher_base):
                rows += list(M.objects.filter(**flt))

            # def by_date(a, b):
            #     return cmp(b.entry_date, a.entry_date)

            rows.sort(key=lambda i: i.entry_date)
        return rows

    @dd.displayfield(_("Voucher"))
    def voucher(self, row, ar):
        return ar.obj2html(row)

    @dd.virtualfield('accounting.Movement.partner')
    def partner(self, row, ar):
        return row.partner

    @dd.virtualfield('accounting.Voucher.entry_date')
    def entry_date(self, row, ar):
        return row.entry_date

    # @dd.virtualfield('accounting.Voucher.state')
    # def state(self, row, ar):
    #     return row.state

    @classmethod
    def table_as_summary(self, ar):
        elems = []
        obj = ar.master_instance
        for voucher in ar:
            vc = voucher.get_mti_leaf()
            if vc and vc.state.name == "draft":
                # if voucher.state.name == "draft":
                elems += [ar.obj2html(vc), " "]

        if len(elems):
            elems.append(E.br())

        vtypes = []
        for vt in VoucherTypes.items():
            if issubclass(vt.model, self._voucher_base):
                vtypes.append(vt)

        if not ar.get_user().user_type.readonly:
            actions = []
            flt = {self._master_field_name: obj}
            for vt in vtypes:
                for jnl in vt.get_journals():
                    sar = vt.table_class.insert_action.request_from(
                        ar, master_instance=jnl, known_values=flt)
                    btn = sar.ar2button(label=str(jnl), icon_name=None)
                    if len(actions):
                        actions.append(', ')
                    actions.append(btn)

            elems += [str(_("Create voucher in journal")), " "] + actions
        return tostring(elems)


class MatchRules(dd.Table):
    required_roles = dd.login_required(LedgerStaff)
    model = 'accounting.MatchRule'


class MatchRulesByAccount(MatchRules):
    master_key = 'account'
    column_names = "journal *"


class MatchRulesByJournal(MatchRules):
    order_by = ["account"]
    master_key = 'journal'
    column_names = "account *"
    params_layout = None


class ExpectedMovements(dd.VirtualTable):
    row_height = 4
    required_roles = dd.login_required(AccountingReader)
    label = _("Debts")
    icon_name = 'book_link'
    # ~ column_names = 'match due_date debts payments balance'
    column_names = 'due_date:15 balance debts payments'
    auto_fit_column_widths = True
    # variable_row_height = True
    parameters = dd.ParameterPanel(
        date_until=models.DateField(_("Date until"), blank=True, null=True),
        trade_type=TradeTypes.field(blank=True),
        from_journal=dd.ForeignKey('accounting.Journal', blank=True),
        for_journal=dd.ForeignKey('accounting.Journal',
                                  blank=True,
                                  verbose_name=_("Clearable by")),
        account=dd.ForeignKey('accounting.Account', blank=True),
        partner=dd.ForeignKey('contacts.Partner', blank=True),
        project=dd.ForeignKey(project_model, blank=True),
        show_sepa=dd.YesNo.field(_("With SEPA"), blank=True),
        same_dc=dd.YesNo.field(_("Same D/C"), blank=True),
    )
    params_layout = """
    trade_type date_until from_journal for_journal
    project partner account show_sepa same_dc"""

    @classmethod
    def get_dc(cls, ar=None):
        return DC.credit  # 20201219 ExpectedMovements.get_dc()

    @classmethod
    def get_data_rows(cls, ar, **flt):
        # ~ if ar.param_values.journal:
        # ~ pass
        pv = ar.param_values
        # if pv is None:
        #     raise Exception("No pv in %s" % ar)
        if pv.trade_type:
            flt.update(account=pv.trade_type.get_main_account(ar))
        if pv.partner:
            flt.update(partner=pv.partner)
        if pv.account:
            flt.update(account=pv.account)
        if pv.project:
            flt.update(project=pv.project)

        if pv.show_sepa == dd.YesNo.yes:
            flt.update(partner__sepa_accounts__primary=True)
        elif pv.show_sepa == dd.YesNo.no:
            flt.update(partner__sepa_accounts__primary__isnull=True)

        if pv.same_dc == dd.YesNo.yes:
            if cls.get_dc(
                    ar
            ) == DC.debit:  # 20201219 ExpectedMovements.get_data_rows()
                flt.update(amount__lt=0)
            else:
                flt.update(amount__gt=0)
        elif pv.same_dc == dd.YesNo.no:
            if cls.get_dc(
                    ar
            ) == DC.credit:  # 20201219 ExpectedMovements.get_data_rows()
                flt.update(amount__lt=0)
            else:
                flt.update(amount__gt=0)

        if pv.date_until is not None:
            flt.update(value_date__lte=pv.date_until)
        if pv.for_journal is not None:
            accounts = rt.models.accounting.Account.objects.filter(
                matchrule__journal=pv.for_journal).distinct()
            flt.update(account__in=accounts)
        if pv.from_journal is not None:
            flt.update(voucher__journal=pv.from_journal)
        flt = models.Q(**flt)
        if ar.quick_search:
            flt &= rt.models.contacts.Partner.quick_search_filter(
                ar.quick_search, prefix='partner__')

        return rt.models.accounting.get_due_movements(cls.get_dc(ar), flt)

    @classmethod
    def get_pk_field(self):
        return rt.models.accounting.Movement._meta.pk

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        # this is tricky.
        # for i in ar.data_iterator:
        #     if i.id == pk:
        #         return i
        # raise Exception("Not found: %s in %s" % (pk, ar))
        mvt = rt.models.accounting.Movement.objects.get(pk=pk)
        dm = rt.models.accounting.DueMovement(cls.get_dc(ar), mvt)
        dm.collect_all()
        return dm

    @dd.displayfield(_("Info"))
    def info(self, row, ar):
        elems = []
        if row.project:
            elems.append(ar.obj2html(row.project))
        if row.partner:
            elems.append(ar.obj2html(row.partner))
            # elems.append(row.partner.address)
        if row.bank_account:
            elems.append(ar.obj2html(row.bank_account))
        if row.account:
            elems.append(ar.obj2html(row.account))
        # return E.span(*join_elems(elems, ' / '))
        return E.span(*join_elems(elems, E.br))
        # return E.span(*elems)

    @dd.displayfield(_("Match"))
    def match(self, row, ar):
        return row.match

    @dd.virtualfield(
        models.DateField(
            _("Due date"),
            help_text=_("Due date of the eldest debt in this match group")))
    def due_date(self, row, ar):
        return row.due_date

    @dd.displayfield(_("Debts"),
                     help_text=_("List of invoices in this match group"))
    def debts(self, row, ar):
        return E.span(*join_elems([  # E.p(...) until 20150128
            ar.obj2html(i.voucher.get_mti_leaf()) for i in row.debts
        ]))

    @dd.displayfield(_("Payments"),
                     help_text=_("List of payments in this match group"))
    def payments(self, row, ar):
        return E.span(*join_elems([  # E.p(...) until 20150128
            ar.obj2html(i.voucher.get_mti_leaf()) for i in row.payments
        ]))

    @dd.virtualfield(dd.PriceField(_("Balance")))
    def balance(self, row, ar):
        return row.balance

    @dd.virtualfield(dd.ForeignKey('contacts.Partner'))
    def partner(self, row, ar):
        return row.partner

    @dd.virtualfield(dd.ForeignKey(project_model))
    def project(self, row, ar):
        return row.project

    @dd.virtualfield(dd.ForeignKey('accounting.Account'))
    def account(self, row, ar):
        return row.account

    @dd.virtualfield(
        dd.ForeignKey('sepa.Account', verbose_name=_("Bank account")))
    def bank_account(self, row, ar):
        return row.bank_account


class DebtsByAccount(ExpectedMovements):
    master = 'accounting.Account'

    @classmethod
    def get_data_rows(cls, ar, **flt):
        account = ar.master_instance
        if account is None:
            return []
        if not account.clearable:
            return []
        flt.update(cleared=False, account=account)
        # ignore trade_type to avoid overriding account
        ar.param_values.trade_type = None
        return super(DebtsByAccount, cls).get_data_rows(ar, **flt)


dd.inject_action('accounting.Account', due=dd.ShowSlaveTable(DebtsByAccount))


class DebtsByPartner(ExpectedMovements):
    master = 'contacts.Partner'
    # ~ column_names = 'due_date debts payments balance'

    @classmethod
    def get_dc(cls, ar=None):
        return DC.credit

    @classmethod
    def get_data_rows(cls, ar, **flt):
        partner = ar.master_instance
        if partner is None:
            return []
        flt.update(cleared=False, partner=partner)
        return super().get_data_rows(ar, **flt)


dd.inject_action('contacts.Partner', due=dd.ShowSlaveTable(DebtsByPartner))


class PartnerVouchers(Vouchers):
    editable = True

    parameters = dict(project=dd.ForeignKey(project_model,
                                            blank=True,
                                            null=True),
                      state=VoucherStates.field(blank=True),
                      partner=dd.ForeignKey('contacts.Partner',
                                            blank=True,
                                            null=True),
                      cleared=dd.YesNo.field(_("Show cleared vouchers"),
                                             blank=True),
                      **Vouchers.parameters)
    params_layout = "partner project state journal start_period end_period cleared"
    params_panel_hidden = True

    @classmethod
    def get_simple_parameters(cls):
        yield super().get_simple_parameters()
        yield 'partner'

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        qs = super().get_request_queryset(ar, **kwargs)
        # movement_set__partner=models.F('partner'))
        if (pv := ar.param_values) is None:
            return qs
        if pv.cleared == dd.YesNo.yes:
            qs = qs.exclude(accounting_movement_set_by_voucher__cleared=False)
        elif pv.cleared == dd.YesNo.no:
            qs = qs.filter(
                accounting_movement_set_by_voucher__cleared=False,
                accounting_movement_set_by_voucher__account__clearable=True)
        return qs


def mvtsum(**fkw):
    d = rt.models.accounting.Movement.objects.filter(**fkw).aggregate(
        models.Sum('amount'))
    return d['amount__sum'] or ZERO


class AccountBalances(dd.Table):
    editable = False
    required_roles = dd.login_required(AccountingReader)
    auto_fit_column_widths = True
    column_names = "description old_d old_c empty_column:1 during_d during_c empty_column:1 new_d new_c"
    default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    abstract = True
    params_panel_hidden = False
    use_as_default_table = False

    parameters = PeriodRangeParameters()
    params_layout = "start_period end_period"

    @classmethod
    def rowmvtfilter(self):
        raise NotImplementedError()

    @classmethod
    def get_request_queryset(self, ar, **kwargs):

        # see https://docs.djangoproject.com/en/5.2/ref/models/expressions/#using-aggregates-within-a-subquery-expression
        StoredPeriod = rt.models.periods.StoredPeriod
        if (pv := ar.param_values) is None:
            return qs
        sp = pv.start_period or StoredPeriod.get_or_create_from_date(
            dd.today())
        ep = pv.end_period or sp

        qs = super().get_request_queryset(ar)

        flt = self.rowmvtfilter(ar)
        oldflt = dict()
        oldflt.update(flt)
        duringflt = dict()
        duringflt.update(flt)
        during_periods = StoredPeriod.objects.filter(ref__gte=sp.ref,
                                                     ref__lte=ep.ref)
        before_periods = StoredPeriod.objects.filter(ref__lt=sp.ref)
        oldflt.update(voucher__accounting_period__in=before_periods)
        duringflt.update(voucher__accounting_period__in=during_periods)

        outer_link = self.model._meta.model_name

        def addann(kw, name, dc, flt):
            mvts = rt.models.accounting.Movement.objects.filter(dc=dc, **flt)
            mvts = mvts.order_by()
            mvts = mvts.values(outer_link)  # this was the important thing
            mvts = mvts.annotate(
                total=Sum('amount', output_field=dd.PriceField()))
            mvts = mvts.values('total')
            kw[name] = Subquery(mvts, output_field=dd.PriceField())

        kw = dict()
        addann(kw, 'old_d', DC.debit, oldflt)
        addann(kw, 'old_c', DC.credit, oldflt)
        addann(kw, 'during_d', DC.debit, duringflt)
        addann(kw, 'during_c', DC.credit, duringflt)

        qs = qs.annotate(**kw)

        qs = qs.exclude(old_d=ZERO, old_c=ZERO, during_d=ZERO, during_c=ZERO)

        # print("20170930 {}".format(qs.query))
        return qs

    @classmethod
    def new_balance(cls, row):
        return Balance(row.old_d, row.old_c) + Balance(row.during_d,
                                                       row.during_c)

    @classmethod
    def normal_dc(cls, row, ar):
        # raise NotImplementedError()
        return DC.debit  # row.normal_dc

    @dd.displayfield(_("Reference"))
    def ref(self, row, ar):
        return row.ref

    @dd.displayfield(_("Description"))
    def description(self, row, ar):
        # print(20180831, ar.renderer, ar.user)
        return row.as_summary_item(ar)

    @dd.virtualfield(dd.PriceField(_("Old balance")))
    def old_dc(self, row, ar):
        return Balance(row.old_d, row.old_c).value(self.normal_dc(row, ar))

    @dd.virtualfield(dd.PriceField(_("Movements")))
    def during_dc(self, row, ar):
        return Balance(row.during_d,
                       row.during_c).value(self.normal_dc(row, ar))

    @dd.virtualfield(dd.PriceField(_("New balance")))
    def new_dc(self, row, ar):
        return self.new_balance(row).value(self.normal_dc(row, ar))

    @dd.virtualfield(dd.PriceField(_("Debit before")))
    def old_d(self, row, ar):
        return Balance(row.old_d, row.old_c).d

    @dd.virtualfield(dd.PriceField(_("Credit before")))
    def old_c(self, row, ar):
        return Balance(row.old_d, row.old_c).c

    @dd.virtualfield(dd.PriceField(_("Debit")))
    def during_d(self, row, ar):
        return row.during_d

    @dd.virtualfield(dd.PriceField(_("Credit")))
    def during_c(self, row, ar):
        return row.during_c

    @dd.virtualfield(dd.PriceField(_("Debit after")))
    def new_d(self, row, ar):
        return self.new_balance(row).d

    @dd.virtualfield(dd.PriceField(_("Credit after")))
    def new_c(self, row, ar):
        return self.new_balance(row).c

    @dd.displayfield("", max_length=0)
    def empty_column(self, row, ar):
        return ''


class GeneralAccountBalances(AccountBalances, Accounts):

    label = _("General Account Balances")
    # model = 'accounting.Account'
    # order_by = ['group__ref', 'ref']
    order_by = ['ref']

    @classmethod
    def rowmvtfilter(self, ar):
        return dict(account=OuterRef('pk'))


# contacts = dd.resolve_app('contacts')
# from lino_xl.lib.contacts.ui import Partners
# print "20180831", dir(contacts)


# class PartnerBalancesByTradeType(AccountBalances, contacts.Partners):
#
#     order_by = ['name', 'id']
#     column_names = "description old_dc during_d during_c new_dc"
#
#     @classmethod
#     def get_title_base(self, ar):
#         return _("Partner Account Balances {}").format(ar.master_instance)
#
#     @classmethod
#     def rowmvtfilter(self, ar):
#         tt = ar.master_instance
#         if tt is None:
#             return
#         a = tt.get_main_account(ar)
#         return dict(partner=OuterRef('pk'), account=a)
#
#     @dd.displayfield(_("Ref"))
#     def ref(self, row, ar):
#         return str(row.pk)
#
#     @classmethod
#     def normal_dc(cls, row, ar):
#         tt = ar.master_instance
#         if tt is None:
#             return DC.debit
#         return tt.dc


# class CustomerAccountsBalance(PartnerAccountsBalance):
#     label = _("Customer Accounts Balance")
#     trade_type = TradeTypes.sales

# class SupplierAccountsBalance(PartnerAccountsBalance):
#     label = _("Supplier Accounts Balance")
#     trade_type = TradeTypes.purchases

##


class DebtorsCreditors(dd.VirtualTable):
    required_roles = dd.login_required(AccountingReader)
    auto_fit_column_widths = True
    column_names = "age due_date partner partner_id balance vouchers"
    default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    abstract = True

    parameters = mixins.Today()
    # params_layout = "today"

    d_or_c = NotImplementedError

    @classmethod
    def get_data_rows(self, ar):
        rows = []
        mi = ar.master_instance
        if mi is None:  # called directly from main menu
            if ar.param_values is None:
                return rows
            end_date = ar.param_values.today
        else:  # called from Situation report
            end_date = mi.today
        get_due_movements = rt.models.accounting.get_due_movements
        qs = rt.models.contacts.Partner.objects.order_by('name')
        for row in qs:
            row._balance = ZERO
            row._due_date = None
            row._expected = tuple(
                get_due_movements(
                    self.d_or_c, models.Q(partner=row,
                                          value_date__lte=end_date)))
            for dm in row._expected:
                row._balance += dm.balance
                if dm.due_date is not None:
                    if row._due_date is None or row._due_date > dm.due_date:
                        row._due_date = dm.due_date
                # logger.info("20140105 %s %s", row, dm)

            if row._balance > ZERO:
                rows.append(row)

        def k(a):
            return a._due_date

        rows.sort(key=k)
        return rows

    # @dd.displayfield(_("Partner"))
    # def partner(self, row, ar):
    #     return ar.obj2html(row)

    @dd.virtualfield(dd.ForeignKey('contacts.Partner'))
    def partner(self, row, ar):
        return row

    @dd.virtualfield(models.IntegerField(_("ID")))
    def partner_id(self, row, ar):
        return row.pk

    @dd.virtualfield(dd.PriceField(_("Balance")))
    def balance(self, row, ar):
        return row._balance

    @dd.virtualfield(models.DateField(_("Due date")))
    def due_date(self, row, ar):
        return row._due_date

    @dd.virtualfield(models.IntegerField(_("Age")))
    def age(self, row, ar):
        dd = ar.param_values.today - row._due_date
        return dd.days

    @dd.displayfield(_("Vouchers"))
    def vouchers(self, row, ar):
        matches = [dm.match for dm in row._expected]
        return E.span(', '.join(matches))

    # @dd.displayfield(_("Actions"))
    # def actions(self, row, ar):
    #     # TODO
    #     return E.span("[Show debts] [Issue reminder]")


class Debtors(DebtorsCreditors):
    label = _("Debtors")
    help_text = _("List of partners who are in debt towards us "
                  "(usually customers).")
    d_or_c = DC.debit  # 20201219 accounting.Creditors


class Creditors(DebtorsCreditors):
    label = _("Creditors")
    help_text = _("List of partners who are giving credit to us "
                  "(usually suppliers).")

    d_or_c = DC.credit  # 20201219 accounting.Creditors


##

# class Situation(Report):
#     """
#     A report consisting of the following tables:
#
#    -  :class:`Debtors`
#    -  :class:`Creditors`
#
#     """
#     label = _("Situation")
#     help_text = _("Overview of the financial situation on a given date.")
#     required_roles = dd.login_required(AccountingReader)
#
#     parameters = mixins.Today()
#
#     report_items = (Debtors, Creditors)

# class ActivityReport(Report):
#     """Overview of the financial activity during a given period.

#     A report consisting of the following tables:

#     - :class:`GeneralAccountsBalance`
#     - :class:`CustomerAccountsBalance`
#     - :class:`SupplierAccountsBalance`

#     """
#     label = _("Activity Report")
#     required_roles = dd.login_required(AccountingReader)

#     parameters = mixins.Yearly(
#         # include_vat = models.BooleanField(
#         #     verbose_name=dd.plugins.vat.verbose_name),
#     )

#     params_layout = "start_date end_date"
#     #~ params_panel_hidden = True

#     report_items = (
#         GeneralAccountsBalance,
#         CustomerAccountsBalance,
#         SupplierAccountsBalance)

# class AccountingReport(Report):
#     label = _("Accounting Report")
#     auto_apply_params = False
#     required_roles = dd.login_required(AccountingReader)
#     params_panel_hidden = False
#     parameters = PeriodRangeParameters(
#         with_general = models.BooleanField(
#             verbose_name=_("General accounts"), default=True),
#         with_balances = models.BooleanField(
#             verbose_name=_("Balance lists"), default=True),
#         with_activity = models.BooleanField(
#             verbose_name=_("Activity lists"), default=True))
#     build_method = 'appypdf'

#     @classmethod
#     def setup_parameters(cls, fields):
#         params_layout = """
#         start_period end_period with_balances with_activity with_general"""

#         if dd.is_installed('ana'):
#             k = 'with_analytic'
#             fields[k] = models.BooleanField(
#                 verbose_name=_("Analytic accounts"), default=True)
#             params_layout += ' ' + k

#         params_layout += '\n'
#         for tt in TradeTypes.get_list_items():
#             k = 'with_'+tt.name
#             fields[k] = models.BooleanField(
#                 verbose_name=tt.text, default=True)
#             params_layout += ' ' + k
#         # params_layout += ' go_button'
#         cls.params_layout = params_layout
#         super(AccountingReport, cls).setup_parameters(fields)

#     @classmethod
#     def get_story(cls, self, ar):
#         pv = ar.param_values
#         cls.check_params(pv)
#         # if not pv.start_period:
#         #     yield E.p(gettext("Select at least a start period"))
#         #     return
#         bpv = dict(start_period=pv.start_period, end_period=pv.end_period)
#         balances = []
#         if pv.with_general:
#             balances.append(ar.spawn(
#                 GeneralAccountBalances, param_values=bpv))
#         if dd.is_installed('ana'):
#             if pv.with_analytic:
#                 balances.append(ar.spawn(
#                     rt.models.ana.AnalyticAccountBalances,
#                     param_values=bpv))
#         for tt in TradeTypes.get_list_items():
#             k = 'with_'+tt.name
#             if pv[k]:
#                 balances.append(ar.spawn(
#                     PartnerBalancesByTradeType,
#                     master_instance=tt, param_values=bpv))
#         # if pv.with_sales:
#         #     balances.append(CustomerAccountsBalance)
#         # if pv.with_purchases:
#         #     balances.append(SupplierAccountsBalance)
#         if pv.with_balances:
#             for sar in balances:
#                 yield E.h1(str(sar.get_title()))
#                 yield sar
#                 # yield E.h1(B.label)
#                 # yield B.create_request(param_values=bpv)


class Movements(dd.Table):
    # only MovementsByPartner is editable (and only the match field)
    editable = False
    model = 'accounting.Movement'
    required_roles = dd.login_required(LedgerUser)
    column_names = 'value_date voucher_link description \
    debit credit match_link cleared *'

    sum_text_column = 2
    order_by = ['id']

    parameters = mixins.ObservedDateRange(
        year=dd.ForeignKey('periods.StoredYear', blank=True),
        journal_group=JournalGroups.field(blank=True),
        partner=dd.ForeignKey('contacts.Partner', blank=True, null=True),
        project=dd.ForeignKey(project_model,
                              blank=True,
                              null=True),
        account=dd.ForeignKey('accounting.Account', blank=True, null=True),
        journal=JournalRef(blank=True),
        cleared=dd.YesNo.field(_("Show cleared movements"), blank=True))
    params_layout = """
    start_period end_period start_date end_date cleared
    journal_group journal year project partner account"""

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        qs = super(Movements, cls).get_request_queryset(ar, **kwargs)

        if (pv := ar.param_values) is None:
            return qs
        if pv.cleared == dd.YesNo.yes:
            qs = qs.filter(cleared=True)
        elif pv.cleared == dd.YesNo.no:
            qs = qs.filter(cleared=False)

        if pv.start_date:
            qs = qs.filter(value_date__gte=pv.start_date)
        if pv.end_date:
            qs = qs.filter(value_date__lte=pv.end_date)

        # if ar.param_values.partner:
        #     qs = qs.filter(partner=ar.param_values.partner)
        # if ar.param_values.paccount:
        #     qs = qs.filter(account=ar.param_values.paccount)
        if pv.year:
            qs = qs.filter(voucher__fiscal_year=pv.year)
        if pv.journal_group:
            qs = qs.filter(voucher__journal__journal_group=pv.journal_group)
        if pv.journal:
            qs = qs.filter(voucher__journal=pv.journal)
        return qs

    @classmethod
    def get_sum_text(self, ar, sums):
        bal = sums['debit'] - sums['credit']
        return _("Balance {1} ({0} movements)").format(ar.get_total_count(),
                                                       bal)

    @classmethod
    def get_simple_parameters(cls):
        p = list(super().get_simple_parameters())
        p.append('partner')
        p.append('project')
        # p.append('journal_group')
        # p.append('year')
        p.append('account')
        return p

    @classmethod
    def get_title_tags(cls, ar):
        for t in super().get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.journal is not None:
            yield pv.journal.ref
        if pv.journal_group is not None:
            yield str(pv.journal_group)
        if pv.year is not None:
            yield str(pv.year)
        if pv.cleared == dd.YesNo.no:
            yield str(_("only uncleared"))
        elif pv.cleared == dd.YesNo.yes:
            yield str(_("only cleared"))

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        # raise Exception("20191003")
        if ar is None:
            return ''
        elems = []
        elems.append(ar.obj2html(self.account))
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
        if self.project:
            elems.append(ar.obj2html(self.project))
        return E.p(*join_elems(elems, " / "))


class AllMovements(Movements):
    required_roles = dd.login_required(LedgerStaff)


class MovementsByVoucher(Movements):
    # master = 'accounting.Voucher'
    master_key = 'voucher'
    column_names = 'account project partner debit credit match_link cleared *'
    sum_text_column = 3
    # auto_fit_column_widths = True
    default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    order_by = dd.plugins.accounting.remove_dummy('seqno', 'value_date',
                                                  'account__ref', 'partner',
                                                  'project', 'id')


class MovementsByPartner(Movements):
    editable = True
    allow_create = False
    master_key = 'partner'
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    # auto_fit_column_widths = True
    # order_by = ['-value_date', 'voucher__id', 'account__ref']
    order_by = dd.plugins.accounting.remove_dummy('-value_date', 'voucher__id',
                                                  'account__ref', 'project', 'id')
    column_names = 'value_date voucher_link description \
    debit credit match cleared *'

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        # kw.update(cleared=dd.YesNo.no)
        kw.update(year=None)
        return kw

    @classmethod
    def setup_request(self, ar):
        ar.no_data_text = _("No uncleared movements")

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        # raise Exception("20191003")
        if ar is None:
            return ''
        elems = []
        elems.append(ar.obj2html(self.account))
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
            # if voucher.narration:
            #     elems.append(voucher.narration)
            # p = voucher.get_partner()
            # if p is not None and p != ar.master_instance:
            #     elems.append(ar.obj2html(p))
        if self.project:
            elems.append(ar.obj2html(self.project))
        return E.p(*join_elems(elems, " | "))

    @classmethod
    def table_as_summary(cls, ar):
        elems = []
        ar.param_values.cleared = dd.YesNo.no
        ar.clear_cached_status()
        bal = ZERO
        for mvt in ar:
            bal += mvt.amount
        txt = _("{0} open movements ({1} {2})").format(
            ar.get_total_count(), bal, dd.plugins.accounting.currency_symbol)

        elems.append(ar.href_to_request(ar, txt))
        return tostring(elems)


class MyMovements(Movements):
    editable = True
    allow_create = False
    label = _("My movements")
    required_roles = dd.login_required(LedgerPartner)
    column_names = 'value_date voucher_link debit credit match cleared *'
    order_by = dd.plugins.accounting.remove_dummy('-value_date', 'voucher__id',
                                                  'account__ref', 'project', 'id')
    params_layout = """
    start_period end_period start_date end_date cleared"""

    @classmethod
    def get_filter_kw(self, ar, **kw):
        p = ar.get_user().partner
        if p is None:
            return None
        kw.update(partner=p)
        return super().get_filter_kw(ar, **kw)


class MovementsByProject(MovementsByPartner):
    editable = False
    column_names = 'value_date voucher_link description \
    debit credit match_link cleared *'

    master_key = 'project'
    default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    order_by = ['-value_date', 'partner', 'id']

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(MovementsByPartner, cls).param_defaults(ar, **kw)
        kw.update(cleared=dd.YesNo.no)
        kw.update(year=None)
        return kw

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        # raise Exception("20191003")
        if ar is None:
            return ''
        elems = []
        elems.append(ar.obj2html(self.account))
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
        return E.p(*join_elems(elems, " / "))


class MovementsByAccount(Movements):
    master_key = 'account'
    column_names = 'value_date voucher_link description \
    debit credit match_link *'

    # order_by = ['-value_date']
    # auto_fit_column_widths = True
    default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    # order_by = ['-value_date', 'account__ref', 'project', 'id']
    order_by = dd.plugins.accounting.remove_dummy('-value_date', 'partner__name',
                                                  'project', 'id')

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        if ar.master_instance is not None and ar.master_instance.clearable:
            kw.update(cleared=dd.YesNo.no)
            kw.update(year=None)
        return kw

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        if ar is None:
            return ''
        elems = []
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
        if self.project:
            elems.append(ar.obj2html(self.project))
        return E.p(*join_elems(elems, " / "))


class MovementsByMatch(Movements):
    column_names = 'value_date voucher_link description '\
                   'debit credit cleared *'
    master = str  # 'accounting.Matching'
    variable_row_height = True
    order_by = dd.plugins.accounting.remove_dummy('-value_date', 'account__ref',
                                                  'project', 'id')

    details_of_master_template = _("%(details)s matching '%(master)s'")

    @classmethod
    def get_master_instance(self, ar, model, pk):
        """No database lookup, just return the primary key"""
        # if not pk:
        #     return None
        return pk

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        qs = super(MovementsByMatch, cls).get_request_queryset(ar, **kwargs)
        qs = qs.filter(match=ar.master_instance)
        return qs

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        if ar is None:
            return ''
        elems = []
        elems.append(ar.obj2html(self.account))
        if self.voucher.narration:
            elems.append(self.voucher.narration)
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
        if self.project:
            elems.append(ar.obj2html(self.project))
        return E.p(*join_elems(elems, " / "))
