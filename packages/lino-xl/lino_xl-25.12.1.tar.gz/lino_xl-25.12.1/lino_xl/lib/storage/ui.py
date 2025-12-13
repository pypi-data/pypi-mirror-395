# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from lino import mixins
from lino.api import dd, rt, _
from lino.core import constants
from lino.utils import join_elems
from lino.utils.html import E
from lino_xl.lib.accounting.choicelists import JournalGroups
from lino_xl.lib.accounting.mixins import JournalRef
from lino_xl.lib.accounting.ui import PartnerVouchers, ByJournal
from lino_xl.lib.accounting.choicelists import VoucherTypes
from lino_xl.lib.invoicing.ui import InvoicingsByGenerator

from .roles import StorageUser, StorageStaff


class TransferRules(dd.Table):
    required_roles = dd.login_required(StorageStaff)
    model = 'storage.TransferRule'
    column_names = "seqno journal from_state to_state *"


class TransferRulesByJournal(TransferRules):
    master_key = 'journal'
    params_layout = None


class Movements(dd.Table):
    editable = False  # only MovementsByPartner is editable (and only the match field)
    model = 'storage.Movement'
    required_roles = dd.login_required(StorageUser)
    column_names = 'value_date voucher_link description \
    debit credit #match_link cleared *'

    sum_text_column = 2
    order_by = ['id']

    parameters = mixins.ObservedDateRange(
        year=dd.ForeignKey('periods.StoredYear', blank=True),
        journal_group=JournalGroups.field(blank=True),
        partner=dd.ForeignKey('contacts.Partner', blank=True, null=True),
        product=dd.ForeignKey('products.Product', blank=True, null=True),
        journal=JournalRef(blank=True),
        cleared=dd.YesNo.field(_("Show cleared movements"), blank=True))
    params_layout = """
    start_period end_period start_date end_date cleared
    journal_group journal year partner product"""

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        qs = super().get_request_queryset(ar, **kwargs)

        if (pv := ar.param_values) is None:
            return qs
        if pv.cleared == dd.YesNo.yes:
            qs = qs.filter(cleared=True)
        elif pv.cleared == dd.YesNo.no:
            qs = qs.filter(cleared=False)

        if pv.start_date:
            qs = qs.filter(value_date__gte=pv.start_date)
        if pv.end_date:
            qs = qs.filter(value_date__lte=pv.end_date)

        # if ar.param_values.partner:
        #     qs = qs.filter(partner=ar.param_values.partner)
        # if ar.param_values.paccount:
        #     qs = qs.filter(account=ar.param_values.paccount)
        if pv.year:
            qs = qs.filter(voucher__fiscal_year=pv.year)
        if pv.journal_group:
            qs = qs.filter(voucher__journal__journal_group=pv.journal_group)
        if pv.journal:
            qs = qs.filter(voucher__journal=pv.journal)
        return qs

    @classmethod
    def get_sum_text(self, ar, sums):
        bal = sums['debit'] - sums['credit']
        return _("Balance {1} ({0} movements)").format(ar.get_total_count(),
                                                       bal)

    @classmethod
    def get_simple_parameters(cls):
        p = list(super(Movements, cls).get_simple_parameters())
        p.append('partner')
        p.append('product')
        return p

    @classmethod
    def get_title_tags(cls, ar):
        for t in super(Movements, cls).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.journal is not None:
            yield pv.journal.ref
        if pv.journal_group is not None:
            yield str(pv.journal_group)
        if pv.year is not None:
            yield str(pv.year)
        if pv.cleared == dd.YesNo.no:
            yield str(_("only uncleared"))
        elif pv.cleared == dd.YesNo.yes:
            yield str(_("only cleared"))

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        # raise Exception("20191003")
        if ar is None:
            return ''
        elems = []
        elems.append(ar.obj2html(self.product))
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
        return E.p(*join_elems(elems, " / "))


class AllMovements(Movements):
    required_roles = dd.login_required(StorageStaff)


class MovementsByVoucher(Movements):
    # master = 'storage.Voucher'
    master_key = 'voucher'
    column_names = 'product debit credit cleared *'
    sum_text_column = 3
    # auto_fit_column_widths = True
    default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    order_by = ('seqno', 'value_date', 'product__id', 'id')


class MovementsByPartner(Movements):
    editable = True
    allow_create = False
    master_key = 'partner'
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    # auto_fit_column_widths = True
    # order_by = ['-value_date', 'voucher__id', 'account__ref']
    order_by = ('-value_date', 'voucher__id', 'product__id', 'id')
    column_names = 'value_date voucher_link description \
    debit credit match cleared *'

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        # kw.update(cleared=dd.YesNo.no)
        kw.update(year=None)
        return kw

    @classmethod
    def setup_request(self, ar):
        ar.no_data_text = _("No uncleared movements")

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        # raise Exception("20191003")
        if ar is None:
            return ''
        elems = []
        elems.append(ar.obj2html(self.product))
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
            # if voucher.narration:
            #     elems.append(voucher.narration)
            # p = voucher.get_partner()
            # if p is not None and p != ar.master_instance:
            #     elems.append(ar.obj2html(p))
        return E.p(*join_elems(elems, " | "))


class MovementsByFiller(MovementsByPartner):

    # master = 'storage.Filler'

    @classmethod
    def cast_master_instance(cls, obj):
        # we have a filler but need a partner
        if isinstance(obj, rt.models.storage.Filler):
            return obj.partner
        return obj

    # @classmethod
    # def get_master_instance(cls, ar, model, pk):
    #     # the master instance of MovementsByPartner must be a partner, but since
    #     # we use this on a Filler, we get the pk of a filler
    #     assert model is rt.models.contacts.Partner
    #     filler = rt.models.storage.Filler.objects.get(pk=pk)
    #     # print("20240731", filler)
    #     return filler.partner


class MovementsByProduct(Movements):
    master_key = 'product'
    column_names = 'value_date voucher_link description \
    debit credit #match_link *'

    # order_by = ['-value_date']
    # auto_fit_column_widths = True
    # default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    # order_by = ['-value_date', 'account__ref', 'project', 'id']
    order_by = ('-value_date', 'partner__name', 'id')

    # @classmethod
    # def param_defaults(cls, ar, **kw):
    #     kw = super().param_defaults(ar, **kw)
    #     if ar.master_instance is not None and ar.master_instance.clearable:
    #         kw.update(cleared=dd.YesNo.no)
    #         kw.update(year=None)
    #     return kw

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        if ar is None:
            return ''
        elems = []
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
        return E.p(*join_elems(elems, " / "))


class MovementsByMatch(Movements):
    column_names = 'value_date voucher_link description '\
                   'debit credit cleared *'
    master = str  # 'accounting.Matching'
    variable_row_height = True
    order_by = ('-value_date', 'product__ref', 'id')

    details_of_master_template = _("%(details)s matching '%(master)s'")

    @classmethod
    def get_master_instance(self, ar, model, pk):
        """No database lookup, just return the primary key"""
        # if not pk:
        #     return None
        return pk

    @classmethod
    def get_request_queryset(cls, ar, **kwargs):
        qs = super(MovementsByMatch, cls).get_request_queryset(ar, **kwargs)
        qs = qs.filter(match=ar.master_instance)
        return qs

    @dd.displayfield(_("Description"))
    def description(cls, self, ar):
        if ar is None:
            return ''
        elems = []
        elems.append(ar.obj2html(self.product))
        if self.voucher.narration:
            elems.append(self.voucher.narration)
        voucher = self.voucher.get_mti_leaf()
        if voucher is not None:
            elems.extend(voucher.get_movement_description(self, ar))
        return E.p(*join_elems(elems, " / "))


class Provisions(dd.Table):
    model = 'storage.Provision'
    required_roles = dd.login_required(StorageUser)


class ProvisionsByProduct(Provisions):
    master_key = 'product'


class ProvisionsByPartner(Provisions):
    master_key = 'partner'


class Components(dd.Table):
    required_roles = dd.login_required(StorageStaff)
    model = 'storage.Component'
    column_names = "parent child qty *"


class ComponentsByParent(Components):
    master_key = 'parent'
    required_roles = dd.login_required(StorageUser)
    column_names = "child qty *"
    default_display_modes = {None: constants.DISPLAY_MODE_GRID}


class DeliveryNoteDetail(dd.DetailLayout):
    main = """
    left right
    ItemsByDeliveryNote
    """

    left = """
    id journal number
    partner
    narration
    """

    right = """
    entry_date voucher_date accounting_period
    invoicing_min_date invoicing_max_date
    workflow_buttons printed
    """


# class DeliveryNotes(PartnerVouchers):
class DeliveryNotes(dd.Table):
    model = 'storage.DeliveryNote'
    required_roles = dd.login_required(StorageUser)
    detail_layout = "storage.DeliveryNoteDetail"

    show_movements = dd.ShowSlaveTable('storage.MovementsByVoucher',
                                       button_text="⚖")  # 2696
    # react_icon_name="pi-book",


class DeliveryNotesByJournal(ByJournal, DeliveryNotes):
    column_names = "number_with_year entry_date " \
        "partner workflow_buttons invoicing_min_date invoicing_max_date *"
    insert_layout = """
    partner
    entry_date
    """
    order_by = ["accounting_period", "number"]


class DeliveryItems(dd.Table):
    model = 'storage.DeliveryItem'
    required_roles = dd.login_required(StorageUser)
    column_names = "seqno title product qty move_buttons invoiceable *"
    order_by = ["seqno"]


class ItemsByDeliveryNote(DeliveryItems):
    master_key = 'voucher'


VoucherTypes.add_item_lazy(DeliveryNotesByJournal, _("Delivery notes"))


class DeliveriesByGenerator(InvoicingsByGenerator):
    model = 'storage.DeliveryItem'
    column_names = "voucher qty title #description:20x1 #discount_rate #discount_amount *"


class FillerDetail(dd.DetailLayout):
    main = """
    partner
    provision_state provision_product min_asset fill_asset #filler_product
    MovementsByFiller
    """


class Fillers(dd.Table):
    model = 'storage.Filler'
    required_roles = dd.login_required(StorageUser)
    detail_layout = "storage.FillerDetail"


class FillersByPartner(Fillers):
    master_key = "partner"
    column_names = "provision_state provision_product min_asset fill_asset #filler_product"


class FillersByProduct(Fillers):
    master_key = "provision_product"
    column_names = "provision_state partner min_asset fill_asset *"


# class FillersByJournal(ByJournal, Fillers):
#     column_names = "number_with_year entry_date " \
#         "partner user workflow_buttons *"
#     insert_layout = """
#     partner
#     entry_date
#     """
#     order_by = ["-id"]
#
# VoucherTypes.add_item_lazy(FillersByJournal, _("Provision fillers"))
