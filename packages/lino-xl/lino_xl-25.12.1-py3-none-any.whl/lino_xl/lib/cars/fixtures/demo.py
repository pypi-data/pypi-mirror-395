# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils import Cycler
from lino.api import rt

brand_names = """
Alfa Romeo
Audi
BMW
Chevrolet
Chrysler
Citroen
Daewoo
Dacia
Daihatsu
Dodge
Fiat
Ford
Honda
Hyundai
Isuzu
Iveco
Jaguar
Jeep
Kia
Lada
Lancia
Linhai
Land Rover
Mazda
Mercedes-Benz
MG
Mini
Mitsubishi
Nissan
Opel
Peugeot
Plymouth
Pontiac
Porsche
Renault
Rover
Saab
Seat
Skoda
Smart
Ssangyong
Subaru
Suzuki
Toyota
Volvo
VW
"""


def objects():
    PARTNERS = Cycler(rt.models.contacts.Partner.objects.all())
    Car = rt.models.cars.Car
    Brand = rt.models.cars.Brand

    def brand(name):
        return Brand(name=name)

    for name in brand_names.strip().splitlines():
        yield brand(name)

    BRANDS = Cycler(Brand.objects.all())

    def car(license_plate):
        return Car(license_plate=license_plate, partner=PARTNERS.pop(), brand=BRANDS.pop())

    yield car("ABC123")
    yield car("ABC456")
    yield car("DEF123")
    yield car("DEF789")
    yield car("GHI123")
    yield car("GHI789")
