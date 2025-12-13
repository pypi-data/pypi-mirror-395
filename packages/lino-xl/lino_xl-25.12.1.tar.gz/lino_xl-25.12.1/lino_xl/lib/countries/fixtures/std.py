# -*- coding: UTF-8 -*-
# Copyright 2013-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd


def objects():
    if dd.plugins.countries.full_data:
        from lino_xl.lib.countries.fixtures.all_countries import objects
        yield objects()
        if dd.plugins.countries.country_code == 'EE':
            from lino_xl.lib.countries.fixtures.eesti import objects
            yield objects()
        elif dd.plugins.countries.country_code == 'BE':
            from lino_xl.lib.countries.fixtures.be import objects
            yield objects()
    else:
        from lino_xl.lib.countries.fixtures.few_countries import objects
        yield objects()
