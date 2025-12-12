# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils import Cycler
from lino.api import rt


def objects():
    PARTNERS = Cycler(rt.models.contacts.Partner.objects.all())
    PartnerAsset = rt.models.assets.PartnerAsset

    def asset(name):
        return PartnerAsset(name=name, partner=PARTNERS.pop())

    yield asset("ABC123")
    yield asset("ABC456")
    yield asset("DEF123")
    yield asset("DEF789")
