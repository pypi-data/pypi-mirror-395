# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models

from lino.api import dd, rt, _

from .roles import StorageStaff


class ProvisionState(dd.Choice):
    is_editable = False


class ProvisionStates(dd.ChoiceList):
    item_class = ProvisionState
    verbose_name = _("Provision state")
    verbose_name_plural = _("Provision states")
    column_names = "value name text"
    required_roles = dd.login_required(StorageStaff)

    @classmethod
    def get_editable_states(cls):
        return [o for o in cls.objects() if o.is_editable]

    @dd.virtualfield(models.BooleanField(_("Editable")))
    def is_editable(cls, choice, ar):
        return choice.is_editable


# add = ProvisionStates.add_item
# in Lino Noi
# add('10', _("Purchased"), 'purchased')

# Simple
# add('10', _("Promised to customer"), 'promised')
# add('20', _("Ordered from supplier"), 'ordered')
# add('30', _("Received from supplier"), 'received')
# add('40', _("Shipped to customer"), 'shipped')
