# -*- coding: UTF-8 -*-
# Copyright 2010-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Some utilities for parsing contact data. See also
:mod:`lino.mixins.human`.

"""

import re

# PARTNER_NUMBERS_START_AT = 100  # used for generating demo data and tests
PARTNER_NUMBERS_START_AT = 1  # used for generating demo data and tests


def street2kw(s, **kw):
    "Parse a string to extract the fields street, street_no and street_box."
    # ~ m = re.match(r"(\D+),?\s*(\d+)\s*(\w*)", s)
    m = re.match(r"(.+),?\s+(\d+)\s*(\D*)$", s)
    if m:
        kw['street'] = m.group(1).strip()
        kw['street_no'] = m.group(2).strip()
        street_box = m.group(3).strip()
        if len(street_box) > 5:
            kw['addr2'] = street_box
        else:
            kw['street_box'] = street_box
    else:
        s = s.strip()
        if len(s):
            kw['street'] = s
    return kw
