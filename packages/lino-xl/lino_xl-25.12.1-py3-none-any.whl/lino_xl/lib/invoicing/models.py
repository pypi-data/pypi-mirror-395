# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from datetime import timedelta

from django.db import models
from django.db.utils import OperationalError, ProgrammingError
from django.conf import settings
from django.utils.text import format_lazy
from django.utils import translation
from django.core.exceptions import ValidationError

from lino.core.gfks import GenericForeignKey, ContentType
from lino.core.exceptions import UnresolvedChoice
from lino.modlib.gfks.fields import GenericForeignKeyIdField
from lino.utils.mldbc.mixins import BabelDesignated
from lino.modlib.users.mixins import UserPlan, UserAuthored
from lino import logger
from lino.mixins import Sequenced
from lino.api import dd, rt, _
from lino.modlib.linod.mixins import Runnable
from lino.modlib.linod.choicelists import schedule_daily
from lino_xl.lib.accounting.utils import ZERO
# from lino_xl.lib.accounting.roles import LedgerUser, LedgerStaff

from .mixins import InvoiceGenerator
from .actions import (ToggleSelection, StartInvoicing,
                      StartInvoicingForPartner, StartInvoicingForOrder,
                      ExecutePlan, ExecuteItem)
from .ui import *

order_model = dd.plugins.invoicing.order_model
generator_label = _("Generator")


class Task(Runnable, UserAuthored):

    class Meta:
        app_label = 'invoicing'
        abstract = dd.is_abstract_model(__name__, "Task")
        verbose_name = _("Invoicing task")
        verbose_name_plural = _("Invoicing tasks")

    # start_invoicing = StartInvoicingByTask()

    target_journal = dd.ForeignKey(
        'accounting.Journal',
        verbose_name=_("Target journal"),
        # null=True,
        # blank=True,
        related_name="invoicing_task_targets")

    max_date_offset = models.IntegerField(_("Max date offset"), default=-1)
    today_offset = models.IntegerField(_("Invoice date offset"), default=0)

    def get_action_name(self):
        return "start_invoicing_{}".format(self.pk)

    def run_task(self, ar):
        plan = rt.models.invoicing.Plan.create_user_plan(self.user)
        sar = ar.spawn_request(user=self.user)
        plan.update_plan.run_from_ui(sar)
        plan.execute_plan.run_from_ui(sar)

    def full_clean(self, *args, **kwargs):
        if not self.name:
            self.name = _("Make {}").format(self.target_journal)
        super().full_clean(*args, **kwargs)

    def get_invoice_generators(self):
        for o in FollowUpRule.objects.filter(invoicing_task=self):
            if o.invoice_generator is not None:
                yield o.invoice_generator.model_class()

    def get_generator_models(self):
        ContentType = rt.models.contenttypes.ContentType
        return [ContentType.objects.get_for_model(m)
                for m in rt.models_by_base(InvoiceGenerator)]

    def get_source_journals(self):
        for o in FollowUpRule.objects.filter(invoicing_task=self):
            if o.source_journal is not None:
                yield o.source_journal

    # def get_target_journals(self):
    #     for o in FollowUpRule.objects.filter(invoicing_task=self):
    #         if o.target_journal is not None:
    #             yield o.target_journal

    # @dd.displayfield(_("Invoice generators"))
    # def invoice_generators(self, ar):
    #     if ar is None:
    #         return None
    #     return ", ".join(
    #         [dd.full_model_name(m) for m in self.get_invoice_generators()])

    @dd.displayfield(_("Source journals"))
    def source_journals(self, ar):
        if ar is None:
            return None
        return ", ".join(
            [ar.obj2htmls(jnl, jnl.ref) for jnl in self.get_source_journals()])

    # @dd.displayfield(_("Target journals"))
    # def target_journals(self, ar):
    #     if ar is None:
    #         return None
    #     return ", ".join([ar.obj2htmls(jnl, jnl.ref)
    #         for jnl in self.get_target_journals()])


# dd.update_field(Task, 'user', verbose_name=_("Responsible user"))


class FollowUpRule(Sequenced):

    class Meta:
        app_label = 'invoicing'
        verbose_name = _("Follow-up rule")
        verbose_name_plural = _("Follow-up rules")

    # invoicing_area = InvoicingAreas.field()
    invoicing_task = dd.ForeignKey("invoicing.Task")
    # source_journal = dd.ForeignKey(
    #     'accounting.Journal', related_name="followup_source")
    invoice_generator = dd.ForeignKey(
        'contenttypes.ContentType',
        # editable=True,
        # blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set",
        verbose_name=_("Invoice generator"))

    source_journal = dd.ForeignKey('accounting.Journal',
                                   verbose_name=_("Source journal"),
                                   null=True,
                                   blank=True,
                                   related_name="followup_source")
    # target_journal = dd.ForeignKey(
    #     'accounting.Journal', verbose_name=_("Target journal"), null=True, blank=True,
    #     related_name="followup_target")

    allow_cascaded_delete = "invoicing_task source_journal"

    @dd.chooser()
    def source_journal_choices(cls, invoicing_task):
        if not invoicing_task:
            return []
        return invoicing_task.get_source_journals()

    @dd.chooser()
    def invoice_generator_choices(cls, invoicing_task):
        if not invoicing_task:
            return []
        return invoicing_task.get_generator_models()

    def full_clean(self, *args, **kw):
        super().full_clean(*args, **kw)
        ig = self.invoice_generator.model_class()
        if not issubclass(ig, InvoiceGenerator):
            raise ValidationError("{} is not an InvoiceGenerator".format(ig))


#     @classmethod
#     def find_for_model(cls, model):
#         return cls.objects.filter(source_journal=journal).first()


# class SubscriptionType(BabelDesignated):
#     class Meta(object):
#         app_label = 'invoicing'
#         abstract = dd.is_abstract_model(__name__, 'SubscriptionType')
#         verbose_name = _("Subscription type")
#         verbose_name_plural = _("Subscription types")
#
#     renew_every = models.IntegerField(_("Renew every"), default=1)
#     renew_by = DurationUnits.field(_("Renew by"), blank=True, null=True)
#     renew_before = models.IntegerField(_("Renew before"), default=0)
#
#
# class SubscriptionTypes(dd.Table):
#     required_roles = dd.login_required(LedgerUser)
#     model = "invoicing.SubscriptionType"
#     column_names = "designation renew_every renew_by *"
#     order_by = ['designation']


class Tariff(BabelDesignated):

    class Meta(object):
        app_label = 'invoicing'
        abstract = dd.is_abstract_model(__name__, 'Tariff')
        verbose_name = _("Flatrate")
        verbose_name_plural = _("Flatrates")

    # allow_cascaded_delete = 'product'

    # product = dd.OneToOneField('products.Product', primary_key=True)
    product = dd.ForeignKey('products.Product', blank=True, null=True)

    number_of_events = models.IntegerField(
        _("Number of events"),
        blank=True,
        null=True,
        help_text=_("Number of events paid per invoicing."))

    min_asset = models.IntegerField(
        _("Minimum threshold"),
        blank=True,
        null=True,
        help_text=_("Minimum quantity to pay in advance."))

    max_asset = models.IntegerField(
        _("Maximum threshold"),
        blank=True,
        null=True,
        help_text=_("Maximum quantity to pay per period."))

    # invoicing_cycle = InvoicingCycles.field(default="once")


# @dd.receiver(dd.post_save, sender='products.Product')
# def create_tariff(sender, instance, created, **kwargs):
#     if created and not settings.SITE.loading_from_dump:
#         if not hasattr(instance, 'tariff'):
#             rt.models.invoicing.Tariff.objects.create(product=instance)

# class Area(BabelDesignated, Sequenced):
#     class Meta:
#         app_label = 'invoicing'
#         abstract = dd.is_abstract_model(__name__, 'Area')
#         verbose_name = _("Invoicing area")
#         verbose_name_plural = _("Invoicing areas")
#
#     # designation = dd.CharField(max_length=100)
#     journal = dd.ForeignKey('accounting.Journal', blank=True, null=True)
#
#     # start_invoicing = StartInvoicingForArea()
#
#     # def __str__(self):
#     #     return str(self.designation)
#
#     @dd.chooser()
#     def journal_choices(cls):
#         vt = dd.plugins.invoicing.get_voucher_type()
#         return rt.models.accounting.Journal.objects.filter(voucher_type=vt)
#
#     def full_clean(self):
#         if self.journal is None:
#             vt = dd.plugins.invoicing.get_voucher_type()
#             # print("20220707", vt, vt.get_journals())
#             self.journal = vt.get_journals().first()
#             # raise Exception("20220707")
#
#         # if not self.designation:
#         #     self.designation = str(self.journal)
#         super(Area, self).full_clean()
#
#
# class Areas(dd.Table):
#     required_roles = dd.login_required(LedgerStaff)
#     model = "invoicing.Area"
#     column_names = "seqno designation journal *"
#


class Plan(UserPlan):

    class Meta:
        app_label = 'invoicing'
        abstract = dd.is_abstract_model(__name__, 'Plan')
        verbose_name = _("Invoicing plan")
        verbose_name_plural = _("Invoicing plans")

    # invoicing_area = InvoicingAreas.field(default="default")
    invoicing_task = dd.ForeignKey('invoicing.Task', null=True, blank=True)
    # 20250212 invoicing_task = dd.ForeignKey('invoicing.Task')
    # target_journal = dd.ForeignKey('accounting.Journal', blank=True, null=True)
    min_date = models.DateField(_("Invoiceables from"), null=True, blank=True)
    max_date = models.DateField(_("until"), null=True, blank=True)
    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)
    order = dd.ForeignKey(order_model, blank=True, null=True)
    # provision_product = dd.ForeignKey(
    #     'products.Product',
    #     verbose_name=_("Provision product"),
    #     blank=True,
    #     null=True,
    #     related_name="products_by_invoicing_plan")

    # start_plan = StartInvoicing()
    execute_plan = ExecutePlan()
    toggle_selections = ToggleSelection()

    # @classmethod
    # def create_user_plan(cls, user, **options):
    #     options.update(target_journal=None)
    #     return super().create_user_plan(user, **options)

    # def __str__(self):  # 20250212
    # #     # if self.target_journal is None:
    # #     #     return "{0} plan by {1}".format(
    # #     #         self.invoicing_task, self.user)
    # #     return _("{plan} by {user}").format(plan=self._meta.verbose_name, self.user)
    #     if self.invoicing_task:
    #         return "{0} to {1} plan by {2}".format(
    #             self.invoicing_task, self.invoicing_task.target_journal,
    #             self.user)
    #     return self._meta.verbose_name
    #     # return str(self.user)

    # @dd.chooser()
    # def target_journal_choices(cls, invoicing_task):
    #     if invoicing_task:
    #         return invoicing_task.get_target_journals()
    #     return []

    # def full_clean(self):
    #     # if not self.invoicing_area:
    #     #     if self.order:
    #     #         self.invoicing_area = FollowUpRule.find_for_model(self.order.__class__).invoicing_area
    #     super().full_clean()
    #     target_journals = list(self.invoicing_task.get_target_journals())
    #     if self.target_journal is None:
    #         if len(target_journals) > 0:
    #             self.target_journal = target_journals[0]
    #     elif not self.target_journal in target_journals:
    #         raise ValidationError("Journal {} is not a target for {}".format(
    #             self.target_journal, self.invoicing_task))
    #     # if not issubclass(self.target_journal.voucher_type.model, dd.plugins.invoicing.voucher_model):
    #     #     raise ValidationError("Journal {} is not on {}".format(
    #     #         self.target_journal, dd.plugins.invoicing.voucher_model))

    # def get_target_journal(self):
    #     # return self.target_journal
    #     return self.invoicing_task.target_journal

    def get_max_date(self):
        if self.invoicing_task_id is None:
            return None
        if self.max_date:
            return self.max_date
        return self.today + timedelta(days=self.invoicing_task.max_date_offset)

    def get_generators_for_plan(self, partner=None):
        for m in rt.models_by_base(InvoiceGenerator):
            if not m.has_generators_for_plan(self, partner):
                logger.debug("20240120 %s has no generators for %s", m, self)
                # print("20230624 has no generators:", m)
                continue
            logger.debug("20240120 Ask %s to get_generators_for_plan()", m)
            for obj in m.get_generators_for_plan(self, partner):
                # print("20210727", obj)
                # if obj.get_invoiceable_product(self) is not None:
                yield obj

    def reset_plan(self):
        self.items.all().delete()

    def run_update_plan(self, ar):
        # logger.debug("20240120 run_update_plan() %s", self)
        self.reset_plan()
        self.fill_plan(ar)

    def fill_plan(self, ar):
        # logger.debug("20240120 fill_plan() %s", self)
        # print("20230515 fill", self.invoicing_area.value,
        #     "plan(", self.min_date, self.max_date, ") -> ", self.target_journal)
        self.full_clean()
        Item = rt.models.invoicing.Item
        collected = dict()
        max_date = self.get_max_date()
        jnl = self.invoicing_task.target_journal
        for ig in self.get_generators_for_plan(self.partner):
            partner = ig.get_invoiceable_partner()
            if partner is None:
                # raise Exception("{!r} has no invoice recipient".format(ig))
                continue
            # logger.debug("20240120 %s %s", ig, partner)
            partner = partner.get_invoice_recipient(jnl.trade_type)
            invoice = self.create_invoice(partner=partner, user=ar.get_user())

            info = ig.compute_invoicing_info(self.min_date, max_date)
            # if not info.invoiceable_product:
            #     continue
            # print("20200425", ig, info, invoice)

            invoice_items = list(ig.get_wanted_invoice_items(
                info, invoice, ar))
            if len(invoice_items) == 0:
                # dd.logger.info("20230515 no invoice items for %s", ig)
                continue

            logger.debug("20230515 %s makes invoice %s for %s with items %s",
                         ig, invoice.journal, partner,
                         [i.product for i in invoice_items])

            # assert invoice.pk is None
            # for i in invoice_items:
            #     assert i.pk is None

            # print("20210731 collect", self, ig, collected)
            if ig.allow_group_invoices():
                item = collected.get(partner.pk, None)
                if item is None:
                    item = Item(plan=self, partner=partner, preview="")
                    collected[partner.pk] = item
                    # item.preview = ""
            else:
                item = Item(plan=self,
                            partner=partner,
                            generator=ig,
                            preview="")
                # collected[obj] = item
                # item.preview = ""

            # item.preview = "" # _("{} items").format(len(invoice_items))
            # total_amount = ZERO
            for n, i in enumerate(invoice_items):
                # i.discount_changed()
                # total_amount += i.get_amount() or ZERO
                item.amount += i.get_amount() or ZERO
                # item.qty += i.get_quantity(self.provision_product) or ZERO
                item.number += 1

                if item.number < ItemsByPlan.row_height:
                    if item.preview:
                        item.preview += '<br>\n'
                    ctx = dict(title=i.title or i.product,
                               amount=i.get_amount() or ZERO,
                               currency=dd.plugins.accounting.currency_symbol)
                    tpl = "{title} ({amount} {currency})"
                    # if self.provision_product is None:
                    #     tpl = "{title} ({amount} {currency})"
                    # else:
                    #     ctx.update(qty=i.get_quantity() or ZERO)
                    #     ctx.update(unit=self.provision_product.delivery_unit)
                    #     tpl = "{title} ({qty} {unit})"
                    item.preview += tpl.format(**ctx)
                elif item.number == ItemsByPlan.row_height:
                    item.preview += '...'

            # item.amount = total_amount
            # item.number_of_invoiceables += 1
            item.full_clean()
            item.save()

    def create_invoice(self, **kwargs):
        # ITEM_MODEL = dd.plugins.invoicing.item_model
        # M = dd.plugins.invoicing.default_voucher_view.model
        # source_journal = self.invoicing_area.source_journal
        # M = self.source_journal.voucher_type.model
        # 20230522 M = dd.plugins.invoicing.voucher_model
        # M = ITEM_MODEL._meta.get_field('voucher').remote_field.model
        # jnl = self.get_target_journal()
        if self.invoicing_task_id is None:
            raise Warning(_("No invoicing task specified"))
        jnl = self.invoicing_task.target_journal
        today = self.today
        if self.invoicing_task.today_offset:
            today += timedelta(days=self.invoicing_task.today_offset)
        kwargs.update(journal=jnl, entry_date=today)
        # print("20221217 gonna create", M)
        # if issubclass(M, dd.plugins.invoicing.voucher_model):
        kwargs.update(invoicing_min_date=self.min_date,
                      invoicing_max_date=self.get_max_date())
        # 20230522 invoice = M(**kwargs)
        invoice = jnl.voucher_type.model(**kwargs)
        # invoice.fill_defaults()
        invoice.full_clean()
        return invoice


class Item(dd.Model):

    class Meta:
        app_label = 'invoicing'
        abstract = dd.is_abstract_model(__name__, 'Item')
        verbose_name = _("Invoicing suggestion")
        verbose_name_plural = _("Invoicing suggestions")

    plan = dd.ForeignKey('invoicing.Plan', related_name="items")
    partner = dd.ForeignKey('contacts.Partner')
    # invoice_recipient = dd.ForeignKey(
    #     'contacts.Partner', blank=True, null=True,
    #     related_name="items_by_invoice_recipient")

    generator_type = dd.ForeignKey(ContentType,
                                   editable=True,
                                   blank=True,
                                   null=True,
                                   verbose_name=format_lazy(
                                       "{} {}", generator_label, _('(type)')))
    generator_id = GenericForeignKeyIdField(generator_type,
                                            editable=True,
                                            blank=True,
                                            null=True,
                                            verbose_name=format_lazy(
                                                "{} {}", generator_label,
                                                _('(object)')))
    generator = GenericForeignKey('generator_type',
                                  'generator_id',
                                  verbose_name=generator_label)

    # first_date = models.DateField(_("First date"))
    # last_date = models.DateField(_("Last date"))
    number = models.IntegerField(_("Invoiceables"), default=ZERO)
    amount = dd.PriceField(_("Amount"), default=ZERO)
    # qty = dd.QuantityField(_("Quantity"), default=ZERO)
    # number_of_invoiceables = models.IntegerField(_("Number"), default=0)
    preview = models.TextField(_("Preview"), blank=True, editable=False)
    selected = models.BooleanField(_("Selected"), default=True)
    invoice = dd.ForeignKey(
        # 20230522 dd.plugins.invoicing.voucher_model,
        'accounting.Voucher',
        verbose_name=_("Invoice"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    allow_cascaded_delete = ['plan', 'partner']

    exec_item = ExecuteItem()

    @dd.displayfield(_("Invoice"))
    def invoice_button(self, ar):
        if ar is not None:
            if self.invoice_id:
                return self.invoice.as_summary_item(ar)
            ba = ar.actor.get_action_by_name('exec_item')
            if ar.actor.get_row_permission(self, ar, None, ba):
                return ar.action_button(ba, self)
        return ''

    def create_invoice(self, ar):
        if self.plan.invoicing_task_id is None:
            raise Warning(_("No invoicing task specified"))
        # if self.plan.target_journal is None:
        #     raise Warning(_("No target journal specified for {}").format(self.plan.invoicing_area))
        invoice = self.plan.create_invoice(partner=self.partner,
                                           user=ar.get_user())
        lng = invoice.get_print_language()
        items = []
        max_date = self.plan.get_max_date()
        with translation.override(lng):
            if self.generator:
                generators = [self.generator]
            else:
                generators = [
                    ig
                    for ig in self.plan.get_generators_for_plan(self.partner)
                    if ig.allow_group_invoices()
                ]
                # assert len(generators) > 0
            for ig in generators:
                info = ig.compute_invoicing_info(self.plan.min_date, max_date)
                pt = ig.get_invoiceable_payment_term()
                if pt:
                    invoice.payment_term = pt
                pt = ig.get_invoiceable_paper_type()
                if pt:
                    invoice.paper_type = pt

                # ig.setup_invoice_from_suggestion(invoice, self.plan, info)

                for i in ig.get_wanted_invoice_items(info, invoice, ar):
                    # print("20230710 got invoice item", i, i.product, info.invoiceable_product)
                    if i.product == info.invoiceable_product:
                        i.invoiceable = ig
                    # kwargs.update(voucher=invoice)
                    # i = ITEM_MODEL(**kwargs)
                    # if 'amount' in kwargs:
                    #     i.set_amount(ar, kwargs['amount'])
                    # amount = kwargs.get('amount', ZERO)
                    # if amount:
                    #     i.set_amount(ar, amount)
                    items.append((ig, i))

        if len(items) == 0:
            # neither invoice nor items are saved
            raise Warning(_("Nothing to invoice for %s.") % self)
            # dd.logger.warning(
            #     _("No invoiceables found for %s.") % self.partner)
            # return

        invoice.full_clean()
        invoice.save()

        for ig, i in items:
            # assert i.voucher is None
            # assign voucher after it has been saved
            i.voucher = invoice
            ig.setup_invoice_item(i)
            # if not i.title:
            #     i.title = ig.get_invoiceable_title(invoice)
            # compute the sales_price and amounts, but don't change
            # title and description

            # title = i.title
            # i.product_changed()
            # i.discount_changed()
            # i.title = title
            i.full_clean()
            i.save()

        self.invoice = invoice
        self.full_clean()
        self.save()

        invoice.after_create_invoice()
        invoice.full_clean()
        invoice.save()
        invoice.register(ar)

        for ig in generators:
            ig.after_invoicing(ar, invoice)

        return invoice

    def __str__(self):
        return _("{0} for {1}").format(
            self.plan, self.partner or _("All partners"))


# dd.inject_field(
#     'products.Product', 'tariff', dd.ForeignKey(
#         'invoicing.Tariff', blank=True, null=True))

# VOUCHER_MODEL = dd.plugins.invoicing.voucher_model
# dd.inject_field(
#     VOUCHER_MODEL, 'invoicing_min_date', dd.DateField(
#         _("Invoiceables from"), blank=True, null=True))
# dd.inject_field(
#     VOUCHER_MODEL, 'invoicing_max_date', dd.DateField(
#         _("until"), blank=True, null=True))

# dd.inject_field(
#     'accounting.Journal', 'invoicing_area',
#     InvoicingAreas.field(null=True, blank=True))

# dd.inject_field(
#     'accounting.Journal', 'invoiceable_product',
#     dd.ForeignKey('products.Product', blank=True, null=True))

# dd.inject_field(
#     dd.plugins.invoicing.item_model,
#     'invoiceable_type', dd.ForeignKey(
#         ContentType,
#         blank=True, null=True,
#         verbose_name=format_lazy("{} {}",invoiceable_label, _('(type)'))))
# dd.inject_field(
#     dd.plugins.invoicing.item_model,
#     'invoiceable_id', GenericForeignKeyIdField(
#         'invoiceable_type',
#         blank=True, null=True,
#         verbose_name=format_lazy("{} {}",invoiceable_label, _('(object)'))))
# dd.inject_field(
#     dd.plugins.invoicing.item_model,
#     'invoiceable', GenericForeignKey(
#         'invoiceable_type', 'invoiceable_id',
#         verbose_name=invoiceable_label))
#
# # dd.inject_field(
# #     dd.plugins.invoicing.item_model,
# #     'item_no', models.IntegerField(_("Iten no."))
#
# # define a custom chooser because we want to see only invoiceable
# # models when manually selecting an invoiceable_type:
# @dd.chooser()
# def invoiceable_type_choices(cls):
#     return ContentType.objects.get_for_models(
#         *rt.models_by_base(InvoiceGenerator)).values()
#
# dd.inject_action(
#     dd.plugins.invoicing.item_model,
#     invoiceable_type_choices=invoiceable_type_choices)

# 20181115 : note this feature doesn't work when a generator creates
# more than one item because it would now require an additional field
# item_no per invoice item.
# @dd.receiver(dd.pre_save, sender=dd.plugins.invoicing.item_model)
# def item_pre_save_handler(sender=None, instance=None, **kwargs):
#     """
#     When the user sets `title` of an automatically generated invoice
#     item to an empty string, then Lino restores the default value for
#     title and description
#     """
#     self = instance
#     if self.invoiceable_id and not self.title:
#         lng = self.voucher.get_print_language()
#         # lng = self.voucher.partner.language or dd.get_default_language()
#         with translation.override(lng):
#             self.title = self.invoiceable.get_invoiceable_title(self.voucher)
#             self.invoiceable.setup_invoice_item(self)

# def get_invoicing_voucher_type():
#     voucher_model = dd.resolve_model(dd.plugins.invoicing.voucher_model)
#     vt = VoucherTypes.get_for_model(voucher_model)


@dd.receiver(dd.pre_analyze)
def install_start_actions(sender=None, **kwargs):
    # vt = dd.plugins.invoicing.get_voucher_type()
    # vt.table_class.start_invoicing = StartInvoicingForJournal()
    try:
        for it in rt.models.invoicing.Task.objects.filter(disabled=False):
            an = it.get_action_name()
            if not dd.plugins.invoicing.use_default_record_id:
                rt.models.system.SiteConfig.define_action(
                    **{an: StartInvoicing(it)})
            rt.models.contacts.Partner.define_action(
                **{an: StartInvoicingForPartner(it)})
            m = dd.plugins.invoicing.order_model
            if m is not None:
                m.define_action(**{an: StartInvoicingForOrder(it)})
    except (OperationalError, ProgrammingError, UnresolvedChoice) as e:
        dd.logger.debug("Failed to set invoicing actions : %s", e)

# @dd.background_task(every_unit="monthly", every=1)


@schedule_daily(class_name='invoicing.Task')
def run_invoicing_tasks(ar):
    pass
