# -*- coding: UTF-8 -*-
# Copyright 2012-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
# from django.template.loader import select_template

from django.db import models
from django.db.models import Q, F, Sum, Subquery, OuterRef, Exists, Case, Value, When
from django.db.models.functions import Cast

from lino.utils.sums import ONE, ZERO, myround, SumCollector
# from lino.utils.dates import AMONTH, ADAY
from lino.api import dd, rt, _
# from lino.mixins.registrable import Registrable
from lino.modlib.uploads.mixins import make_captured_image

from lino_xl.lib.accounting.choicelists import CommonAccounts
from lino_xl.lib.accounting.choicelists import TradeTypes, VoucherStates
from lino_xl.lib.accounting.mixins import ProjectRelated, VoucherItem
from lino_xl.lib.accounting.mixins import Payable, PaymentRelated
from lino_xl.lib.accounting.models import Voucher
from lino_xl.lib.peppol.mixins import PeppolSendable

from .choicelists import VatClasses, VatRegimes, VatAreas, VatRules

# ZERO = Decimal("0.00")


def get_default_vat_regime():
    return dd.plugins.vat.default_vat_regime


# def get_default_vat_class():
#     return dd.plugins.vat.default_vat_class


class VatTotal(dd.Model):
    # abstract base class for both voucher and item
    class Meta:
        abstract = True

    total_incl = dd.PriceField(_("Total incl. VAT"), blank=True, null=True)
    total_base = dd.PriceField(_("Total excl. VAT"), blank=True, null=True)
    total_vat = dd.PriceField(_("VAT"), blank=True, null=True)

    @classmethod
    def override_column_headers(cls, ar, **headers):
        headers['total_incl'] = _("TotIncl")
        headers['total_base'] = _("TotExcl")
        return super().override_column_headers(ar, **headers)

    def reset_totals(self, ar):
        pass

    def get_vat_rule(self, tt):
        return None

    def total_base_changed(self, ar):
        # dd.logger.info("20150128 total_base_changed %r", self.total_base)
        if self.total_base is None:
            self.reset_totals(ar)
            if self.total_base is None:
                return

        rule = self.get_vat_rule(self.get_trade_type())
        # dd.logger.info("20180813 %r", rule)
        if rule is None:
            self.total_incl = None
            self.total_vat = None
        else:
            if rule.vat_returnable_account is not None:
                self.total_incl = self.total_base
                self.total_vat = None
            else:
                self.total_vat = myround(self.total_base * rule.rate)
                self.total_incl = self.total_base + self.total_vat

    def total_vat_changed(self, ar):
        if self.total_vat is None:
            self.reset_totals(ar)
            if self.total_vat is None:
                return

        if self.total_base is None:
            self.total_base = ZERO
        rule = self.get_vat_rule(self.get_trade_type())
        if rule is not None and rule.vat_returnable_account is not None:
            self.total_incl = self.total_base
            self.total_vat = None
        else:
            self.total_incl = self.total_vat + self.total_base

    def total_incl_changed(self, ar):
        if self.total_incl is None:
            self.reset_totals(ar)
            if self.total_incl is None:
                return
        # assert not isinstance(self.total_incl,basestring)
        rule = self.get_vat_rule(self.get_trade_type())
        if rule is None:
            self.total_base = None
            self.total_vat = None
        elif rule.vat_returnable_account is not None:
            self.total_base = self.total_incl
            self.total_vat = None
        else:
            decpos = dd.plugins.vat.unit_price_decpos
            self.total_base = round(self.total_incl / (ONE + rule.rate), decpos)
            self.total_vat = round(self.total_incl - self.total_base, decpos)


class ComputeSums(dd.Action):
    help_text = _("Compute sums")
    button_text = "Σ"
    custom_handler = True
    readonly = False

    def get_action_permission(self, ar, obj, st):
        # if ar.data_iterator is None:
        #     return False
        if not super(ComputeSums, self).get_action_permission(ar, obj, st):
            return False
        return True

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        obj.compute_totals()
        obj.full_clean()
        obj.save()
        ar.success(refresh=True)


class VatDocument(Voucher, ProjectRelated, VatTotal):

    # refresh_after_item_edit = False

    class Meta:
        abstract = True

    state = VoucherStates.field(default='draft')
    vat_regime = VatRegimes.field()
    items_edited = models.BooleanField(default=False)

    edit_totals = True
    _vat_subtotals = None

    compute_sums = ComputeSums()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super().get_registrable_fields(site):
            yield f
        yield 'vat_regime'

    def is_reversal(self):
        rv = super().is_reversal()
        return rv if self.total_base >= 0 else not rv

    def compute_totals(self):
        if self.pk is None or not self.state.is_editable:
            return
        # print("20190911 compute_totals")
        base = Decimal()
        vat = Decimal()
        # tt = self.get_trade_type()
        self._vat_subtotals = None
        for cat, rule, total_base, total_vat in self.vat_subtotals:
            base += total_base
            vat += total_vat
        # for i in self.items.all():
        #     if i.total_base is not None:
        #         base += i.total_base
        #     if i.total_vat is not None:
        #         vat += i.total_vat
        self.total_base = myround(base)
        self.total_vat = myround(vat)
        self.total_incl = myround(base + vat)

    def get_payable_sums_dict(self, ar=None):
        # implements sepa.mixins.Payable
        sums = SumCollector()
        tt = self.get_trade_type()
        # vat_account = tt.get_vat_account()
        # if vat_account is None:
        #     raise Exception("No VAT account for %s." % tt)
        for i in self.items.order_by('seqno'):
            base_account = i.get_base_account(tt, ar)
            if base_account is None:
                # e.g. a subtotal
                continue
                # msg = "No base account for {0} (tt {1}, total_base {2})"
                # msg = msg.format(i, tt, i.total_base)
                # raise Warning(msg)
            rule = i.get_vat_rule(tt)
            ana_account = i.get_ana_account()
            if i.total_base:
                sums.collect(((base_account, ana_account), self.project,
                              i.vat_class, self.vat_regime), i.total_base)

            if rule is not None:
                if rule.vat_returnable_account is None:
                    vat_amount = i.total_vat
                elif i.total_base is None:
                    continue
                else:
                    vat_amount = i.total_base * rule.rate
                if not vat_amount:
                    continue

                if rule.vat_returnable_account is not None:
                    acc_tuple = (rule.vat_returnable_account.get_object(),
                                 None)
                    sums.collect((acc_tuple, self.project, i.vat_class,
                                  self.vat_regime), -vat_amount)
                if rule.vat_account is None:
                    acc_tuple = (base_account, ana_account)
                else:
                    acc_tuple = (rule.vat_account.get_object(), None)
                sums.collect(
                    (acc_tuple, self.project, i.vat_class, self.vat_regime),
                    vat_amount)
        sums.myround()
        return sums

    def fill_defaults(self):
        super().fill_defaults()
        if not self.vat_regime:
            if self.partner_id:
                self.vat_regime = self.partner.vat_regime
            if not self.vat_regime:
                self.vat_regime = get_default_vat_regime()

    def update_item(self):
        if self.pk is None or not self.state.is_editable:
            return
        if self.items_edited or not self.edit_totals:
            return
        tt = self.journal.trade_type
        account = tt.get_partner_invoice_account(self.partner)
        if account is None:
            account = CommonAccounts.waiting.get_object()
            if account is None:
                raise Warning(
                    _("{} is not configured").format(CommonAccounts.waiting))
        kw = dict()
        if dd.is_installed('ana') and account.needs_ana:
            kw['ana_account'] = account.ana_account
        kw['account'] = account
        kw['total_incl'] = self.total_incl
        qs = self.items.all()
        if qs.count():
            item = qs[0]
            for k, v in kw.items():
                setattr(item, k, v)
        else:
            item = self.add_voucher_item(seqno=1, **kw)
        item.total_incl_changed(None)
        item.full_clean()
        item.save()

    @dd.chooser()
    def vat_regime_choices(self, partner):
        return VatRegimes.get_choices_for_country(partner.country)

    def partner_changed(self, ar=None):
        self.vat_regime = None
        self.fill_defaults()
        # self.update_item()  # called by after_ui_save()

    def after_ui_save(self, ar, cw):
        self.update_item()
        return super().after_ui_save(ar, cw)

    def full_clean(self, *args, **kw):
        super().full_clean(*args, **kw)
        if not self.edit_totals:
            self.compute_totals()
        # 20250123 disable because it disturbs in tim2lino
        # if self.vat_regime is not None:
        #     if self.vat_regime.needs_vat_id and not self.partner.vat_id:
        #         raise ValidationError(
        #             _("Cannot use VAT regime {} for partner without VAT id").
        #             format(self.vat_regime))

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            self.compute_totals()

            self.items_edited = True
            # Above line is because an automatically filled invoice
            # item should not change anymore once the invoice has been
            # registered.  For example if the partner's
            # purchase_account changed and you unregister an old
            # invoice, Lino must not automatically replace the account
            # of that invoice.

        # elif new.name == 'draft':
        #     if not self.edit_totals:
        #         self.total_base = None
        #         self.total_vat = None
        #         self.total_incl = None
        #     else:
        #         self.compute_totals()
        super().before_state_change(ar, old, new)

    def after_create_invoice(self):
        self.compute_totals()

    @property
    def vat_subtotals(self):
        # used in lino_xl/lib/vat/config/vat/peppol-ubl.xml
        if self._vat_subtotals is None:
            sums = dict()
            tt = self.get_trade_type()
            for i in self.items.order_by('seqno'):
                rule = i.get_vat_rule(tt)
                if rule is not None:
                    cat = i.get_peppol_vat_category()
                    k = (cat, rule)
                    amounts = sums.setdefault(k, [ZERO, ZERO])
                    if i.total_base:
                        amounts[0] += i.total_base
                    if i.total_vat:
                        amounts[1] += i.total_vat
            self._vat_subtotals = []
            for k, amounts in sums.items():
                (cat, rule) = k
                self._vat_subtotals.append(
                    (cat, rule, myround(amounts[0]), myround(amounts[1])))
        return self._vat_subtotals


# dd.update_field(VatDocument, 'total_incl', verbose_name=_("Total to pay"))
# dd.update_field(VatDocument, 'workflow_buttons', verbose_name=_("State"))

class VatVoucher(VatDocument, PaymentRelated, Payable, PeppolSendable):
    # todo: merge VatDocument and VatVoucher?

    class Meta:
        abstract = True

    xml_file_template = "vat/peppol-ubl.xml"
    xml_validator_file = Path(__file__).parent / 'XSD/PEPPOL-EN16931-UBL.sch'

    def store_attached_file(self, ar, data, mimetype, filename, desc, **kwargs):
        UploadType = rt.models.uploads.UploadType
        Shortcuts = rt.models.uploads.Shortcuts
        source_document = UploadType.objects.get(
            shortcut=Shortcuts.source_document)
        file = make_captured_image(data, filename=filename)
        kwargs.update(user=ar.get_user())
        kwargs.update(owner=self)
        kwargs.update(type=source_document)
        kwargs.update(description=desc)
        kwargs.update(mimetype=mimetype)
        obj = rt.models.uploads.Upload(file=file, **kwargs)
        obj.save_new_instance(ar)
        return obj


class VatItemBase(VoucherItem, VatTotal):

    class Meta:
        abstract = True

    vat_class = VatClasses.field(blank=True)

    # item_total = dd.field_alias('total_incl' if dd.plugins.vat.item_vat else 'total_base')

    @classmethod
    def override_column_headers(cls, ar, **headers):
        headers['vat_class'] = _("VCl")
        headers['total_incl'] = _("Pr.incl")
        headers['total_base'] = _("Pr.excl")
        return super().override_column_headers(ar, **headers)

    def delete(self, **kw):
        super().delete(**kw)
        v = self.voucher
        if v.edit_totals and v.items_edited:
            if not v.items.exists():
                v.items_edited = False
                v.save()

    def get_trade_type(self):
        return self.voucher.get_trade_type()

    def get_default_vat_class(self, tt):
        acc = self.get_base_account(tt)
        if acc and acc.vat_class:
            return acc.vat_class
        return dd.plugins.vat.get_vat_class(tt, self)

    def vat_class_changed(self, ar):
        # dd.logger.info("20121204 vat_class_changed")
        self.reset_totals(ar)  # #4291 (partly deducible VAAT)
        # # if self.voucher.vat_regime.item_vat:
        # if dd.plugins.vat.item_vat:
        #     self.total_incl_changed(ar)
        # else:
        #     self.total_base_changed(ar)

    def get_base_account(self, tt, ar=None):
        raise NotImplementedError

    def get_quantity(self, product):  # implement InvoicingTargetItem
        if self.product == product:
            return self.qty

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount(self, ar):  # implement InvoicingTargetItem
        if dd.plugins.vat.item_vat:
            return self.total_incl
        return self.total_base

    def get_amount(self):  # implement InvoicingTargetItem
        # if self.voucher.vat_regime.item_vat:  # unit_price_includes_vat
        if dd.plugins.vat.item_vat:
            return self.total_incl
        return self.total_base

    def set_amount(self, ar, amount):
        self.voucher.fill_defaults()
        # if self.voucher.vat_regime.item_vat:  # unit_price_includes_vat
        if dd.plugins.vat.item_vat:  # unit_price_includes_vat
            self.total_incl = myround(amount)
            self.total_incl_changed(ar)
        else:
            self.total_base = myround(amount)
            self.total_base_changed(ar)

    def reset_totals(self, ar):
        # if self.voucher.items_edited:
        if self.voucher.edit_totals and self.voucher.total_incl and not settings.SITE.loading_from_dump:
            rule = self.get_vat_rule(self.get_trade_type())
            qs = self.voucher.items.exclude(id=self.id)
            if rule.vat_returnable_account is not None:
                total = qs.aggregate(
                    models.Sum('total_base'))['total_base__sum'] or Decimal()
                self.total_base = self.voucher.total_incl - total
                self.total_base_changed(ar)
            else:
                total = qs.aggregate(
                    models.Sum('total_incl'))['total_incl__sum'] or Decimal()
                self.total_incl = self.voucher.total_incl - total
                self.total_incl_changed(ar)
        super().reset_totals(ar)

    def full_clean(self):
        if self.vat_class is None:
            self.vat_class = self.get_default_vat_class(self.get_trade_type())
        super().full_clean()

    def before_ui_save(self, ar, cw):
        if self.total_incl is None:
            self.reset_totals(ar)
        super().before_ui_save(ar, cw)

    def after_ui_save(self, ar, cw):
        """
        After editing a grid cell automatically show new invoice totals.
        """
        kw = super().after_ui_save(ar, cw)
        if self.voucher.edit_totals and not self.voucher.items_edited:
            self.voucher.items_edited = True
            self.voucher.save()
        # if self.voucher.refresh_after_item_edit:
        #     ar.set_response(refresh_all=True)
        #     self.voucher.compute_totals()
        #     self.voucher.full_clean()
        #     self.voucher.save()
        return kw

    def get_vat_rule(self, tt):
        if self.vat_class is None:
            self.vat_class = self.get_default_vat_class(tt)
            # we store it because there might come more calls, but we
            # don't save it because here's not the place to decide
            # this.

        # country = self.voucher.partner.country or \
        #           dd.plugins.countries.get_my_country()
        vat_area = VatAreas.get_for_country(self.voucher.partner.country)
        return VatRules.get_vat_rule(vat_area,
                                     trade_type=tt,
                                     vat_regime=self.voucher.vat_regime,
                                     vat_class=self.vat_class,
                                     date=self.voucher.entry_date)

    def get_peppol_vat_category(self):
        # There are at least two versions of the UNCL5305 code list
        # https://docs.peppol.eu/pracc/catalogue/1.0/codelist/UNCL5305/
        # https://docs.peppol.eu/poacc/billing/3.0/codelist/UNCL5305/
        # trade_type = self.voucher.get_trade_type()
        # if rule.trade_type.name != 'sales':
        #     return None
        # if not self.total_incl:
        #     return None
        # if rule.vat_returnable_account is not None:
        # if self.voucher.vat_regime.name in {'cocontractor', 'intracom'}:
        # if self.voucher.vat_regime.name == 'intracom':
        #     return "K"
        if self.voucher.vat_regime.reverse_charge:
            return "AE"
        # if self.vat_class.name == 'reduced':
        #     return "AA"
        if self.vat_class.name == 'exempt':
            return "Z"
        # Can happen in bevats:
        # if not self.total_vat:
        #     raise Exception(f"20240706 Oops: category S but no VAT! {self.vat_class} {self.voucher.vat_regime}")
        return "S"

    # @dd.displayfield(_("Peppol cat"))
    # def peppol_vat_category(self, ar=None):
    #     return self.get_peppol_vat_category(self.get_vat_rule(self.get_trade_type()))


decpos = dict(decimal_places=dd.plugins.vat.unit_price_decpos)

dd.update_field(
    VatItemBase, 'total_incl', verbose_name=_("Price incl. VAT"),  **decpos)
dd.update_field(
    VatItemBase, 'total_base', verbose_name=_("Price excl. VAT"), **decpos)
dd.update_field(
    VatItemBase, 'total_vat', verbose_name=_("VAT"), **decpos)


class QtyVatItemBase(VatItemBase):

    class Meta:
        abstract = True

    unit_price = dd.PriceField(
        _("Unit price"), blank=True, null=True,
        decimal_places=dd.plugins.vat.unit_price_decpos)
    qty = dd.QuantityField(_("Quantity"), blank=True, null=True)

    def unit_price_changed(self, ar=None):
        self.reset_totals(ar)

    def qty_changed(self, ar=None):
        self.reset_totals(ar)

    def reset_totals(self, ar=None):
        super().reset_totals(ar)
        # if self.voucher.edit_totals:
        #     if self.qty:
        #         if self.voucher.item_vat:
        #             self.unit_price = self.total_incl / self.qty
        #         else:
        #             self.unit_price = self.total_base / self.qty

        if self.unit_price is not None:
            if self.qty is None:
                self.set_amount(ar, self.unit_price)
            else:
                self.set_amount(ar, self.unit_price * self.qty)

    def get_vat_rule(self, tt):
        if self.product and self.product.subtotal:
            return None
        return super().get_vat_rule(tt)

    @classmethod
    def override_column_headers(cls, ar, **headers):
        headers['qty'] = _("Qty")
        headers['unit_price'] = _("UPr")
        return super().override_column_headers(ar, **headers)


# QtyVatItemBase.set_widget_options('qty', hide_sum=True)
QtyVatItemBase.set_widget_options(
    'unit_price', hide_sum=True, short_header="UP")

accounting = dd.resolve_app("accounting")


class VatDeclaration(accounting.Declaration):

    class Meta:
        abstract = True

    def get_payable_sums_dict(self, ar=None):
        # side effect : calling this will also update the fields and save the
        # declaration.
        fields = self.fields_list.get_list_items()
        payable_sums = SumCollector()
        sums = dict()  # field sums
        for fld in fields:
            if fld.editable:
                sums[fld.name] = getattr(self, fld.name)
            else:
                sums[fld.name] = Decimal('0.00')  # ZERO
        flt = dict(voucher__journal__must_declare=True)
        if self.start_period:
            flt = self.get_period_filter(
                'voucher__accounting_period',
                voucher__journal__preliminary=False, **flt)
        qs = rt.models.accounting.Movement.objects.filter(**flt)
        qs = qs.order_by('voucher__journal', 'voucher__number')

        # print(20170713, qs)

        for mvt in qs:
            for fld in fields:
                fld.collect_from_movement(self, mvt, sums, payable_sums)
                # if fld.is_payable:
                #     print("20170802 after {} {} : {}".format(
                #         fld, mvt.amount, payable_sums))

        for fld in fields:
            fld.collect_from_sums(self, sums, payable_sums)

            # dd.logger.info("20170713 value in 55 is %s", sums['F55'])

        for fld in fields:
            if not fld.editable:
                setattr(self, fld.name, sums[fld.name])

        # side effect!:
        self.full_clean()
        self.save()

        return payable_sums

    def print_declared_values(self):
        # used in doctests
        for fld in self.fields_list.get_list_items():
            v = getattr(self, fld.name)
            if v:
                print("[{}] {} : {}".format(fld.value, fld.help_text, v))

    def intracom_statement_iterator(self):
        intracom_regimes = set([
            r for r in VatRegimes.get_list_items() if r.vat_area == VatAreas.eu
        ])

        def annotator():

            def build_case(model):

                def get_filter():
                    filter_kw = dict(partner__pk=OuterRef('pk'),
                                     journal__trade_type=TradeTypes.sales,
                                     vat_regime__in=intracom_regimes)
                    filter_kw.update(
                        self.get_period_filter("accounting_period"))
                    return filter_kw

                return Case(When(
                    ~Exists(model.objects.filter(**get_filter()).values('pk')),
                    then=Value(0.0)),
                            default=Subquery(
                                model.objects.filter(**get_filter()).order_by(
                                ).values('partner').annotate(
                                    total_by_partner=Sum('total_base')).values(
                                        'total_by_partner')),
                            output_field=models.DecimalField())

            kw = dict(vai_base=build_case(rt.models.vat.VatAccountInvoice))
            if dd.is_installed('trading'):
                kw['vpi_base'] = build_case(
                    rt.models.trading.VatProductInvoice)
            else:
                kw['vpi_base'] = Cast(
                    Value(0.0), output_field=models.DecimalField())
            return kw

        qs = rt.models.contacts.Partner.objects.annotate(
            **annotator()).annotate(total_base=F('vai_base')
                                    + F('vpi_base')).filter(total_base__gt=0)

        for p in qs:
            yield p
