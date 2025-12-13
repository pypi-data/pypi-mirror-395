# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime

from django.conf import settings

from lino.api import dd, rt, _
from lino_xl.lib.accounting.choicelists import DC, CommonAccounts
from lino.utils import Cycler

REQUEST = rt.login()  # BaseRequest()


def objects():

    if dd.plugins.vat.declaration_plugin is None:
        return

    JournalEntryItem = rt.models.finan.JournalEntryItem
    USERS = Cycler(settings.SITE.user_model.objects.all())
    PARTNERS = Cycler(rt.models.contacts.Partner.objects.order_by("-id"))
    jnl = rt.models.accounting.Journal.objects.get(preliminary=True)

    voucher = jnl.create_voucher(user=USERS.pop(),
                                 entry_date=datetime.date(
                                     dd.plugins.periods.start_year, 1, 1))
    yield voucher

    # seqno = 0

    def vi(ca, amount, **kwargs):
        # seqno += 1
        kwargs.update(account=ca.get_object(), voucher=voucher)
        amount = jnl.dc.normalized_amount(amount)  # 20240621
        # if jnl.dc == DC.debit:
        #     amount = -amount
        kwargs.update(amount=amount)
        return JournalEntryItem(**kwargs)

    # yield vi(CommonAccounts.net_income_loss, 100)
    yield vi(CommonAccounts.vat_due, 10)
    yield vi(CommonAccounts.suppliers, 50, partner=PARTNERS.pop())
    yield vi(CommonAccounts.customers, -100, partner=PARTNERS.pop())
    yield vi(CommonAccounts.best_bank, 40)

    voucher.register(REQUEST)
    voucher.full_clean()
    voucher.save()
