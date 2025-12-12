# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


import datetime
from dateutil.relativedelta import relativedelta as delta
from decimal import Decimal, ROUND_UP

from django.conf import settings
# from django.db.models import Q

# from lino import logger
from lino.utils import Cycler
from lino.api import dd, rt, _
from lino_xl.lib.vat.choicelists import VatAreas, VatRules
# from lino_xl.lib.accounting.utils import myround
from lino.mixins.ref import Referrable

# from lino.core.requests import BaseRequest
REQUEST = rt.login()  # BaseRequest()

# FIVE = Decimal("5.00")

has_payment_methods = dd.get_plugin_setting(
    'accounting', 'has_payment_methods', False)


def round5(d):
    return int(d / 5) * 5 + 5
    # d = Decimal(int(d/5)*5 + 5)
    # return myround(d)
    # return d.quantize(FIVE, rounding=ROUND_UP)


def objects():

    TradeTypes = rt.models.accounting.TradeTypes
    # VatRule = rt.models.vat.VatRule
    Journal = rt.models.accounting.Journal
    # Person = rt.models.contacts.Person
    Partner = rt.models.contacts.Partner
    Product = rt.models.products.Product
    VatProductInvoice = rt.models.trading.VatProductInvoice
    InvoiceItem = rt.models.trading.InvoiceItem
    Country = rt.models.countries.Country
    project_model = dd.plugins.accounting.project_model

    def get_trade_countries(tt):
        areas = set()
        for va in VatAreas.get_list_items():
            if VatRules.get_vat_rule(va, tt, default=False):
                areas.add(va)
        for obj in Country.objects.all():
            if VatAreas.get_for_country(obj) in areas:
                yield obj

    USERS = Cycler(settings.SITE.user_model.objects.all())

    sales_method = dd.plugins.accounting.sales_method
    if not sales_method:
        return
    PRODUCTS = Cycler(Product.objects.order_by('id'))
    can_cash = False
    if sales_method == "direct":
        ref = "SLS"
    elif sales_method == "delivery":
        ref = "SDN"
    elif sales_method == "pos":
        ref = "SSN"
        can_cash = True
    else:
        raise Exception("Unsupported sales method {}".format(sales_method))

    sales_journal = Journal.objects.get(ref=ref)

    for u in settings.SITE.user_model.objects.all():
        u.sales_journal = sales_journal
        u.full_clean()
        u.save()

    # tt = TradeTypes.sales
    # regimes = set()
    # for reg in VatRegimes.get_list_items():
    #     if VatRule.get_vat_rule(tt, reg, default=False):
    #         regimes.add(reg)
    # qs = Partner.objects.filter(vat_regime__in=regimes).order_by('id')
    # assert qs.count() > 0
    # CUSTOMERS = Cycler(qs)
    CUSTOMERS = Cycler(
        Partner.objects.filter(
            country__in=get_trade_countries(TradeTypes.sales)).order_by('id'))
    if len(CUSTOMERS) == 0:
        raise Exception("20171006 no customers ({})".format(
            len(list(get_trade_countries(TradeTypes.sales)))))

    # CUSTOMERS = Cycler(Person.objects.filter(
    #     gender=dd.Genders.male).order_by('id'))
    # assert Person.objects.count() > 0
    if has_payment_methods:
        PaymentMethod = rt.models.accounting.PaymentMethod
        PAYMENT_METHODS = Cycler(PaymentMethod.objects.order_by('id'))
        # PaymentMethod.objects.filter(
        #     Q(journal__isnull=True)|Q(journal=sales_journal)).order_by('id'))

    ITEMCOUNT = Cycler(1, 2, 3)
    if dd.get_plugin_setting('trading', 'subtotal_demo', False):
        SUBTOTALCOUNT = Cycler(1, 2, 3, 4)
        WITH_PRODUCT = Cycler(False, *([True] * 10))
    else:
        SUBTOTALCOUNT = Cycler([1])
        WITH_PRODUCT = Cycler([True])
    QUANTITIES = Cycler(15, 10, 8, 4)
    # SALES_PER_MONTH = Cycler(2, 1, 3, 2, 0)
    SALES_PER_MONTH = Cycler(5, 4, 1, 8, 6)

    par2projects = {}

    date = datetime.date(dd.plugins.periods.start_year, 1, 1)
    end_date = settings.SITE.demo_date(-10)  # + delta(years=-2)
    invoice_model = sales_journal.voucher_type.model  # VatProductInvoice or CashInvoice
    item_model = sales_journal.voucher_type.model.get_items_model()

    kw = dict(subtotal=True, **dd.str2kw('name', _("Subtotal")))
    if issubclass(Product, Referrable):
        kw.update(ref="=")
    yield (subtotal_prod := Product(**kw))

    while date < end_date:

        partner = None
        for i in range(SALES_PER_MONTH.pop()):
            # Every fifth time there are two successive invoices
            # to the same partner.
            if partner is None or i % 5:
                partner = CUSTOMERS.pop()
            invoice = invoice_model(
                journal=sales_journal,
                partner=partner,
                user=USERS.pop(),
                voucher_date=date + delta(days=5 + i),
                entry_date=date + delta(days=5 + i + 1),
                # payment_term=PAYMENT_TERMS.pop(),
            )
            if has_payment_methods:
                invoice.payment_method = PAYMENT_METHODS.pop()

            if project_model is not None and i % 7:
                if (cycler := par2projects.get(partner, None)) is None:
                    cycler = Cycler(project_model.objects.filter(partner=partner))
                    invoice.project = cycler.pop()
            yield invoice
            number_of_subs = SUBTOTALCOUNT.pop()
            seqno = 0
            for j in range(number_of_subs):
                for k in range(ITEMCOUNT.pop()):
                    seqno += 1
                    kw = dict(voucher=invoice, seqno=seqno)
                    if WITH_PRODUCT.pop():
                        kw.update(product=PRODUCTS.pop(), qty=QUANTITIES.pop())
                        item = item_model(**kw)
                        try:
                            item.product_changed(REQUEST)
                        except Exception as e:
                            # raise
                            msg = "20171006 {} in ({} {!r})".format(
                                e, invoice.partner, invoice.vat_regime)
                            raise Exception(msg)
                            # dd.logger.warning(msg)
                    else:
                        kw.update(title=_("Participation in general in costs"))
                        item = item_model(**kw)
                        item.set_amount(REQUEST, Decimal(20))
                    item.before_ui_save(REQUEST, None)
                    yield item
                if number_of_subs > 1:
                    seqno += 1
                    yield item_model(voucher=invoice, product=subtotal_prod, seqno=seqno)
            if can_cash and invoice.payment_method.is_cash:
                invoice.compute_totals()
                invoice.cash_received = round5(invoice.total_incl)
                # print("20220706", invoice.cash_received)
                invoice.cash_received_changed(REQUEST)
            invoice.register(REQUEST)
            invoice.save()

        date += delta(months=1)

    print("20250617", CUSTOMERS)
