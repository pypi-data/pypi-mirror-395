# -*- coding: UTF-8 -*-
# Copyright 2019-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core.roles import UserRole


class InvoicingUser(UserRole):
    "Can use invoicing."
    pass


class InvoicingStaff(InvoicingUser):
    "Can use and configure invoicing."
    pass
