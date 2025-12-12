# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, _
from lino.utils.mldbc import babeld


def objects():
    License = rt.models.sources.License

    yield babeld(License, _("Public domain"),
                 ref="pd", url="https://en.wikipedia.org/wiki/Public_domain")
    yield babeld(License, _("All rights reserved"),
                 ref="reserved", url="https://en.wikipedia.org/wiki/All_rights_reserved")
    yield babeld(License, _("Creative Commons BY"),
                 ref="cc by", url="https://creativecommons.org/licenses/by/4.0/")
    yield babeld(License, _("Creative Commons BY SA"),
                 ref="cc by-sa", url="https://creativecommons.org/licenses/by-sa/4.0/")
    yield babeld(License, _("Creative Commons BY-ND"),
                 ref="cc by-nd", url="https://creativecommons.org/licenses/by-nd/4.0/")
