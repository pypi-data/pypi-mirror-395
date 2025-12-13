# -*- coding: UTF-8 -*-
# Copyright 2016-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _


def objects():

    PaperType = rt.models.trading.PaperType
    bm = rt.models.printing.BuildMethods.get_system_default()
    yield PaperType(ref="letter", template="default" + bm.template_ext,
                    designation=_("Letter paper"))
    yield PaperType(ref="blank", template="default" + bm.template_ext,
                    designation=_("Blank paper"))
