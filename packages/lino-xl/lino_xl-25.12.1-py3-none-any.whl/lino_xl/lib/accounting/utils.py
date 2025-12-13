# -*- coding: UTF-8 -*-
# Copyright 2012-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Documentation: https://dev.lino-framework.org/plugins/accounting.html

from .choicelists import DC
from lino.utils.sums import ZERO, CENT, HUNDRED, ONE, MAX_AMOUNT, myround


class Balance(object):

    def __init__(self, d, c):
        if d is None:
            d = ZERO
        if c is None:
            c = ZERO
        if d > c:
            self.d = d - c
            self.c = ZERO
        else:
            self.c = c - d
            self.d = ZERO

    def __str__(self):
        if self.d:
            return "{} DB".format(self.d)
        return "{} CR".format(self.c)

    def __repr__(self):
        return "Balance({},{})".format(self.d, self.c)
        return "{} CR".format(self.c)

    def __sub__(self, o):
        d1 = self.d or ZERO
        c1 = self.c or ZERO
        d2 = o.d or ZERO
        c2 = o.c or ZERO
        return Balance(d1 - d2, c1 - c2)

    def __add__(self, o):
        d1 = self.d or ZERO
        c1 = self.c or ZERO
        d2 = o.d or ZERO
        c2 = o.c or ZERO
        return Balance(d1 + d2, c1 + c2)

    def value(self, dc):
        if dc is DC.debit:
            return self.d - self.c
        else:
            return self.c - self.d
