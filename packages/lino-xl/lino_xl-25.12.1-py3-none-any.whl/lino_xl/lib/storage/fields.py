# -*- coding: UTF-8 -*-
# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from .choicelists import DC


class DcQuantityField(dd.VirtualField):
    """An editable virtual QuantityField to get and set both database fields
    :attr:`qty` and :attr:`dc` at once. It may be used only on
    models that also defines these two fields.

    When the quantity is positive and dc is DC.debit, return None.
    When the quantity is positive and dc is DC.credit, return quantity.
    When the quantity is negative and dc is DC.debit, return -quantity.
    When the quantity is negative and dc is DC.credit, return None.

    """

    editable = True
    empty_values = set([None])

    def __init__(self, dc, *args, **kwargs):
        self.dc = dc
        kwargs.update(blank=True)
        dd.VirtualField.__init__(self, dd.QuantityField(*args, **kwargs), None)

    def set_value_in_object(self, request, obj, value):
        if not value:
            obj.qty = None
        elif self.dc == DC.debit:
            obj.qty = -value
        else:
            obj.qty = value

    def value_from_object(self, obj, ar):
        if self.dc == DC.debit:
            return -obj.qty if obj.qty < 0 else None
        return obj.qty if obj.qty > 0 else None
