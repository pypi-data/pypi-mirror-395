# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# See :doc:`/plugins/agenda`.

from lino.api import ad, _


class Plugin(ad.Plugin):

    verbose_name = _("Agenda")
    meeting_model = 'cal.Event'
    topic_model = 'tickets.Ticket'
    needs_plugins = ['lino_xl.lib.checkdata']
    menu_group = "cal"

    def pre_site_startup(self, site):
        super().pre_site_startup(site)
        if self.meeting_model is not None:
            self.meeting_model = site.models.resolve(self.meeting_model)
        if self.topic_model is not None:
            self.topic_model = site.models.resolve(self.topic_model)

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        # mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('agenda.Items')
