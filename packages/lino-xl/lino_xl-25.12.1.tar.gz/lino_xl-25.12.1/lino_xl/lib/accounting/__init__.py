# -*- coding: UTF-8 -*-
# Copyright 2014-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""This is Lino's standard plugin for General Ledger.
See :doc:`/plugins/accounting`.

.. autosummary::
    :toctree:

    fields
    management.commands.reregister

"""

from django.utils.functional import lazystr

from lino.api import ad, _

# UPLOADTYPE_SOURCE_DOCUMENT = 1
# """Primary key of upload type "source document" created in :fixture:`std` fixture."""


class Plugin(ad.Plugin):

    verbose_name = _("Accounting")
    needs_plugins = [
        'lino.modlib.periods',
        'lino.modlib.weasyprint', 'lino_xl.lib.xl', 'lino.modlib.uploads'
    ]

    ref_length = 4  # 20

    currency_symbol = "€"
    use_pcmn = False
    project_model = None
    payer_model = None
    menu_group = "accounting"

    # intrusive_menu = False
    # """
    # Whether the plugin should integrate into the application's
    # main menu in an intrusive way.  Intrusive means that the main
    # menu gets one top-level item per journal group.
    #
    # The default behaviour is `False`, meaning that these items are
    # gathered below a single item "Accounting".
    # """
    #
    suppress_movements_until = None

    # Available sales methods:
    SALES_METHODS = {
        'direct': "just invoices",
        'delivery': "delivery notes and invoices",
        'pos': "point of sales",
    }

    sales_method = 'direct'
    has_payment_methods = False
    has_purchases = False
    xml_media_dir = "xml"

    # sales_stories_journal = "SLS"

    # purchase_stories = True
    # """Whether demo fixture should generate purchase invoices."""

    # registered_states = "registered signed"
    # """The voucher states to be considered as registered.
    #
    # This is specified as a string with a space-separated list of state names,
    # and during startup it is resolved into a tuple of instances of
    # VoucherState.
    #
    # """

    def pre_site_startup(self, site):
        # if isinstance(self.registered_states, str):
        #     s = {
        #         site.models.accounting.VoucherStates.get_by_name(i)
        #             for i in self.registered_states.split()}
        #     self.registered_states = tuple(s)
        if self.sales_method is not None:
            if self.sales_method not in self.SALES_METHODS:
                raise Exception(
                    "Invalid value {} for accounting.sales_method!".format(
                        self.sales_method))
            if self.sales_method == 'pos' and not self.has_payment_methods:
                raise Exception(
                    "When sales_method is 'pos', has_payment_methods must be True."
                )
        super().pre_site_startup(site)

    def post_site_startup(self, site):
        super().post_site_startup(site)
        site.models.accounting.CommonAccounts.sort()
        site.models.accounting.VoucherTypes.sort()
        if self.payer_model is not None:
            self.payer_model = site.models.resolve(self.payer_model)
        if self.project_model is not None:
            self.project_model = site.models.resolve(self.project_model)

    def before_analyze(self):
        super().before_analyze()
        self.site.models.uploads.Shortcuts.add_item(
            'accounting.Voucher',
            'source_document',
            _("Source document"))

    def setup_main_menu(self, site, user_type, m, ar=None):
        """
        Add a menu item for every journal.

        Menu items are grouped by journal group. See :class:`lino_xl.lib.accounting.JournalGroups`

        """
        Journal = site.models.accounting.Journal
        JournalGroups = site.models.accounting.JournalGroups
        # lp = site.plugins.accounting
        lp = self.get_menu_group()
        filter = {}
        if ar is not None and not (user := ar.get_user()).is_anonymous and site.is_installed('ledgers'):
            filter.update(ledger=user.ledger)
        for grp in JournalGroups.get_list_items():
            mg = grp.menu_group
            if mg is None:
                lm = m.add_menu(lp.app_label, lp.verbose_name)
                subm = lm.add_menu(grp.name, grp.text)
            else:
                subm = m.add_menu(mg.app_label, mg.verbose_name)
            for jnl in Journal.objects.filter(
                    journal_group=grp, **filter).order_by('seqno'):
                subm.add_action(jnl.voucher_type.table_class,
                                label=lazystr(jnl),
                                params=dict(master_instance=jnl))
        lm = m.add_menu(lp.app_label, lp.verbose_name)
        lm.add_action('accounting.MyMovements')

    def setup_reports_menu(self, site, user_type, m, ar=None):
        if site.is_installed("finan"):
            # mg = site.plugins.accounting
            mg = self.get_menu_group()
            m = m.add_menu(mg.app_label, mg.verbose_name)
            # m.add_action('accounting.Situation')
            # m.add_action('accounting.ActivityReport')
            # m.add_action('accounting.AccountingReport')
            # m.add_action('accounting.GeneralAccountBalances')
            # m.add_action('accounting.CustomerAccountBalances')
            # m.add_action('accounting.SupplierAccountBalances')
            m.add_action('accounting.Debtors')
            m.add_action('accounting.Creditors')

    def setup_config_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        # mg = site.plugins.accounting
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('accounting.Accounts')
        m.add_action('accounting.Journals')
        m.add_action('accounting.PaymentTerms')
        if self.has_payment_methods:
            m.add_action('accounting.PaymentMethods')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        # mg = site.plugins.accounting
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('accounting.CommonAccounts')
        m.add_action('accounting.MatchRules')
        m.add_action('accounting.AllVouchers')
        m.add_action('accounting.VoucherTypes')
        m.add_action('accounting.AllMovements')
        m.add_action('accounting.TradeTypes')
        m.add_action('accounting.JournalGroups')

    def remove_dummy(self, *args):
        lst = list(args)
        if self.project_model is None:
            lst.remove('project')
        return lst

    def get_dashboard_items(self, user):
        yield self.site.models.accounting.MyMovements
        yield self.site.models.accounting.JournalsOverview
