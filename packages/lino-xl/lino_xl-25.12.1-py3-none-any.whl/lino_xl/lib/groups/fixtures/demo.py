# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, _
from lino.utils.mldbc import babel_named as named
from lino.modlib.users.fixtures import abc


def objects():
    Group = rt.models.groups.Group

    yield named(Group, _("Hitchhiker's Guide to the Galaxy"))
    yield named(Group, _("Star Trek"))
    yield named(Group, _("Harry Potter"))

    yield abc.objects()
