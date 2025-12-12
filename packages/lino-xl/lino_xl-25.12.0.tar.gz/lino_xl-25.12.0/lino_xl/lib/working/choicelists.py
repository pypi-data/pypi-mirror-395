# -*- coding: UTF-8 -*-
# Copyright 2014-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _


class ReportingTypes(dd.ChoiceList):
    verbose_name = _("Reporting type")
    verbose_name_plural = _("Reporting types")
    column_names = 'value name text *'

add = ReportingTypes.add_item

add('10', _("Regular"), 'regular')
add('20', _("Free"), 'free')
