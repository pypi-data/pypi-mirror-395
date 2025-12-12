# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

try:
    import barcode
except ImportError:
    barcode = None
import io
from base64 import b64encode
from django.db import models
from django.conf import settings
from lino.api import dd, _
from lino.utils.quantities import ZERO_DURATION
from decimal import Decimal


class DeliveryUnit(dd.Choice):
    zero = Decimal("0.00")

    def __init__(self, value, text, name, zero=None):
        super().__init__(value, text, name)
        if zero is not None:
            self.zero = zero


class DeliveryUnits(dd.ChoiceList):
    item_class = DeliveryUnit
    verbose_name = _("Delivery unit")
    verbose_name_plural = _("Delivery units")


# values are taken from commondata.peppolcodes.DELIVERY_UNITS
# Note that the text is plural while the (internal) name is singular
add = DeliveryUnits.add_item
add('HUR', _("Hours"), 'hour', ZERO_DURATION)
add('MON', _("Months"), 'month', ZERO_DURATION)
add('XPP', _("Pieces"), 'piece', Decimal("0"))
add('XBX', _("Boxes"), 'box', Decimal("0"))
add('XPK', _("Packages"), 'package', Decimal("0"))
add('MTR', _("Metres"), 'm', Decimal("0.000"))
add('MTQ', _("Cubic metres"), 'm³', Decimal("0.000"))
add('MTK', _("Square metres"), 'm²', Decimal("0.000"))
add('LTR', _("Litres"), 'l', Decimal("0.000"))
add('MLT', _("Millilitres"), 'ml', Decimal("0"))
add('GRM', _("Grams"), 'g', Decimal("0"))
add('MGM', _("Milligrams"), 'mg', Decimal("0"))
add('KGM', _("Kilograms"), 'kg', Decimal("0.00"))


class ProductType(dd.Choice):
    table_name = 'products.Products'


class ProductTypes(dd.ChoiceList):
    item_class = ProductType
    verbose_name = _("Product type")
    verbose_name_plural = _("Product types")
    column_names = "value name text table_name *"

    @dd.virtualfield(models.CharField(_("Table name")))
    def table_name(cls, choice, ar):
        return choice.table_name


add = ProductTypes.add_item
add('100', _("Products"), 'default')


class PriceFactor(dd.Choice):
    field_cls = None

    def __init__(self, value, cls, name):
        self.field_cls = cls
        self.field_name = 'pf_' + name
        super().__init__(value, cls.verbose_name, name)


class PriceFactors(dd.ChoiceList):
    item_class = PriceFactor
    verbose_name = _("Price factor")
    verbose_name_plural = _("Price factors")

    @classmethod
    def get_field(cls, choice):
        return choice.field_cls.field(blank=True)


class BarcodeDriver(dd.Choice):
    barcode_length = None
    _current_demo_value = None
    GS1 = "000"

    def validate(self, bcode):
        raise NotImplementedError

    def get_barcode(self, product):
        raise NotImplementedError

    def pop_demo_value(self):
        if self._current_demo_value is None:
            self._current_demo_value = "1" * self.barcode_length
        else:
            self._current_demo_value = str(int(self._current_demo_value) + 1)
        return self._current_demo_value

    def write_svg_file(self, value):
        raise NotImplementedError

    def get_image_tag_as_string(self, product):
        raise NotImplementedError


class EAN8Driver(BarcodeDriver):
    barcode_length = 8
    # value = "dummy"
    names = "ean8"


class EAN13Driver(BarcodeDriver):
    barcode_length = 13
    # value = "dummy"
    names = "ean13"

    def validate(self, bcode):
        assert len(bcode) == self.barcode_length
        assert barcode.get_barcode_class(self.name)(bcode[:-1]).ean[-1] == bcode[-1]

    def get_barcode(self, product):
        manufacturer_code = (("0" * 4) + str(product.vendor.barcode_identity))[-4:]
        product_code = (("0" * 5) + str(product.barcode_identity))[-5:]
        bcode = f"{self.GS1}{manufacturer_code}{product_code}"
        return barcode.get_barcode_class(self.name)(bcode).ean

    def write_svg_file(self, value):
        EAN = barcode.get_barcode_class(self.name)
        ean = EAN(value)
        ean.save(dd.plugins.products.barcodes_dir / value)

    def get_image_tag_as_string(self, product, **options):
        ean = barcode.get_barcode_class(self.name)(self.get_barcode(product))
        ean.writer = barcode.writer.ImageWriter()
        # ean.writer.set_options(options)
        img = ean.render(options)
        f = io.BytesIO()
        img.save(f, format='PNG')
        f.seek(0)
        data = "data:image/png;base64," + b64encode(f.read()).decode('ascii')
        f.close()
        return f'<img src="{data}">'


class BarcodeDrivers(dd.ChoiceList):
    verbose_name = _("Barcode driver")
    verbose_name_plural = _("Barcode drivers")


add = BarcodeDrivers.add_item_instance
add(EAN8Driver())
add(EAN13Driver())


@dd.receiver(dd.pre_analyze)
def inject_barcode_field(sender, **kw):
    p = dd.plugins.products
    drv = p.barcode_driver
    if drv is None:
        return
    if isinstance(drv, str):
        drv = BarcodeDrivers.get_by_name(drv)
        p.barcode_driver = drv
