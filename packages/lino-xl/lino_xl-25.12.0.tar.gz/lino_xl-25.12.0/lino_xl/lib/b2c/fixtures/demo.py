# -*- coding: UTF-8 -*-
# Copyright 2015-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Import a fictive B2C XML file.

"""

import os
from django.conf import settings
from lino.utils.cycler import Cycler
from lino.api import dd, rt

HERE = os.path.dirname(__file__)


def objects():

    # ses = rt.login('wilfried')
    dd.plugins.b2c.import_statements_path = HERE
    settings.SITE.site_config.import_b2c()
    dd.logger.info(
        "%d statements have been imported",
        rt.models.b2c.Statement.objects.count())

    # That file contains a few dozen accounts, which are now
    # "orphaned".  We are now going to assign these accounts to a
    # random partner TODO: find a more realistic rule for selecting
    # the candidates. The filter might be a plugin attribute.

    IA = rt.models.b2c.Account
    SA = rt.models.sepa.Account
    Partner = rt.models.contacts.Partner
    PARTNERS = Cycler(Partner.objects.order_by('id'))
    imported_accounts = IA.objects.all()
    if imported_accounts.count() > Partner.objects.order_by('id').count():
        raise Exception("20181030")

    count = 0
    for ia in imported_accounts:
        try:
            SA.objects.get(iban=ia.iban)
        except SA.DoesNotExist:
            yield SA(partner=PARTNERS.pop(), iban=ia.iban)
            count += 1
    if count == 0:
        raise Exception(
            "There's something wrong: no accounts have been imported")
