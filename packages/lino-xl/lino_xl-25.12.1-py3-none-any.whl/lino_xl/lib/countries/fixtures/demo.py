# -*- coding: UTF-8 -*-
# Copyright 2013-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd

def objects():
    from lino_xl.lib.countries.fixtures.few_countries import objects
    yield objects()

    from lino_xl.lib.countries.fixtures.few_cities import objects
    yield objects()
