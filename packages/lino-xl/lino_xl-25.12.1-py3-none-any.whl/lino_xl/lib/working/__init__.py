# Copyright 2008-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Adds functionality for managing workting time.

See :doc:`/specs/working`.

"""

from lino.api import ad, _


class Plugin(ad.Plugin):

    # verbose_name = _("Clocking")
    verbose_name = _("Working time")

    needs_plugins = ['lino.modlib.summaries', 'lino.modlib.checkdata']

    # project_model = 'tickets.Project'
    # project_model = 'contacts.Partner'

    reports_master = 'trading.VatProductInvoice'
    ticket_model = 'tickets.Ticket'
    # ticket_model = 'contacts.Partner'
    default_reporting_type = 'regular'

    def post_site_startup(self, site):
        # from .mixins import Workable
        self.ticket_model = site.models.resolve(self.ticket_model)
        # if not issubclass(self.ticket_model, Workable):
        #     msg = "Your plugins.working.ticket_model ({}) is not workable"
        #     msg = msg.format(self.ticket_model)
        #     # raise Exception(msg)
        #     site.logger.warning(msg)

        if isinstance(self.default_reporting_type, str):
            x = site.models.working.ReportingTypes.get_by_name(
                self.default_reporting_type)
            self.default_reporting_type = x

    def setup_main_menu(self, site, user_type, m, ar=None):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('working.MySessions')
        # m.add_action('working.ServiceReports')
        # m.add_action('working.MySessionsByDate')
        m.add_action('working.WorkedHours')
        m.add_action('working.ActiveContracts')

    def setup_config_menu(self, site, user_type, m, ar=None):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('working.SessionTypes')
        m.add_action('working.ReportingRules')
        m.add_action('working.Contracts')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('working.Sessions')
        if site.is_installed("invoicing"):
            m.add_action('working.AllSummaries')
        m.add_action('working.UserSummaries')
        m.add_action('working.ReportingTypes')

    def get_dashboard_items(self, user):
        # if user.is_authenticated:
        yield self.site.models.working.WorkedHours
        super(Plugin, self).get_dashboard_items(user)
