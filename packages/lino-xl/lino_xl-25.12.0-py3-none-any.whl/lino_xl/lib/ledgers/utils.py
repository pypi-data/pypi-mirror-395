# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

def save_object(obj):
    obj.full_clean()
    obj.save_new_instance(obj.get_default_table().create_request())


def prepare_company(company, company_owner):
    """
    """
    from lino.api import rt, dd, _
    from lino_xl.lib.accounting.utils import DC
    from lino_xl.lib.invoicing.utils import invoicing_task, invoicing_rule

    accounting = dd.resolve_app('accounting')
    trading = dd.resolve_app('trading')
    ledgers = dd.resolve_app('ledgers')
    bdvat = dd.resolve_app('bdvat')

    company_ledger = ledgers.Ledger(company=company)
    yield company_ledger

    company_owner.ledger = company_ledger
    yield company_owner

    # JOURNALS
    JournalGroups = accounting.JournalGroups

    default_values = dict(journal_group=JournalGroups.sales, ledger=company_ledger, trade_type='sales', dc=DC.credit,
                          voucher_type=accounting.VoucherTypes.get_for_table(trading.InvoicesByJournal))

    VTT = trading.InvoicesByJournal

    def make_journal(ref, printed_name, name, **kwargs):
        kwargs.update(default_values)
        kwargs.update(dd.str2kw('name', name), ref=ref, printed_name=printed_name)
        vtt = kwargs.pop('table', VTT)
        return vtt.create_journal(**kwargs)

    REF_PREFIX = company.as_ref_prefix()

    yield make_journal(f"{REF_PREFIX}OFF", _("Offer"), _("Offers"))
    yield make_journal(f"{REF_PREFIX}CMP", _("Component sheet"), _("Component sheets"))
    yield (sls := make_journal(f"{REF_PREFIX}SLS", _("Invoice"), _("Sales invoices"),
                               make_storage_movements=True))

    misc_partner = rt.models.contacts.Company.objects.get(name="Miscellaneous")
    default_values.pop('voucher_type')

    yield (sdn := make_journal(f"{REF_PREFIX}SDN", _("Delivery note"), _("Delivery notes"),
                               partner=misc_partner, make_ledger_movements=False, make_storage_movements=True,
                               table=trading.CashInvoicesByJournal))
    yield make_journal(f"{REF_PREFIX}SSN", _("Sales note"), _("Sales notes"),
                       partner=misc_partner, make_ledger_movements=True, make_storage_movements=True,
                       table=trading.CashInvoicesByJournal)

    default_values.update(journal_group=JournalGroups.vat,
                          trade_type='taxes', dc=DC.debit)
    yield make_journal(f"{REF_PREFIX}VAT", _("VAT declaration"), _("VAT declarations"),
                       must_declare=False, table=bdvat.Declaration)

    yield invoicing_task(sls.ref, user_id=company_owner.id)
    yield invoicing_rule(sls.ref, trading.InvoiceItem, source_journal=sdn)

    CommonAccounts = accounting.CommonAccounts

    for common_account in CommonAccounts.get_list_items():
        yield common_account.create_object(ref=f"{REF_PREFIX}{common_account.value}", ledger=company_ledger)

    # TODO: do match rules
    # wages = CommonAccounts.wages.get_object(ledger=company_ledger)
    # tax_offices = CommonAccounts.tax_offices.get_object(ledger=company_ledger)
