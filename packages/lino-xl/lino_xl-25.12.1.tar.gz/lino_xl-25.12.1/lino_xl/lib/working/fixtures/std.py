# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, dd, _


def objects():
    SessionType = rt.models.working.SessionType
    yield SessionType(id=1, name=_("Default"))

    # Product = rt.models.products.Product
    # PriceRule = rt.models.products.PriceRule
    # kw = dict(sales_price="69.90", storage_management=True)
    # kw.update(dd.str2kw('name', _("Development")))
    # kw.update(delivery_unit="hour")
    # # kw.update(ref="dev", delivery_unit="hour")
    # obj = Product(**kw)
    # yield obj
    # yield PriceRule(product=obj)

    # if dd.is_installed("products"):
    #     for i in rt.models.working.ReportingTypes.get_list_items():
    #         yield i.create_object()
