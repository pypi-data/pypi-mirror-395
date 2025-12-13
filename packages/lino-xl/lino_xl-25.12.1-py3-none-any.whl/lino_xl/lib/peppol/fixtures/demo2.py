# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _

# SUPPORTED_COUNTRIES = {'BE', 'LU', 'NL'}
SUPPORTED_COUNTRIES = {'BE'}


def objects():

    if dd.plugins.peppol.with_suppliers:
        qs = rt.models.contacts.Company.objects.filter(
            country__isocode__in=SUPPORTED_COUNTRIES)
        for company in qs:
            if company.endpoint_id.is_valid and not company.send_peppol:
                company.send_peppol = True
                yield company
        qs = rt.models.contacts.Company.objects.filter(send_peppol=True)
        for company in qs:
            yield rt.models.peppol.Supplier(company=company)
