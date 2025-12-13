# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds functionality for **invoicing**, i.e. automatically generating
invoices from invoice generators.

See :doc:`/plugins/invoicing`.

"""

from lino.api.ad import Plugin, _


class Plugin(Plugin):

    verbose_name = _("Invoicing")

    # needs_plugins = ['lino_xl.lib.accounting']
    needs_plugins = ['lino_xl.lib.trading']

    order_model = None

    # default_voucher_view = 'lino_xl.lib.trading.ui.InvoicesByJournal'
    # voucher_type = 'trading.InvoicesByJournal'
    # voucher_model = 'trading.VatProductInvoice'
    # item_model = 'trading.InvoiceItem'

    invoiceable_label = _("Invoiced object")
    short_invoiceable_label = _("InvObj")
    # default_invoiceable_type = None

    # three_demo_areas = True
    # """
    # Whether the :fixture:`demo` fixture should generate three invoicing areas
    # instead of one.
    # """

    # delivery_notes_demo = False
    # """
    # Whether the :fixture:`demo` fixtures should generate delivery notes.
    # """

    use_default_record_id = True
    # temporary setting; will probably become the only choice

    # def before_analyze(self):
    def pre_site_startup(self, site):
        # print("20210722 before_analyze()")
        from lino.core.utils import resolve_model
        # self.voucher_model = resolve_model(self.voucher_model)
        # self.item_model = resolve_model(self.item_model)
        # ivm = self.item_model._meta.get_field('voucher').remote_field.model
        # if self.voucher_model != ivm:
        #     raise Exception("voucher_model is {} but should be {}".format(
        #         self.voucher_model, ivm))
        # assert issubclass(self.default_voucher_view, dbtables.Table)

        if self.order_model is not None:
            self.order_model = resolve_model(self.order_model)

    def post_site_startup(self, site):
        super().post_site_startup(site)
        from lino.core.utils import models_by_base, resolve_model
        from lino_xl.lib.invoicing.mixins import InvoiceGenerator
        #     from lino_xl.lib.invoicing.mixins import InvoicingAreas
        #     for ia in InvoicingAreas.get_list_items():
        #         ia.voucher_model = resolve_model(ia.voucher_model)
        #         ia.item_model = resolve_model(ia.item_model)
        for m in models_by_base(InvoiceGenerator):
            k = m.target_voucher_model
            if isinstance(k, str):
                # k = InvoicingAreas.get_by_name(k)
                # if k is None:
                #     raise Warning(
                #         "Invalid value '{}' for {}.target_invoicing_area".format(
                #             m.target_invoicing_area, m))
                m.target_voucher_model = resolve_model(k, strict=True)

    #             # print("20230515", m, m.target_invoicing_area)
    #             # for k in m.target_invoicing_area:
    #             #     if not site.models.invoicing.InvoicingAreas.get_by_value(k):
    #             #         raise Warning(
    #             #             "Invalid name '{}' in {}.target_invoicing_area".format(
    #             #                 k, m))

    #     for jnl in ia.get_source_journals():
    #         if not issubclass(jnl.voucher_type.model, self.voucher_model):
    #             raise Warning("20221223 {} is not a {}".format(jnl.voucher_type.model, self.voucher_model))

    # def on_ui_init(self, kernel):
    #     if type(self.voucher_type) == str:
    #         VoucherTypes = self.site.models.accounting.VoucherTypes
    #         self.voucher_type = VoucherTypes.get_by_value(self.voucher_type)
    #     assert self.voucher_type.model is self.voucher_model
    #     assert self.voucher_type.model.get_items_model() is self.item_model

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = site.plugins.trading
        m = m.add_menu(mg.app_label, mg.verbose_name)
        # m.add_action('invoicing.Plan', action='start_plan')

        if self.use_default_record_id:
            # This would make things easier (no need to define an action per
            # task on Plan, no need to access database during
            # install_start_actions(), ...), but (1) it doesn't yet work under
            # react (#5552) and (2) it is less intuitive for the end user when
            # there are multiple invoicing tasks.
            m.add_action('invoicing.MyPlan')
        else:
            for it in site.models.invoicing.Task.objects.filter(disabled=False):
                # if next(ia.get_target_journals(), None) == None:
                #     # print("20230514 no target journals for", ia)
                #     continue
                # m.add_action(obj, action='start_invoicing')
                if True:
                    ba = site.models.system.SiteConfigs.get_action_by_name(
                        it.get_action_name())
                    m.add_instance_action(site.site_config, action=ba)
                else:
                    m.add_action(
                        'invoicing.PlansByArea',
                        'start_invoicing',
                        # label=format_lazy(_("Create invoices {}"), obj),
                        label=format_lazy(_("Make {}"),
                                          site.babelattr(it.target_journal, 'name')),
                        params=dict(master_instance=it))

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = site.plugins.trading
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('invoicing.Tariffs')
        m.add_action('invoicing.FollowUpRules')
        m.add_action('invoicing.Tasks')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = site.plugins.trading
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('invoicing.AllPlans')
        # m.add_action('invoicing.InvoicingAreas')
