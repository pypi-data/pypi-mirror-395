# -*- coding: UTF-8 -*-
# Copyright 2016-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Sets `payment_term` of all partners.

"""

from lino.utils import Cycler
from lino.api import dd, rt, _

from lino_xl.lib.accounting.fixtures.std import PT


def objects():

    PaymentTerm = rt.models.accounting.PaymentTerm
    Worker = dd.plugins.accounting.payer_model
    if Worker is rt.models.contacts.Person:
        kwargs = {}
        kwargs['payer'] = Worker.objects.get(first_name="Robin",
                                             last_name="Dubois")
        kwargs['ref'] = "robin"
        kwargs = dd.str2kw('name', _("Cash Robin"), **kwargs)
        yield PaymentTerm(**kwargs)

    if Worker is rt.models.contacts.Company:
        yield PT(_("A"), "A", days=10, informal=True)
        payer = Worker(name=_("Invoices to emit"))
        yield payer
        yield PT(_("B"), "B", days=10, informal=True, payer=payer)

    if not dd.is_installed('trading'):
        return
    PAYMENT_TERMS = Cycler(PaymentTerm.objects.all())
    for p in rt.models.contacts.Partner.objects.all():
        # if p.id % 3 == 0:
        obj = p.get_sales_rule()
        obj.payment_term = PAYMENT_TERMS.pop()
        yield obj
