# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/peppol.html

from lino.api import dd, _
# from lino.mixins.periods import DateRange

if dd.plugins.peppol.with_suppliers:
    from .suppliers import *

if dd.plugins.peppol.supplier_id:
    from .documents import *
