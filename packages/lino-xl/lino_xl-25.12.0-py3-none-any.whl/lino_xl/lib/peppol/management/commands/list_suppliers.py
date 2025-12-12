# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from lino.api.shell import *
from lino.api import dd, rt
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "List the suppliers in this Ibanity environment."

    def add_arguments(self, parser):
        parser.add_argument(
            "-u", "--unknown",
            action="store_true", default=False,
            dest="unknown",
            help="Include unknown suppliers.",
        )
        parser.add_argument(
            "-d", "--deleted",
            action="store_true", default=False,
            dest="deleted",
            help="Include deleted (offboarded) suppliers.",
        )

    def handle(self, *args, **options):
        if not dd.plugins.peppol.credentials:
            print("This Lino site has no Peppol credentials")
            return
        ar = rt.login()
        ses = dd.plugins.peppol.get_ibanity_session(ar)
        kwargs = dict()
        if options.get('deleted', False):
            kwargs.update(hide_offboarded=False)
        if options.get('unknown', False):
            kwargs.update(hide_unknown=False)
        for num, data in enumerate(ses.list_suppliers(**kwargs)):
            names = ' | '.join([j['value'] for j in data['attributes']['names']])
            vat_id = data['attributes']['enterpriseIdentification']['vatNumber']
            status = data['attributes']['onboardingStatus']
            receiver = data['attributes']['peppolReceiver']
            supplier_id = data['id']
            txt = f"{num+1}) {supplier_id} {vat_id} {status} {receiver} ({names})"
            if supplier_id == dd.plugins.peppol.supplier_id:
                txt += " <<< (THIS SITE)"
            print(txt)
