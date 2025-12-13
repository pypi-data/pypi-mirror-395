# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from lino.mixins.ref import Referrable
from lino.api import dd, _


class CarStates(dd.ChoiceList):
    verbose_name = _("Car state")
    verbose_name_plural = _("Car states")


add = CarStates.add_item
add("1", _("For sale"), "forsale")
add("2", _("Sold"), "sold")
add("3", _("Other"), "other")


class FuelTypes(dd.ChoiceList):
    verbose_name = _("Fuel type")
    verbose_name_plural = _("Fuel types")


add = FuelTypes.add_item
add("1", _("Petrol"), "petrol")
add("2", _("Diesel"), "diesel")
add("3", _("Gas"), "gas")
add("4", _("Electricity"), "electricity")


class Brand(Referrable):
    class Meta:
        app_label = 'cars'
        verbose_name = _("Car brand")
        verbose_name_plural = _("Car brands")
        abstract = dd.is_abstract_model(__name__, 'Car')
        ordering = ["name"]

    name = dd.CharField(_("Designation"), blank=True, max_length=200)

    def __str__(self):
        return self.name


class Car(dd.Model):

    class Meta:
        app_label = 'cars'
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")
        abstract = dd.is_abstract_model(__name__, 'Car')
        ordering = ["partner", "license_plate"]

    partner = dd.ForeignKey(dd.plugins.cars.partner_model, blank=True, null=True)
    brand = dd.ForeignKey('cars.Brand', blank=True, null=True)
    model = dd.CharField(_("Model"), blank=True, max_length=100)
    # name = dd.CharField(_("Designation"), blank=True, max_length=200)
    vin = dd.CharField(_("Vehicle ID"), blank=True,
                       null=True, max_length=200, unique=True)
    state = CarStates.field(blank=True)
    color = dd.CharField(_("Color"), blank=True, max_length=100)
    license_plate = dd.CharField(_("License plate"), blank=True, max_length=100)
    reg_date = dd.DateField(_("Registration date"), blank=True, null=True)
    mileage = models.IntegerField(_("Mileage"), blank=True, null=True)
    ps = models.IntegerField(_("PS"), blank=True, null=True)
    kw = models.IntegerField(_("KW"), blank=True, null=True)
    engine = dd.CharField(_("Engine capacity"), blank=True, max_length=100)
    fuel_type = FuelTypes.field(blank=True)
    remarks = dd.RichTextField(_("Remarks"), blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"


class Brands(dd.Table):
    model = 'cars.Brand'
    required_roles = dd.login_required(dd.SiteStaff)
    column_names = "name ref *"
    detail_layout = """
    ref name id
    CarsByBrand
    """


class CarDetail(dd.DetailLayout):
    main = """
    id partner state
    brand model
    left remarks
    """

    left = """
    reg_date ps kw
    vin
    color
    engine fuel_type
    """


class Cars(dd.Table):
    model = 'cars.Car'
    required_roles = dd.login_required(dd.SiteStaff)
    column_names = 'partner license_plate brand model vin *'
    # order_by = ["ref", "partner", "designation"]

    insert_layout = """
    license_plate
    brand model
    partner
    """

    detail_layout = 'cars.CarDetail'


class CarsByPartner(Cars):
    master_key = 'partner'
    column_names = 'license_plate brand model vin *'
    insert_layout = """
    license_plate
    brand model
    partner
    """


class CarsByBrand(Cars):
    master_key = 'brand'
    column_names = 'model partner license_plate vin *'
    insert_layout = """
    model
    partner
    license_plate
    """
