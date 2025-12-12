# -*- coding: UTF-8 -*-
# Copyright 2012-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.text import format_lazy

from lino.api import dd, rt, _
from lino import mixins

from lino.core.roles import Explorer
from lino.utils import join_elems
from lino.utils.html import E
# from lino.utils.report import Report

# from lino.modlib.system.choicelists import PeriodEvents
# from lino.modlib.users.mixins import My

from lino_xl.lib.accounting.ui import ByJournal
from lino_xl.lib.accounting.choicelists import VoucherTypes
from lino_xl.lib.trading.models import InvoicesByPartner
from lino_xl.lib.trading.models import VatProductInvoice, InvoiceItem
from lino_xl.lib.trading.ui import InvoiceItems, ItemsByInvoice
# from lino_xl.lib.invoicing.mixins import InvoicingAreas
from lino_xl.lib.invoicing.roles import InvoicingUser, InvoicingStaff


class SubscriptionDetail(dd.DetailLayout):
    required_roles = dd.login_required(InvoicingUser)

    main = "general more"

    general = dd.Panel("""
    panel1 panel2 panel3
    ItemsBySubscription PeriodsBySubscription
    """,
                       label=_("General"))

    panel1 = dd.Panel("""
    partner
    ref subject
    start_date
    """)  # sales_remark

    panel2 = dd.Panel("""
    invoiceable_product
    subscription_periodicity
    end_date
    """)  # sales_remark

    panel3 = dd.Panel("""
    language
    workflow_buttons
    printed
    """)  # sales_remark

    # totals = dd.Panel("""
    # total_base
    # total_vat
    # total_incl
    # workflow_buttons
    # """)

    more = dd.Panel("""
    entry_date journal number id:8
    narration user
    trading.InvoiceItemsByGenerator #invoicing.InvoicingsByGenerator InvoicesBySubscription
    """,
                    label=_("More"))


class SubscriptionItemDetail(dd.DetailLayout):
    required_roles = dd.login_required(InvoicingUser)

    main = """
    voucher seqno
    product
    unit_price discount qty
    remark
    """


class InvoicesBySubscription(InvoicesByPartner):

    label = _("Sales invoices (to same invoice recipient)")

    @classmethod
    def cast_master_instance(cls, mi):
        # the master instance of InvoicesByPartner must be a Partner, but since
        # we use this on an order, we get the pk of an order
        if isinstance(mi, rt.models.subscriptions.Subscription):
            return mi.get_invoiceable_partner()

    # @classmethod
    # def get_master_instance(cls, ar, model, pk):
    #     # the master instance of InvoicesByPartner must be a Partner, but since
    #     # we use this on an order, we get the pk of an order
    #
    #     if not pk:
    #         return None
    #     assert model is rt.models.contacts.Partner
    #     mi = rt.models.subscriptions.Subscription.objects.get(pk=pk)
    #     return mi.get_invoiceable_partner()


class Subscriptions(dd.Table):
    # _order_area = None
    required_roles = dd.login_required(InvoicingUser)
    model = 'subscriptions.Subscription'
    detail_layout = 'subscriptions.SubscriptionDetail'
    insert_layout = """
    partner
    journal
    entry_date
    """
    column_names = "id start_date ref partner subject workflow_buttons *"
    # order_by = ['-start_date', 'partner']
    auto_fit_column_widths = True


class SubscriptionsByJournal(Subscriptions, ByJournal):
    master_key = 'journal'
    column_names = "number entry_date ref partner subject workflow_buttons *"
    insert_layout = """
    ref
    partner
    entry_date
    """


VoucherTypes.add_item_lazy(SubscriptionsByJournal)


class AllSubscriptions(Subscriptions):
    # _order_area = None
    label = _("All subscriptions")
    required_roles = dd.login_required(Explorer)
    column_names = "id journal number entry_date:8 partner *"
    order_by = ['id']


# class RefSubscriptions(Subscriptions):
#     filter = models.Q(ref__isnull=False)
#     column_names = "ref partner subject workflow_buttons *"
#     order_by = ['ref']


class SubscriptionsByPartner(Subscriptions):
    master_key = 'partner'
    column_names = "ref subject entry_date:8 journal number workflow_buttons user *"


class SubscriptionItems(dd.Table):
    model = 'subscriptions.SubscriptionItem'
    detail_layout = 'subscriptions.SubscriptionItemDetail'
    insert_layout = """
    product
    qty
    discount
    """
    required_roles = dd.login_required(InvoicingStaff)
    auto_fit_column_widths = True

    # required_roles = dd.login_required(InvoicingStaff)
    # auto_fit_column_widths = True
    #
    # insert_layout = """
    # product
    # remark
    # """
    #
    stay_in_grid = True


class ItemsBySubscription(SubscriptionItems):
    label = _("Content")
    master_key = 'voucher'
    order_by = ["seqno"]
    required_roles = dd.login_required(InvoicingUser)
    # detail_layout = None  # 'subscriptions.InvoiceItemDetail'

    column_names = "product discount unit_price qty remark *"


# InvoicingAreas.add_item('subscriptions', _("Subscriptions"), 'subscriptions',
#     voucher_model=VatProductInvoice, voucher_item=InvoiceItem,
#     max_date_offset=7, today_offset=0)


class SubscriptionPeriods(dd.Table):
    model = 'subscriptions.SubscriptionPeriod'
    required_roles = dd.login_required(InvoicingStaff)


class PeriodsBySubscription(SubscriptionPeriods):
    label = _("Subscription periods")
    master_key = 'master'
    order_by = ["start_date"]
    required_roles = dd.login_required(InvoicingUser)
    # detail_layout = None  # 'subscriptions.InvoiceItemDetail'

    column_names = "start_date end_date must_invoice invoicing_info id *"


# from lino_xl.lib.invoicing.models import InvoicingsByGenerator
#
# class InvoicingsBySubscription(InvoicingsByGenerator):
#
#     master_key = 'invoiceable__master'
#
# Exception: Invalid master_key 'invoiceable__master' for
# subscriptions.InvoicingsBySubscription (<class
# 'lino_xl.lib.trading.models.InvoiceItem'> has fields id, seqno, title,
# invoiceable_type, invoiceable_id, must_invoice, total_incl, total_base,
# total_vat, vat_class, unit_price, qty, product, description, discount,
# voucher, invoiceable, name_column, navigation_panel, workflow_buttons,
# overview, list_item, move_buttons, invoicing_info)
