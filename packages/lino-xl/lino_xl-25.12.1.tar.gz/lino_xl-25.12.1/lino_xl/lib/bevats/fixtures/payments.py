# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
# from importlib import import_module

from django.conf import settings
from lino.utils import Cycler
from lino.api import dd, rt
from lino.utils.dates import AMONTH

# from lino.core.requests import BaseRequest
REQUEST = rt.login()  # BaseRequest()


def objects():

    Journal = rt.models.accounting.Journal
    Company = rt.models.contacts.Company
    Declaration = rt.models.bevats.Declaration

    # m = import_module(dd.plugins.declarations.country_module)
    # from lino_xl.lib.declarations.be import demo_objects

    # yield demo_objects()

    office = Company(name="Mehrwertsteuer-Kontrollamt Eupen",
                     street="Vervierser Str. 8",
                     country_id="BE",
                     zip_code="4700")
    yield office

    USERS = Cycler(settings.SITE.user_model.objects.all())
    JOURNAL = Journal.objects.get(ref=rt.models.bevats.DEMO_JOURNAL_NAME)
    # date = datetime.date(dd.plugins.periods.start_year, 1, 4)
    date = datetime.date(dd.plugins.periods.start_year, 1, 31)
    end_date = settings.SITE.demo_date(-30)
    while date < end_date:
        dcl = Declaration(journal=JOURNAL,
                          user=USERS.pop(),
                          partner=office,
                          entry_date=date)
        yield dcl
        dcl.register(REQUEST)
        dcl.save()

        date += AMONTH
