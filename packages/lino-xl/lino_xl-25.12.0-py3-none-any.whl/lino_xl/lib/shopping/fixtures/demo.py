from lino.api import rt, dd, _


def objects():
    Company = rt.models.contacts.Company
    obj = Company(name=_("Webshop customers without contact data"))
    yield obj

    sls = rt.models.accounting.Journal.get_by_ref("SLS")
    sls.partner = obj
    yield sls

    DeliveryMethod = rt.models.shopping.DeliveryMethod

    def delivery_method(designation, price, barcode_identity, **kwargs):
        if dd.is_installed("products"):
            kw = dict(**dd.str2kw('name', designation, sales_price=price))
            if dd.plugins.products.barcode_driver is not None:
                vendor = Company.objects.get(barcode_identity=546)
                kw.update(vendor=vendor, barcode_identity=barcode_identity)
            prod = rt.models.products.Product(**kw)
            yield prod
            kwargs.update(product=prod)
        yield DeliveryMethod(**dd.str2kw('designation', designation, **kwargs))

    yield delivery_method(_("Parcel center"), 2, 18)
    yield delivery_method(_("Home using UPS"), 5, 19)
    yield delivery_method(_("Take away"), 0, 20)
