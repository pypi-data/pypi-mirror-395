# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from lino.modlib.system.choicelists import DurationUnits
from lino.api import dd, rt
from lino.utils import ONE_DAY
from lino_xl.lib.accounting.roles import LedgerStaff

Plan = rt.models.invoicing.Plan
# InvoicingAreas = rt.models.invoicing.InvoicingAreas


def objects():
    # vt = dd.plugins.invoicing.get_voucher_type()
    # jnl_list = vt.get_journals()
    # if len(jnl_list) == 0:
    #     return
    accountants = LedgerStaff.get_user_profiles()
    users = rt.models.users.User.objects.filter(
        language=dd.get_default_language(), user_type__in=accountants)
    if users.count() == 0:
        return
    ses = rt.login(users.first().username)

    min_date = None
    today = datetime.date(dd.plugins.periods.start_year, 1, 1)
    while today < dd.demo_date(-60):
        max_date = today - ONE_DAY
        # max_date = DurationUnits.months.add_duration(today, 1) - ONE_DAY
        # for area in InvoicingAreas.get_list_items():
        for area in rt.models.invoicing.Task.objects.all():
            # print("20221223 start plan for {} ({} --> {})".format(
            #     area, list(area.get_source_journals()), list(area.get_target_journals())))
            plan = Plan.create_user_plan(
                ses.get_user(),
                today=today,
                invoicing_task=area,
                # target_journal=area.get_target_journal(),
                min_date=min_date,
                max_date=max_date)
            plan.full_clean()
            yield plan
            plan.fill_plan(ses)
            # for i in plan.items.all()[:9]:
            # print("20210801 {} : create {} invoices".format(today, plan.items.count()))
            for i in plan.items.all():
                yield i.create_invoice(ses)

        min_date = max_date + ONE_DAY
        today = DurationUnits.months.add_duration(today, 1)
        # today = DurationUnits.weeks.add_duration(today, 1)
