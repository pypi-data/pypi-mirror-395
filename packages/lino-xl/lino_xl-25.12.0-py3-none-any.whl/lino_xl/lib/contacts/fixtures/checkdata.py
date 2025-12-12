# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from commondata.utils import get_name_factory
from commondata.demonames.streets import STREETS_IN_TALLINN
from django.conf import settings
from lino.utils import join_words
from lino.api import dd, rt
from lino.utils import Cycler
from lino.api import rt

class NameCycler:

    def __init__(self, nf):
        self.LAST_NAMES = Cycler(nf.get_last_names())
        self.MALES = Cycler(nf.get_male_first_names())
        self.FEMALES = Cycler(nf.get_female_first_names())


class AddressChangerEstonia:

    def __init__(self):
        super().__init__()
        Country = rt.models.countries.Country
        Place = rt.models.countries.Place
        PlaceTypes = rt.models.countries.PlaceTypes
        # self.tallinn = Place.objects.get(type=PlaceTypes.town, name="Tallinn")
        self.eesti = Country.objects.get(isocode="EE")
        self.streets = Cycler(self.get_streets())

    def get_streets(self):
        Place = rt.models.countries.Place
        PlaceTypes = rt.models.countries.PlaceTypes
        for streetname, township in STREETS_IN_TALLINN:
            t = PlaceTypes.township
            qs = Place.objects.filter(country=self.eesti, type=t, name__iexact=township)
            if qs.count() > 1:
                dd.logger.warning("{} : more than 1 township".format(qs))
            if (p := qs.first()) is not None:
            #     yield self.tallinn, None, streetname
            # else:
                yield p, None, streetname
            # else:
            #     raise Exception("Unknown %s %r" % (t, linnaosa))

    def change_address(self, obj):
        obj.country = self.eesti
        city, region, street = self.streets.pop()
        obj.city = city
        obj.zip_code = city.zip_code
        obj.street = street


def objects():
    demo_region = dd.plugins.contacts.demo_region
    if not demo_region:
        return []

    # print("Localize demo names to", demo_region)

    names = NameCycler(get_name_factory(demo_region))

    if demo_region == "EE":
        dist = AddressChangerEstonia()
    else:
        dist = None

    User = settings.SITE.user_model
    Person = rt.models.contacts.Person

    for p in Person.objects.order_by('id'):
        # Site users keep their original name:
        if User.objects.filter(partner=p).count() == 0:
            p.last_name = names.LAST_NAMES.pop()
            if p.gender == dd.Genders.male:
                p.first_name = names.MALES.pop()
                names.FEMALES.pop()
            else:
                p.first_name = names.FEMALES.pop()
                names.MALES.pop()
            p.name = join_words(p.last_name, p.first_name)
            if dist is not None:
                if p.country and p.country.isocode == 'BE':
                    dist.change_address(p)
            yield p
            # p.save()
            # dblogger.info(p.get_address(', '))
