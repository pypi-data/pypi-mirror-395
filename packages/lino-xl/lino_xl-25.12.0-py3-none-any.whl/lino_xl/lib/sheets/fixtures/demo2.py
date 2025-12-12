# -*- coding: UTF-8 -*-
# Copyright 2018-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Create a series of reports.

All reports have the same user, which would not be possible when using the web
front end because reports are user plans and you can have only one plan per
user. But programatically it is possible and doesn't disturb.

"""

from django.conf import settings
from lino.api import rt, dd


def objects():
    # dd.logger.info(
    #     "sheets %s %s",
    #     dd.plugins.periods.start_year, dd.today().year+1)
    from datetime import date
    Report = rt.models.sheets.Report
    StoredPeriod = rt.models.periods.StoredPeriod
    try:
        ses = rt.login("robin")
    except rt.models.users.User.DoesNotExist:
        print("20220621 no robin in {} (languages = {})".format(
            rt.models.users.User.objects.all(), settings.SITE.languages))
        raise
    for year in range(dd.plugins.periods.start_year, dd.today().year + 1):
        sp = StoredPeriod.get_or_create_from_date(date(year, 1, 1))
        ep = StoredPeriod.get_or_create_from_date(date(year, 12, 31))
        obj = Report(start_period=sp, end_period=ep, user=ses.get_user())
        yield obj
        obj.run_update_plan(ses)
        # dd.logger.info("20180907 %s", year)
