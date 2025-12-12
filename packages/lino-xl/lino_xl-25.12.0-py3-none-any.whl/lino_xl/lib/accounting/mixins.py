# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
# from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError

from lino.utils import SumCollector
from lino.mixins import Sequenced
from lino.mixins.registrable import Registrable
from lino.modlib.periods.mixins import PeriodRangeObservable
from lino.api import dd, rt, _
# from lino.core import constants
from lino.core.keyboard import Hotkey
from lino_xl.lib.contacts.mixins import PartnerRelated
from lino_xl.lib.accounting.choicelists import TradeTypes

from .choicelists import TradeTypes
from .roles import LedgerUser

project_model = dd.get_plugin_setting('accounting', 'project_model', None)
has_payment_methods = dd.get_plugin_setting('accounting', 'has_payment_methods',
                                            False)


class ToggleState(dd.Action):
    # show_in_toolbar = False
    # button_text = _("Toggle state")
    # sort_index = 52
    label = _("Toggle state")
    # action_name = "changemystate"
    # button_text = "⏼" # 23FC Toggle power
    # button_text = "⇄" # 21c4
    # button_text = "⇌" # 21cc
    button_text = "⇅"  # 21c5
    hotkey = Hotkey('x', code="KeyX", ctrl=True)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        fld = ar.actor.workflow_state_field
        chl = fld.choicelist  # VoucherStates
        # print("20190722", obj)
        if obj.state == chl.draft:
            obj.set_workflow_state(ar, fld, chl.registered)
        elif obj.state == chl.registered:
            obj.set_workflow_state(ar, fld, chl.draft)
        else:
            raise Warning(_("Cannot toggle from state {}").format(obj.state))
        # obj.full_clean()
        # obj.save()
        ar.set_response(refresh=True)


class LedgerRegistrable(Registrable):

    class Meta:
        abstract = True

    toggle_state = ToggleState()
    hide_editable_number = True

    def __str__(self):
        # if not isinstance(dd.plugins.accounting.registered_states, tuple):
        #     raise Exception("registered_states is {}".format(dd.plugins.accounting.registered_states))
        # if not isinstance(self.state, dd.plugins.accounting.registered_states):
        if self.hide_editable_number and self.state.is_editable:
            # raise Exception("20191223 {} is not in {}".format(self.state, dd.plugins.accounting.registered_states))
            return "({0} #{1})".format(self._meta.verbose_name, self.id)
            # return "{0} #{1}".format(self.journal.ref, self.id)
        return super().__str__()

    def get_wanted_movements(self, ar=None):
        # deactivated this because MRO is complex, see 20200128
        # reactivated 20240116 because SLS didn't generate storage movements
        return []
        # raise NotImplementedError(
        #     "{} must define get_wanted_movements()".format(self.__class__))

    def after_state_change(self, ar, oldstate, newstate):
        # Movements are created *after* having changed the state because
        # otherwise the match isn't correct.
        if newstate.name == 'draft':
            self.deregister_voucher(ar)
        elif newstate.name == 'registered':
            self.register_voucher(ar)
        super().after_state_change(ar, oldstate, newstate)

    def register_voucher(self, ar=None, do_clear=True):
        """
        Delete any existing movements and re-create them.
        """

        # dd.logger.info("20151211 cosi.Voucher.register_voucher()")
        # self.year = StoredYears.get_or_create_from_date(self.entry_date)
        # dd.logger.info("20151211 accounting_movement_set_by_voucher.all().delete()")

        # if self.number is None:
        #     self.number = self.journal.get_next_number(self)

        def doit(partners, products):
            seqno = 0
            # dd.logger.info("20151211 gonna call get_wanted_movements(ar)")
            movements = self.get_wanted_movements(ar)
            # dd.logger.info("20151211 gonna save %d movements", len(movements))
            # self.full_clean()
            # self.save()

            fcu = dd.plugins.accounting.suppress_movements_until
            for m in movements:
                # don't create movements before suppress_movements_until
                if fcu and m.value_date <= fcu:
                    continue
                # if we don't set seqno, Sequenced.full_clean will do
                # it, but at the price of an additional database
                # lookup.
                seqno += 1
                m.seqno = seqno
                # m.cleared = True
                try:
                    m.full_clean()
                except ValidationError as e:
                    dd.logger.warning("20181116 %s : %s", e, dd.obj2str(m))
                    return
                m.save()
                if m.partner:
                    partners.add(m.partner)
                if m.product and m.product.storage_management:
                    products.add(m.product)
                # print("20230614 saved movement:", m, m.partner, m.product)
            if settings.SITE._history_aware_logging:
                dd.logger.debug("Register %s (%d movements, %d partners)",
                                self, seqno, len(partners))

        self.do_and_clear(doit, do_clear)

    def deregister_voucher(self, ar, do_clear=True):

        def doit(partners, products):
            if settings.SITE._history_aware_logging:
                dd.logger.info("Deregister %s (%d partners)", self,
                               len(partners))

        self.do_and_clear(doit, do_clear)


class ProjectRelated(dd.Model):

    class Meta:
        abstract = True

    project = dd.ForeignKey(
        project_model,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_set_by_project")

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        if project_model:
            yield 'project'


class PaymentRelated(PartnerRelated):

    class Meta:
        abstract = True

    payment_term = dd.ForeignKey(
        'accounting.PaymentTerm',
        related_name="%(app_label)s_%(class)s_set_by_payment_term",
        blank=True,
        null=True)

    if has_payment_methods:
        payment_method = dd.ForeignKey('accounting.PaymentMethod',
                                       blank=True,
                                       null=True)
    else:
        payment_method = dd.DummyField(())

    def get_payment_term(self):
        return self.payment_term

    # def get_trade_type(self):
    #     return TradeTypes.sales

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        yield 'payment_term'

    def full_clean(self, *args, **kw):
        self.fill_defaults()
        super().full_clean(*args, **kw)

    def fill_defaults(self):
        if dd.is_installed('trading') and not self.payment_term_id and self.partner_id:
            tt = self.get_trade_type()
            obj = self.partner.get_trading_rule(tt)
            self.payment_term = obj.payment_term
            if self.payment_term:
                self.payment_term_changed()
        if has_payment_methods:
            if not self.payment_method:
                self.payment_method = rt.models.accounting.PaymentMethod.objects.order_by(
                    'id').first()
                # self.payment_method = rt.models.accounting.PaymentMethod.objects.filter(
                #     Q(journal__isnull=True)|Q(journal=self.journal)).order_by('id').first()

    def payment_term_changed(self, ar=None):
        if self.payment_term:
            self.due_date = self.payment_term.get_due_date(self.entry_date)


class Payable(LedgerRegistrable):

    class Meta:
        abstract = True

    your_ref = models.CharField(_("Your reference"),
                                max_length=200,
                                blank=True)
    due_date = models.DateField(_("Due date"), blank=True, null=True)

    def get_payment_term(self):
        return None

    def full_clean(self):
        if not self.due_date:
            payment_term = self.get_payment_term()
            if payment_term:
                self.due_date = payment_term.get_due_date(self.voucher_date
                                                          or self.entry_date)
        # super(Payable, self).full_clean()
        super().full_clean()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        yield 'your_ref'

    def get_due_date(self):
        return self.due_date or self.voucher_date

    def get_payable_sums_dict(self, ar=None):
        raise NotImplemented()

    def get_movement_description(self, mvt, ar=None):
        for chunk in super().get_movement_description(mvt, ar):
            yield chunk
        if self.your_ref:
            yield self.your_ref

    def get_wanted_movements(self, ar=None):
        for mvt in super().get_wanted_movements(ar):
            yield mvt

        if not self.journal.make_ledger_movements:
            return

        item_sums = self.get_payable_sums_dict(ar)
        # logger.info("20120901 get_wanted_movements %s", sums_dict)
        counter_sums = SumCollector()
        partner = self.get_partner()
        payment_term = self.get_payment_term()
        has_vat = dd.is_installed('vat')
        kw = dict()
        for k, amount in item_sums.items():
            # amount = myround(amount)
            # first item of each tuple k is itself a tuple (account, ana_account)
            acc_tuple, prj, vat_class, vat_regime = k
            account, ana_account = acc_tuple
            # if not isinstance(acc_tuple, tuple):
            #     raise Exception("Not a tuple: {}".format(acc_tuple))
            if not isinstance(account, rt.models.accounting.Account):
                raise Exception("Not an account: {}".format(account))
            if has_vat:
                kw.update(vat_class=vat_class, vat_regime=vat_regime)

            if account.needs_partner:
                kw.update(partner=partner)
            amount = self.journal.dc.normalized_amount(amount)
            if payment_term is None or not payment_term.informal:
                yield self.create_ledger_movement(None, acc_tuple, prj, amount, **kw)
            counter_sums.collect(prj, amount)

        tt = self.get_trade_type()
        if tt is None:
            if len(counter_sums.items()):
                raise Warning("No trade type for {}".format(self))
            return
        acc = self.get_trade_type().get_main_account(ar)
        if acc is None:
            if len(counter_sums.items()):
                raise Warning("No main account for {}".format(tt))
            return

        kwargs = dict(match=self.get_match())
        if acc.needs_partner:
            kwargs.update(partner=partner)
        total_amount = 0
        for prj, amount in counter_sums.items():
            total_amount += amount
            yield self.create_ledger_movement(
                None, (acc, None), prj, -amount, **kwargs)

        if payment_term is not None:
            if payment_term.informal:
                # a movement to balance the partner movement
                if payment_term.payer:
                    kwargs.update(partner=payment_term.payer)
                    yield self.create_ledger_movement(
                        None, (TradeTypes.clearings.get_main_account(ar), None),
                        None, total_amount, **kwargs)
                else:
                    yield self.create_ledger_movement(
                        None, (acc, None), None, total_amount, **kwargs)
            elif payment_term.payer:
                # one movement to clear the credit that was booked to the partner account,
                # another movment to book it to the payer's account:
                yield self.create_ledger_movement(
                    None, (acc, None), None, total_amount, **kwargs)
                kwargs.update(partner=payment_term.payer)
                yield self.create_ledger_movement(
                    None, (TradeTypes.clearings.get_main_account(ar), None),
                    None, -total_amount, **kwargs)


class Matching(dd.Model):

    class Meta:
        abstract = True

    match = dd.CharField(_("Match"),
                         max_length=20,
                         blank=True,
                         help_text=_("The movement to be matched."))

    @classmethod
    def get_match_choices(cls, journal, partner, **fkw):
        """This is the general algorithm.
        """
        matchable_accounts = rt.models.accounting.Account.objects.filter(
            matchrule__journal=journal)
        fkw.update(account__in=matchable_accounts)
        fkw.update(cleared=False)
        if partner:
            fkw.update(partner=partner)
        qs = rt.models.accounting.Movement.objects.filter(**fkw)
        qs = qs.order_by('value_date')
        # qs = qs.distinct('match')
        return qs.values_list('match', flat=True)

    @dd.chooser(simple_values=True)
    def match_choices(cls, journal, partner):
        # todo: move this to implementing classes?
        return cls.get_match_choices(journal, partner)

    def get_match(self):
        # return self.match or self.get_default_match()
        return self.match or self  # 20191226


class VoucherItem(dd.Model):

    allow_cascaded_delete = ['voucher']

    class Meta:
        abstract = True

    @classmethod
    def disable_create(cls, ar):
        mi = ar.master_instance
        if mi is None:
            return _("No master instance")
        if not mi.state.is_editable:
            return _("Voucher is not editable")
        return super().disable_create(ar)

    def get_row_permission(self, ar, state, ba):
        if not ba.action.readonly:
            if self.voucher_id:
                if not self.voucher.state.is_editable:
                    return False
        return super().get_row_permission(ar, state, ba)

    def get_ana_account(self):
        return None


class SequencedVoucherItem(VoucherItem, Sequenced):

    class Meta:
        abstract = True

    def get_siblings(self):
        return self.voucher.items.all()

    def __str__(self):
        return str(self.voucher) + "#" + str(self.seqno)
        # return super().__str__()


class AccountVoucherItem(SequencedVoucherItem):

    class Meta:
        abstract = True

    account = dd.ForeignKey(
        'accounting.Account',
        related_name="%(app_label)s_%(class)s_set_by_account")

    def get_base_account(self, tt, ar=None):
        return self.account

    @dd.chooser()
    def account_choices(self, voucher):
        if voucher and voucher.journal:
            return voucher.journal.get_allowed_accounts()
        return rt.models.accounting.Account.objects.none()


# def set_partner_invoice_account(sender, instance=None, **kwargs):
#     if instance.account:
#         return
#     if not instance.voucher:
#         return
#     p = instance.voucher.partner
#     if not p:
#         return
#     tt = instance.voucher.get_trade_type()
#     instance.account = tt.get_partner_invoice_account(p)

# @dd.receiver(dd.post_analyze)
# def on_post_analyze(sender, **kw):
#     for m in rt.models_by_base(AccountVoucherItem):
#         dd.post_init.connect(set_partner_invoice_account, sender=m)


def JournalRef(**kw):
    # ~ kw.update(blank=True,null=True) # Django Ticket #12708
    kw.update(related_name="%(app_label)s_%(class)s_set_by_journal")
    return dd.ForeignKey('accounting.Journal', **kw)


def VoucherNumber(*args, **kwargs):
    return models.IntegerField(*args, **kwargs)


class ItemsByVoucher(dd.Table):
    label = _("Content")
    required_roles = dd.login_required(LedgerUser)
    master_key = 'voucher'
    order_by = ["seqno"]
    auto_fit_column_widths = True
    # display_mode = ((None, constants.DISPLAY_MODE_HTML),)
    preview_limit = 0
    abstract = True


class VoucherRelated(dd.Model):
    # This is also used by peppol.OutboundDocument
    # Defines virtual fields voucher_link and voucher_partner. The
    # implementing class must itself provide the voucher field, which is either
    # a ForeignKey or a OneToOneField.

    class Meta:
        abstract = True

    def select_text(self):
        v = self.voucher.get_mti_leaf()
        # v = self.voucher
        if v is None:
            return str(self.voucher)
        return "%s (%s)" % (v, v.entry_date)

    @dd.displayfield(_("Voucher"),
                     sortable_by=[
                         'voucher__journal__ref',
                         'voucher__fiscal_year', 'voucher__number'
                     ])
    def voucher_link(self, ar):
        if ar is None:
            return ''
        return ar.obj2html(self.voucher.get_mti_leaf())
        # return ar.obj2html(self.voucher)

    @dd.displayfield(_("Voucher partner"))
    def voucher_partner(self, ar):
        if ar is None:
            return ''
        voucher = self.voucher.get_mti_leaf()
        # voucher = self.voucher
        if voucher is None:
            return ''
        p = voucher.get_partner()
        if p is None:
            return ''
        return ar.obj2html(p)


class MovementBase(VoucherRelated, PeriodRangeObservable):

    class Meta:
        abstract = True

    allow_cascaded_delete = ['voucher']
    observable_period_prefix = 'voucher__'
    product = None  # 20230617

    voucher = dd.ForeignKey(
        'accounting.Voucher',
        related_name="%(app_label)s_%(class)s_set_by_voucher")
    seqno = models.IntegerField(_("Seq.No."))
    partner = dd.ForeignKey(
        'contacts.Partner',
        related_name="%(app_label)s_%(class)s_set_by_partner",
        blank=True,
        null=True)
    value_date = models.DateField(_("Value date"), null=True, blank=True)
    match = models.CharField(_("Match"), blank=True, max_length=20)
    cleared = models.BooleanField(_("Cleared"), default=False)

    def __str__(self):
        return "%s.%d" % (str(self.voucher), self.seqno)


MovementBase.set_widget_options('voucher_link', width=12)
