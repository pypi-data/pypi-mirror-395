# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# from decimal import Decimal
from django.db import models
# from django.core.exceptions import ValidationError
from django.conf import settings

from lino.utils.sums import HUNDRED, ZERO
# from lino.utils.quantities import Quantity
from lino_xl.lib.contacts.mixins import PartnerPrintable
from lino_xl.lib.excerpts.mixins import Certifiable
from lino.api import dd, rt, _


if dd.is_installed('trading'):
    from lino_xl.lib.accounting.choicelists import TradeTypes
    from lino_xl.lib.vat.mixins import QtyVatItemBase, VatVoucher
    from lino_xl.lib.vat.utils import add_vat, remove_vat
    from lino_xl.lib.vat.mixins import get_default_vat_regime, myround
    from lino_xl.lib.vat.choicelists import VatAreas, VatRules


class TradingPartner(dd.Model):

    class Meta:
        abstract = True

    if dd.is_installed('trading'):

        show_invoice_partners = dd.ShowSlaveTable('trading.PartnersByInvoiceRecipient')
        show_trading_rules = dd.ShowSlaveTable('trading.RulesByPartner')

        def get_trading_rule(self, trade_type):
            TR = rt.models.trading.TradingRule
            obj = TR.objects.filter(partner=self, trade_type=trade_type).first()
            return obj or TR(partner=self, trade_type=trade_type)

        def get_sales_rule(self):
            return self.get_trading_rule(TradeTypes.sales)

        def get_invoice_recipient(self, trade_type):
            return self.get_trading_rule(trade_type).invoice_recipient or self


class TradingPrintable(PartnerPrintable, Certifiable):

    class Meta:
        abstract = True

    subject = models.CharField(_("Subject"), max_length=200, blank=True)
    paper_type = dd.ForeignKey('trading.PaperType', null=True, blank=True)

    # channel = Channels.field(default='paper')

    def get_paper_type(self):
        if self.paper_type:
            return self.paper_type
        tr = self.get_partner().get_trading_rule(self.get_trade_type())
        return tr.paper_type
        # sr = getattr(obj, 'salesrule', None)
        # if sr:
        #     return sr.paper_type

    def get_excerpt_templates(self, bm):
        # Overrides lino_xl.lib.excerpts.mixins.Certifiable.get_excerpt_templates

        pt = self.get_paper_type()
        if pt and pt.template:
            # print(20190506, pt.template)
            return [pt.template]

    def get_printable_context(self, ar):
        context = super().get_printable_context(ar)
        context.update(
            site_company=settings.SITE.get_plugin_setting('contacts', 'site_owner', None))
        # site_company=settings.SITE.get_config_value('site_company'))
        return context

    def get_columns_to_print(self):
        pt = self.get_paper_type()
        if pt and pt.columns_to_print:
            lst = pt.columns_to_print.split()
        elif dd.plugins.trading.columns_to_print:
            lst = dd.plugins.trading.columns_to_print.split()
        else:
            lst = dd.plugins.trading.items_column_names.split()
        if '*' in lst:
            lst.remove('*')
        return lst

    def get_column_heading(self, colname):
        if colname == "*":
            return ""
        if colname == "invoiceable":
            return dd.plugins.invoicing.invoiceable_label
        fld = getattr(rt.models.trading.InvoiceItem, colname)
        # if not hasattr(fld, "field"):
        #     raise Exception(f"20250630 {fld}")
        return fld.field.verbose_name


if dd.is_installed('trading'):

    class TradingVoucher(TradingPrintable, VatVoucher):

        class Meta:
            abstract = True

        edit_totals = False

        intro = models.TextField(_("Introductive text"), blank=True)
        default_discount = dd.PercentageField(_("Discount"), blank=True, null=True)

        def get_trade_type(self):
            return TradeTypes.sales

        def add_voucher_item(self, product=None, qty=None, **kw):
            if product is not None:
                Product = rt.models.products.Product
                if not isinstance(product, Product):
                    product = Product.objects.get(pk=product)
                # if qty is None:
                # qty = Duration(1)
            kw['product'] = product
            kw['qty'] = qty
            i = super().add_voucher_item(**kw)
            return i

    dd.update_field(TradingVoucher, 'total_base', editable=False)
    dd.update_field(TradingVoucher, 'total_vat', editable=False)
    dd.update_field(TradingVoucher, 'total_incl', editable=False)

    class TradingVoucherItem(QtyVatItemBase):

        class Meta:
            abstract = True

        product = dd.ForeignKey('products.Product', blank=True, null=True)
        description = dd.RichTextField(
            _("Description"), blank=True, null=True, bleached=True)
        # discount = dd.PercentageField(_("Discount"), blank=True, null=True)
        discount_rate = dd.PercentageField(_("Discount rate"), blank=True, null=True)
        discount_amount = dd.PriceField(_("Discount"), blank=True, null=True)

        @classmethod
        def override_column_headers(cls, ar, **headers):
            headers['discount_rate'] = _("D%")
            return super().override_column_headers(ar, **headers)

        def get_base_account(self, tt, ar=None):
            if self.product and self.product.subtotal:
                # raise Exception(f"{self.product}")
                return None
            # if self.product is None:
            #     return tt.get_base_account(ar)
            return tt.get_product_base_account(self.product, ar)
            # return self.voucher.journal.chart.get_account_by_ref(ref)

        def get_default_vat_class(self, tt):
            if self.product and self.product.vat_class:
                return self.product.vat_class
            return super().get_default_vat_class(tt)

        def discount_rate_changed(self, ar=None):
            self.reset_totals(ar)

        def discount_amount_changed(self, ar=None):
            self.reset_totals(ar)

        def product_changed(self, ar=None):
            if not self.product:
                return
            self.title = dd.babelattr(self.product, 'name')
            self.body = dd.babelattr(self.product, 'body')

            if self.product.subtotal:
                return
            # if self.qty is None:
            #     self.qty = Decimal("1")

            tt = self.voucher.get_trade_type()
            catalog_price = tt.get_catalog_price(self.product)

            if catalog_price is None:
                return
            # assert self.vat_class == self.product.vat_class
            rule = self.get_vat_rule(tt)
            if rule is None:
                return
            va = VatAreas.get_for_country()
            cat_rule = VatRules.get_vat_rule(
                va, tt, get_default_vat_regime(), self.vat_class, dd.today())
            if cat_rule is None:
                return
            if rule.rate != cat_rule.rate:
                catalog_price = remove_vat(catalog_price, cat_rule.rate)
                catalog_price = add_vat(catalog_price, cat_rule.rate)
            self.unit_price = round(catalog_price, dd.plugins.vat.unit_price_decpos)
            self.unit_price_changed(ar)

        def set_amount(self, ar, amount):
            if self.discount_rate is None:
                discount_rate = self.voucher.default_discount
            else:
                discount_rate = self.discount_rate
            if discount_rate is not None:
                amount -= amount * discount_rate / HUNDRED
            if self.discount_amount is not None:
                amount -= self.discount_amount
                amount = myround(amount)  # important for tim2lino
            super().set_amount(ar, amount)

        def full_clean(self):
            # We call super() only at the end because we need to check for "Data too
            # long for column 'qty'", but we must call set_seqno() explicitly before
            # doing the loop.
            if not self.seqno:
                self.set_seqno()
            if self.product and self.product.subtotal:
                flt = dict(voucher=self.voucher, seqno__lt=self.seqno)
                # if self.seqno is not None:
                #     flt.update(seqno__lt=self.seqno)
                sums = [ZERO, ZERO, ZERO, ZERO]
                for i in self.__class__.objects.filter(**flt).order_by('seqno'):
                    if i.product and i.product.subtotal:
                        sums = [ZERO, ZERO, ZERO, ZERO]
                    else:
                        sums[0] += i.total_base or 0
                        sums[1] += i.total_vat or 0
                        sums[2] += i.total_incl or 0
                        sums[3] += i.qty or 1
                self.total_base = sums[0]
                self.total_vat = sums[1]
                self.total_incl = sums[2]
                # self.qty = Quantity(sums[3])  # avoid "Data too long for column 'qty'"
                self.qty = sums[3]
                self.unit_price = None
            # elif self.total_incl:
            #     raise ValidationError(
            #         _("You must specify a product if there is an amount."))
            super().full_clean()
