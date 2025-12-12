# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds an arbitrary selection of a few demo countries.
"""

from lino.api import dd, rt, _

Country = dd.resolve_model('countries.Country')


def objects():

    def country(isocode, **kw):
        try:
            return Country.objects.get(isocode=isocode)
        except Country.DoesNotExist:
            return Country(isocode=isocode, **kw)

    yield country('EE', **dd.str2kw('name', _("Estonia")))
    yield country('BE', **dd.str2kw('name', _("Belgium")))
    yield country('DE', **dd.str2kw('name', _("Germany")))
    yield country('FR', **dd.str2kw('name', _("France")))
    yield country('NL', **dd.str2kw('name', _("Netherlands")))
    yield country('MA', **dd.str2kw('name', _("Maroc")))
    yield country('RU', **dd.str2kw('name', _("Russia")))
    yield country('CD', **dd.str2kw('name', _("Congo (Democratic Republic)")))
    yield country('BD', **dd.str2kw('name', _("Bangladesh")))
    yield country('US', **dd.str2kw('name', _("United States")))
