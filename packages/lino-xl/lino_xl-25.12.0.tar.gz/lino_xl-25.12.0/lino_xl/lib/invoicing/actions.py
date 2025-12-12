# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.utils.text import format_lazy
from django.conf import settings

from lino.api import dd, rt, _
from lino.modlib.users.mixins import StartPlan


class StartInvoicing(StartPlan):
    # label = _("Generate invoices")
    icon_name = 'basket'
    show_in_toolbar = False
    select_rows = True

    def __init__(self, invoicing_task):
        self.invoicing_task = invoicing_task
        super().__init__()

    def get_button_label(self, actor):
    # def get_label(self):
        # return str(self.invoicing_task)
        it = self.invoicing_task
        name = settings.SITE.babelattr(it.target_journal, 'name')
        return format_lazy(_("Make {}"), name)

    def get_plan_model(self, ar):
        return rt.models.invoicing.Plan

    def get_plan_options(self, ar):
        return dict(invoicing_task=self.invoicing_task, partner=None)


class StartInvoicingForPartner(StartInvoicing):
    show_in_toolbar = True
    select_rows = True
    update_after_start = True

    def __init__(self, invoicing_task):
        super().__init__(invoicing_task)
        self.help_text = format_lazy(
            _("Make {} for this partner."),
            invoicing_task.target_journal)

    def get_plan_options(self, ar):
        partner = ar.selected_rows[0]
        assert isinstance(partner, rt.models.contacts.Partner)
        return dict(partner=partner, invoicing_task=self.invoicing_task)


class StartInvoicingForOrder(StartInvoicing):
    show_in_toolbar = True
    select_rows = True
    update_after_start = True

    def __init__(self, invoicing_task):
        super().__init__(invoicing_task)
        self.help_text = format_lazy(
            _("Make {} for this {}."),
            invoicing_task.target_journal,
            dd.plugins.invoicing.order_model._meta.verbose_name)

    def get_plan_options(self, ar):
        order = ar.selected_rows[0]
        assert isinstance(order, dd.plugins.invoicing.order_model)
        return dict(order=order,
                    partner=None,
                    invoicing_task=self.invoicing_task)
        # return dict(order=order, partner=None, invoicing_area=InvoicingAreas.default)
        # return dict(order=order, partner=None)
        # return dict(order=order, partner=None, invoicing_area=order.get_invoicing_area())
        # return dict(order=order, partner=None, area=order.journal.room.invoicing_area)


class ExecutePlan(dd.Action):
    label = _("Execute plan")
    icon_name = 'money'
    sort_index = 54

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        for item in plan.items.filter(selected=True, invoice__isnull=True):
            item.create_invoice(ar)
        ar.success(refresh=True)


class ExecuteItem(ExecutePlan):
    label = _("Execute item")
    show_in_workflow = True
    show_in_toolbar = False

    def get_action_permission(self, ar, obj, state):
        if obj.invoice_id:
            return False
        return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        for item in ar.selected_rows:
            if item.invoice_id:
                raise Warning(
                    _("Invoice {} was already generated").format(item.invoice))
            item.create_invoice(ar)
        ar.success(refresh=True)


class ToggleSelection(dd.Action):
    label = _("Toggle selections")

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        for item in plan.items.all():
            item.selected = not item.selected
            item.save()
        ar.success(refresh=True)
