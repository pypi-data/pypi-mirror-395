# -*- coding: UTF-8 -*-
# Copyright 2014-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Imports all Estonian places from :mod:`commondata`.

New implementation after moving demonames from lino to commondata in March 2024.

"""

from lino import logger
from lino.api import dd

from commondata.places.estonia import COUNTIES

countries = dd.resolve_app('countries')


def cd2type(p):
    return countries.PlaceTypes.get_by_name(p.type)


def place2objects(country, place, parent=None):
    t = cd2type(place)
    if t is None:
        logger.info("20140612 ignoring place %s", place)
        return
    try:
        obj = countries.Place.objects.get(
            country=country, name=place.name, type=t, parent=parent)
        # obj.type = t
        # obj.parent = parent
        obj.zip_code = place.zip_code
    except countries.Place.DoesNotExist:
        obj = countries.Place(country=country,
                              type=t,
                              name=place.name,
                              parent=parent,
                              zip_code=place.zip_code)

    # We must save the parent before we can generate children.
    try:
        obj.full_clean()
    except Exception as e:
        raise Exception("Could not save %s : %r" % (dd.obj2str(obj), e))
    obj.save()
    yield obj

    for cp in place.children:
        yield place2objects(country, cp, obj)


def objects():
    EE = countries.Country.objects.get(isocode="EE")
    for p in COUNTIES:
        yield place2objects(EE, p)
