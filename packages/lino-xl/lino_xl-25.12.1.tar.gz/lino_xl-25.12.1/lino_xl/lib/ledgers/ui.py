# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.core.roles import SiteAdmin
from lino_xl.lib.accounting.roles import LedgerStaff


class Ledgers(dd.Table):
    label = _("Ledgers")
    model = "ledgers.Ledger"
    required_roles = dd.login_required(SiteAdmin)

    column_names = "id ledger_owner company entry_date *"
    detail_layout = """
    id ledger_owner company
    entry_date name
    accounting.JournalsByLedger
    """


class MyLedger(Ledgers):
    label = _("My ledger")
    required_roles = dd.login_required(LedgerStaff)
    default_record_id = "row"

    @classmethod
    def get_row_permission(cls, obj, ar, state, ba):
        if ar.get_user().ledger == obj:
            return True
        return False

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        return ar.get_user().ledger


class ByLedger(dd.Table):
    master_key = "ledger"
    no_phantom_row = True
