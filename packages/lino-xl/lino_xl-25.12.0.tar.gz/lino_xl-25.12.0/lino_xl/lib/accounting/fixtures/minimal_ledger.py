# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino_xl.lib.accounting.choicelists import DC, CommonAccounts
# from lino_xl.lib.invoicing.mixins import InvoicingAreas
# from lino.utils import Cycler
# from django.contrib.contenttypes.models import ContentType
from lino_xl.lib.invoicing.utils import invoicing_task, invoicing_rule

vat = dd.resolve_app('vat')
trading = dd.resolve_app('trading')
accounting = dd.resolve_app('accounting')
finan = dd.resolve_app('finan')
bevat = dd.resolve_app('bevat')
eevat = dd.resolve_app('eevat')
bevats = dd.resolve_app('bevats')
# ~ partners = dd.resolve_app('partners')
has_payment_methods = dd.get_plugin_setting('accounting', 'has_payment_methods',
                                            False)

# def m2ct(m):
#     return ContentType.objects.get_for_model(m)
#
# def make_rule(it, m, **kwargs):
#     return rt.models.invoicing.FollowUpRule(
#         invoicing_task=it, invoice_generator=m2ct(m), **kwargs)


def objects():

    JournalGroups = rt.models.accounting.JournalGroups
    Company = rt.models.contacts.Company

    # JOURNALS

    kw = dict(journal_group=JournalGroups.sales)
    if trading:
        # MODEL = trading.VatProductInvoice
        MODEL = trading.InvoicesByJournal
    else:
        MODEL = vat.InvoicesByJournal
    kw.update(trade_type='sales')

    kw.update(ref="SLS", dc=DC.credit)
    kw.update(dd.str2kw('printed_name', _("Invoice")))
    # kw.update(dd.str2kw('name', _("Sales invoices")))
    kw.update(dd.str2kw('name', _("Sales invoices")))
    # 20240119
    # if dd.is_installed("invoicing"):
    #     kw.update(invoicing_area='default')
    if dd.is_installed("storage"):
        kw.update(make_storage_movements=True)
    # if dd.is_installed('invoicing'):
    #     kw.update(invoicing_area=InvoicingAreas.default)
    SLS_JOURNAL = MODEL.create_journal(**kw)
    # if dd.is_installed('peppol'):
    #     if dd.plugins.peppol.outbound_model:
    yield SLS_JOURNAL
    # if dd.is_installed("invoicing"):
    #
    #     it = rt.models.invoicing.Task(target_journal=SLS_JOURNAL)
    #         # **dd.str2kw("designation", _("Invoicing")))
    #     yield it
    #     # InvoicingAreas.add_item('sales', _("Invoicing"), 'default',
    #     #     voucher_model=VatProductInvoice, voucher_item=InvoiceItem)
    #     yield make_rule(it, rt.models.trading.InvoiceItem)
    #     if dd.is_installed("storage"):
    #         yield make_rule(it, rt.models.storage.Filler)
    #     if dd.is_installed("courses"):
    #         yield make_rule(it, rt.models.courses.Enrolment)
    #         yield make_rule(it, rt.models.courses.Course)
    #     if dd.is_installed("rooms"):
    #         yield make_rule(it, rt.models.rooms.Booking)

    if dd.is_installed('subscriptions'):
        kw.update(ref="SUB", dc=DC.credit)
        kw.update(dd.str2kw('name', _("Subscription invoices")))
        kw.update(dd.str2kw('printed_name', _("Subscription invoice")))
        kw.update(make_ledger_movements=True)
        if dd.is_installed("storage"):
            kw.update(make_storage_movements=True)
        # 20240119
        # if dd.is_installed("invoicing"):
        #     kw.update(invoicing_area='subscriptions')
        yield trading.InvoicesByJournal.create_journal(**kw)
        # if dd.is_installed("invoicing"):
        #     it = rt.models.invoicing.Task(target_journal=PSI_JOURNAL,
        #         max_date_offset=7, today_offset=0)
        #         # **dd.str2kw("designation", _("Subscriptions")))
        #     yield it
        #     yield make_rule(it, rt.models.subscriptions.SubscriptionPeriod)
        # kw.pop('invoicing_area', None)
        kw.pop('make_ledger_movements', None)

    if dd.is_installed('working'):
        kw.update(ref="SRV", dc=DC.debit)
        kw.update(dd.str2kw('name', _("Service reports")))
        kw.update(dd.str2kw('printed_name', _("Service report")))
        kw.update(make_ledger_movements=False)
        if dd.is_installed("storage"):
            kw.update(make_storage_movements=True)
        # 20240119
        # if dd.is_installed("invoicing"):
        #     kw.update(invoicing_area='reporting')
        SRV_JOURNAL = rt.models.storage.DeliveryNotesByJournal.create_journal(**kw)
        yield SRV_JOURNAL
        # if dd.is_installed("invoicing"):
        #     it = rt.models.invoicing.Task(target_journal=SRV_JOURNAL)
        #         # **dd.str2kw("designation", _("Reporting")))
        #     yield it
        #     yield make_rule(it, rt.models.working.Session)
        # kw.pop('invoicing_area', None)
        kw.pop('make_ledger_movements', None)

    # if dd.is_installed('invoicing') and dd.plugins.invoicing.delivery_notes_demo:
    # stories_journal = dd.plugins.accounting.sales_stories_journal
    sales_method = dd.plugins.accounting.sales_method
    if sales_method and sales_method != 'direct':
        misc_partner = rt.models.contacts.Company(
            name="Miscellaneous",
            country=dd.plugins.countries.get_my_country())
        yield misc_partner
        kw.update(partner=misc_partner)
        # kw.update(invoicing_area=InvoicingAreas.delivered)
        if sales_method == "delivery":
            kw.update(ref="SDN", dc=DC.credit)
            kw.update(dd.str2kw('printed_name', _("Delivery note")))
            kw.update(dd.str2kw('name', _("Delivery notes")))
            kw.update(make_ledger_movements=False)
            if dd.is_installed("storage"):
                kw.update(make_storage_movements=True)
        elif sales_method == "pos":
            # kw.pop('invoicing_area', None)
            kw.update(ref="SSN", dc=DC.credit)
            kw.update(dd.str2kw('printed_name', _("Sales note")))
            kw.update(dd.str2kw('name', _("Sales notes")))
            kw.update(make_ledger_movements=True)
            if dd.is_installed("storage"):
                kw.update(make_storage_movements=True)
        else:
            raise Exception("Unsupported sales method {}".format(sales_method))
        SDN_JOURNAL = trading.CashInvoicesByJournal.create_journal(**kw)
        yield SDN_JOURNAL
        kw.pop('make_ledger_movements', None)
        kw.pop('make_storage_movements', None)
        if sales_method == "delivery" and dd.is_installed("invoicing"):
            yield invoicing_task(SLS_JOURNAL, user_id=1)
            yield invoicing_rule(SLS_JOURNAL,
                                 rt.models.trading.InvoiceItem,
                                 source_journal=SDN_JOURNAL)
            # it = rt.models.invoicing.Task(target_journal=SLS_JOURNAL)
            #     # **dd.str2kw("designation", _("Invoicing")))
            # yield it
            # yield make_rule(it, rt.models.trading.InvoiceItem, source_journal=SDN_JOURNAL)
        # yield PaymentMethod(designation=_("Cash payment"), journal=SDN_JOURNAL)

    if has_payment_methods:

        PaymentMethod = rt.models.accounting.PaymentMethod

        def payment_method(designation, payment_account, **kwargs):
            if payment_account:
                kwargs.update(payment_account=CommonAccounts.get_by_name(
                    payment_account).get_object())
            # kwargs.update(journal=SLS_JOURNAL)
            return PaymentMethod(
                **dd.str2kw('designation', designation, **kwargs))

        yield payment_method(_("Cash payment"), "cash", is_cash=True)
        yield payment_method(_("PayPal"), "online_payments")
        yield payment_method(_("bKash"), "online_payments")
        # yield payment_method(_("Cash on delivery"), "cash")

    if dd.plugins.vat.declaration_plugin is None:
        dd.logger.warning(
            "No journal SLC, BNK, PMO etc because declaration_plugin is None")
        return

    # kw.pop('invoicing_area', None)
    kw.pop('make_storage_movements', None)

    kw.update(ref="SLC", dc=DC.debit)
    kw.update(dd.str2kw('name', _("Sales credit notes")))
    kw.update(dd.str2kw('printed_name', _("Credit note")))
    yield MODEL.create_journal(**kw)

    kw.update(journal_group=JournalGroups.purchases)
    kw.update(trade_type='purchases', ref="PRC")
    kw.update(dd.str2kw('name', _("Purchase invoices")))
    kw.update(dd.str2kw('printed_name', _("Invoice")))
    kw.update(dc=DC.debit)
    if dd.is_installed('ana'):
        yield rt.models.ana.InvoicesByJournal.create_journal(**kw)
    else:
        yield vat.InvoicesByJournal.create_journal(**kw)
        # yield vat.VatAccountInvoice.create_journal(**kw)

    if finan:

        if True:
            country = dd.plugins.countries.get_my_country()
            kw = dict()
        else:
            city = rt.models.countries.Place.objects.filter(name="Brussels").first()
            country = rt.models.countries.Country.objects.get(isocode="BE")
            kw = dict(
                street="rue de la Monnaie", street_no="1", city=city, zip_code="1234"
            )

        bestbank = Company(name="Bestbank", country=country, **kw)

        # if dd.is_installed('vat'):
        #     bestbank.vat_id = "BE 0123.456.749"
        yield bestbank

        kw = dict(journal_group=JournalGroups.financial)
        kw.update(dd.str2kw('name', _("Payment orders Bestbank")))
        kw.update(dd.str2kw('printed_name', _("Payment order")))
        # kw.update(dd.babel_values(
        #     'name', de="Zahlungsaufträge", fr="Ordres de paiement",
        #     en="Payment Orders", et="Maksekorraldused"))
        kw.update(trade_type='bank_po',
                  partner=bestbank,
                  account=CommonAccounts.pending_po.get_object(),
                  ref="PMO")
        kw.update(dc=DC.credit)  # 20201219  PMO Journal.dc
        yield finan.PaymentOrdersByJournal.create_journal(**kw)

        kw = dict(journal_group=JournalGroups.financial)
        # kw.update(trade_type='')
        kw.update(dc=DC.credit)
        kw.update(account=CommonAccounts.cash.get_object(), ref="CSH")
        kw.update(dd.str2kw('name', _("Cash book")))
        kw.update(dd.str2kw('printed_name', _("Cash statement")))
        yield finan.BankStatementsByJournal.create_journal(**kw)

        kw.update(dd.str2kw('name', _("Bestbank")))
        kw.update(dd.str2kw('printed_name', _("Bank statement")))
        kw.update(account=CommonAccounts.best_bank.get_object(), ref="BNK")
        kw.update(dc=DC.credit)
        yield finan.BankStatementsByJournal.create_journal(**kw)

        kw.update(journal_group=JournalGroups.misc)
        kw.update(account=CommonAccounts.cash.get_object(), ref="MSC")
        # kw.update(dc=DC.credit)
        kw.update(dd.str2kw('name', _("Miscellaneous transactions")))
        kw.update(dd.str2kw('printed_name', _("Transaction")))
        yield finan.JournalEntriesByJournal.create_journal(**kw)

        kw.update(preliminary=True, ref="PRE")
        kw.update(dd.str2kw('name', _("Preliminary transactions")))
        yield finan.JournalEntriesByJournal.create_journal(**kw)

        kw = dict(journal_group=JournalGroups.wages)
        kw.update(dd.str2kw('name', _("Paychecks")))
        kw.update(dd.str2kw('printed_name', _("Paycheck")))
        kw.update(account=CommonAccounts.cash.get_object(), ref="SAL")
        kw.update(dc=DC.debit)
        yield finan.JournalEntriesByJournal.create_journal(**kw)

    for m in (bevat, bevats, eevat):
        if not m:
            continue
        kw = dict(journal_group=JournalGroups.vat)
        kw.update(trade_type='taxes')
        kw.update(dd.str2kw('name', _("VAT declarations")))
        kw.update(dd.str2kw('printed_name', _("VAT declaration")))
        kw.update(must_declare=False)
        kw.update(account=CommonAccounts.due_taxes.get_object())
        kw.update(ref=m.DEMO_JOURNAL_NAME, dc=DC.debit)
        yield m.DeclarationsByJournal.create_journal(**kw)

    payments = []
    if finan:
        payments += [
            finan.BankStatement, finan.JournalEntry, finan.PaymentOrder
        ]

    pending_po = CommonAccounts.pending_po.get_object()
    wages = CommonAccounts.wages.get_object()
    tax_offices = CommonAccounts.tax_offices.get_object()

    MatchRule = rt.models.accounting.MatchRule
    for jnl in accounting.Journal.objects.all():
        if jnl.voucher_type.model in payments:
            yield MatchRule(journal=jnl,
                            account=CommonAccounts.customers.get_object())
            yield MatchRule(journal=jnl,
                            account=CommonAccounts.suppliers.get_object())
            if tax_offices:
                yield MatchRule(journal=jnl, account=tax_offices)
            if wages:
                yield MatchRule(journal=jnl, account=wages)
            if jnl.voucher_type.model is not finan.PaymentOrder:
                if pending_po:
                    yield MatchRule(journal=jnl, account=pending_po)
        elif jnl.trade_type:
            a = jnl.trade_type.get_main_account()
            if a:
                yield MatchRule(journal=jnl, account=a)
        # if jnl.voucher_type.model in payments:

    # pending_po = CommonAccounts.pending_po.get_object()
    # if pending_po:
    #     for jnl in accounting.Journal.objects.filter(voucher_type__in=VoucherTypes.finan.BankStatement):
    #         yield MatchRule(journal=jnl, account=pending_po)
