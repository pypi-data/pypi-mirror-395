# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import _
from .actions import *


class Ledger(dd.Model):
    class Meta:
        app_label = "ledgers"
        abstract = dd.is_abstract_model(__name__, "Ledger")
        verbose_name = _("Ledger")
        verbose_name_plural = _("Ledgers")

    name = dd.CharField(max_length=80, default="", null=False, blank=True)
    entry_date = dd.DateField(_("Last entry date"), null=True, blank=True)

    company = dd.OneToOneField("contacts.Company", null=True, blank=True)

    ledger_subscribe__ledger = SubscribeToLedger(params_layout="""
    role
    user
    """)

    @dd.virtualfield(dd.CharField(_("Ledger owner"), max_length=200))
    def ledger_owner(self, ar):
        desc = self.company.name
        if self.name:
            desc += f" ({self.name})"
        return desc

    def __str__(self):
        s = _("Ledger of %s") % self.company.name
        if self.name:
            s += f" ({self.name})"
        return s


from .ui import *
