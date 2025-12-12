# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, _


def objects():
    PaperType = rt.models.trading.PaperType

    def pt(name, ref, template):
        return PaperType(designation=name, ref=ref, template=template)

    yield pt(_("Sale"), "car_sale", "cars.weasy.html")
    yield pt(_("Repair"), "car_repair", "cars.weasy.html")
