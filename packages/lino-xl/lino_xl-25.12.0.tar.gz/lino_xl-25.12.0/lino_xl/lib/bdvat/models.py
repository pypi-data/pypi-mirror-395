# -*- coding: UTF-8 -*-
# Copyright 2012-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings

from lino.api import dd, _
from lino_xl.lib.vat.mixins import VatDeclaration

from .choicelists import DeclarationFields

DEMO_JOURNAL_NAME = "VAT"

# print("20170711a {}".format(DeclarationFields.get_list_items()))


class Declaration(VatDeclaration):

    fields_list = DeclarationFields

    class Meta:
        app_label = 'bdvat'
        verbose_name = _("Bangladeshi VAT declaration")
        verbose_name_plural = _("Bangladeshi VAT declarations")

for fld in DeclarationFields.get_list_items():
    dd.inject_field('bdvat.Declaration', fld.name, fld.get_model_field())


from .ui import *
