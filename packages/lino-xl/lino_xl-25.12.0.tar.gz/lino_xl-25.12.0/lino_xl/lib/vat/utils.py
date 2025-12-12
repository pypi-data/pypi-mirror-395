# -*- coding: UTF-8 -*-
# Copyright 2008-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/vat.html


def add_vat(base, rate):

    # return base * (HUNDRED + rate) / HUNDRED
    return base * (100 + rate) / 100


def remove_vat(incl, rate):
    # return incl / ((HUNDRED + rate) / HUNDRED)
    return incl / ((100 + rate) / 100)
