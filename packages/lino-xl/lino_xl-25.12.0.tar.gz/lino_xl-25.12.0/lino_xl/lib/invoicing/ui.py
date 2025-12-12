# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.core import constants

# from lino.modlib.users.mixins import My

from lino.api import dd, rt, _
from lino_xl.lib.accounting.roles import LedgerUser, LedgerStaff

# from .mixins import InvoicingAreas
# from .actions import ToggleSelection


class FollowUpRules(dd.Table):
    model = 'invoicing.FollowUpRule'
    required_roles = dd.login_required(LedgerStaff)
    column_names = 'seqno invoicing_task invoice_generator source_journal *'


class RulesByTask(FollowUpRules):
    master_key = "invoicing_task"
    column_names = 'seqno invoice_generator source_journal *'


class TaskDetail(dd.DetailLayout):
    main = "general_tab cal_tab"

    general_tab = dd.Panel("""
    seqno target_journal name
    user procedure
    # invoice_generators
    invoicing.RulesByTask
    """,
                           label=_("General"))

    cal_tab = dd.Panel("""
    max_events every_unit every positions
    max_date_offset today_offset
    monday tuesday wednesday thursday friday saturday sunday
    log_level disabled status
    message
    """,
                       label=_("Calendar"))


class Tasks(dd.Table):
    model = 'invoicing.Task'
    required_roles = dd.login_required(LedgerStaff)
    column_names = 'seqno name disabled weekdays_text status *'
    detail_layout = 'invoicing.TaskDetail'
    insert_layout = """
    procedure
    target_journal
    """


class Tariffs(dd.Table):
    required_roles = dd.login_required(LedgerStaff)
    model = "invoicing.Tariff"
    column_names = "designation number_of_events min_asset max_asset product *"
    order_by = ['designation']


class Plans(dd.Table):
    required_roles = dd.login_required(LedgerUser)
    model = "invoicing.Plan"
    detail_layout = """
    user invoicing_task #provision_product
    partner order today min_date max_date
    invoicing.ItemsByPlan
    """


class MyPlan(Plans):
    label = _("My invoicing plan")
    # label = _("Make invoices")
    help_text = _(
        "Open your invoicing plan in order to generate invoices or service reports.")
    required_roles = dd.login_required(LedgerUser)
    default_record_id = 'row'

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        u = ar.get_user()
        if u.is_anonymous:
            raise Warning(_("You are not signed in"))
        # dd.logger.warning("Get plan for %s", u)
        return cls.model.create_user_plan(u)
        # import traceback
        # try:
        #     return rt.models.invoicing.Plan.create_user_plan(u)
        # except Exception as e:
        #     traceback.print_exc(e)


# class PlansByArea(Plans):
#     master_key = 'invoicing_task'
#     # detail_layout = """user source_journal partner
#     # order today min_date max_date
#     # invoicing.ItemsByPlan
#     # """
#     start_invoicing = StartInvoicingByTask()
#
#     # @classmethod
#     # def get_master_instance(self, ar, model, pk):
#     #     if not pk:
#     #         return None
#     #     return InvoicingAreas.get_by_value(pk)


class AllPlans(Plans):
    required_roles = dd.login_required(LedgerStaff)


class Items(dd.Table):
    required_roles = dd.login_required(LedgerUser)
    model = "invoicing.Item"


class ItemsByPlan(Items):
    verbose_name_plural = _("Suggestions")
    master_key = 'plan'
    row_height = 2
    column_names = "selected partner preview number amount invoice_button *"
    default_display_modes = {None: constants.DISPLAY_MODE_GRID}
    allow_create = False


class InvoicingsByGenerator(dd.Table):
    abstract = True
    required_roles = dd.login_required(LedgerUser)
    # model = dd.plugins.invoicing.item_model
    # model = 'accounting.Voucher'
    # model = Invoiceable
    label = _("Invoicings")
    master_key = 'invoiceable'
    editable = False
