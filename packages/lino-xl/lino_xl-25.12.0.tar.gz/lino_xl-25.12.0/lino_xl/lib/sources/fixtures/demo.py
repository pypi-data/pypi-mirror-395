# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, _
from lino.utils.mldbc import babeld


def objects():
    Source = rt.models.sources.Source
    License = rt.models.sources.License
    Author = rt.models.sources.Author
    # Person = rt.models.contacts.Person

    reserved = License.objects.get(ref="reserved")
    yield (adams := Author(first_name="Douglas", last_name="Adams",
                           birth_date="11.03.1952", death_date="11.05.2001"))

    yield Source(title="The Hitchhiker's Guide to the Galaxy", license=reserved, author=adams)
