# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino_xl.lib.accounting.choicelists import JournalGroups
from lino_xl.lib.vat.choicelists import VatRegimes
from lino_xl.lib.accounting.utils import DC, ZERO
from lino_xl.lib.finan.fixtures.payments import add_demo_account


def objects():
    if dd.plugins.peppol.supplier_id:
        qs = rt.models.contacts.Company.objects.exclude(
            vat_id="").filter(country__isocode="BE")
        qs.update(send_peppol=True)
        jnl = rt.models.accounting.Journal.get_by_ref("SLS")
        jnl.is_outbound = True
        yield jnl

        kw = dict()
        kw.update(journal_group=JournalGroups.purchases)
        kw.update(trade_type='purchases',
                  ref=dd.plugins.peppol.inbound_journal)
        kw.update(dd.str2kw('name', _("Inbound documents")))
        kw.update(dd.str2kw('printed_name', _("Invoice")))
        kw.update(dc=DC.debit)
        yield rt.models.peppol.ReceivedInvoicesByJournal.create_journal(**kw)

    # every fourth company in supported_countries and with a VAT id becomes
    # an Ibanity end user
    # supported_countries = {"BE"}
    # supported_countries = {"BE", "DE", "LU", "NL", "IE"}
    # # ar = rt.login("robin")
    # qs = rt.models.contacts.Company.objects.exclude(vat_id="")
    # qs = qs.filter(country__isocode__in=supported_countries)
    #
    # # Some of our demo partners already registered on another Access Point:
    # qs = qs.exclude(name__startswith="Niederau")
    # qs = qs.exclude(name__startswith="Ethias")
    # # Bestbank doesn't always exist
    # qs = qs.exclude(name__startswith="Bestbank")

    eupen = rt.models.countries.Place.objects.get(name="Eupen")
    kwargs = dict(
        city=eupen, street="Peppolstraße", zip_code="4700",
        email="info@example.com", phone="+3223344556",
        send_peppol=True, vat_regime=VatRegimes.get_by_name('subject', None))

    def s(name, vat_id, street_no):
        obj = rt.models.contacts.Company(
            name=name, vat_id=vat_id, street_no=street_no, **kwargs)
        obj.full_clean()
        obj.save()
        add_demo_account(obj)
        # if dd.plugins.peppol.with_suppliers:
        #     return rt.models.peppol.Supplier(company=obj)
        # else:
        #     return obj

    yield s("Number One", "BE 0123.456.749", 12)
    yield s("Number Two", "BE 0234.567.873", 23)
    yield s("Number Three", "BE 0345.678.997", 34)
