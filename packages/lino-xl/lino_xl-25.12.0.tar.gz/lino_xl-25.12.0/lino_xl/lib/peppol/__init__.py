# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/peppol.html


from lino.api import ad, _
from lino.utils import i2d
from .utils import Session


class Plugin(ad.Plugin):

    # verbose_name = _("Ibanity")
    verbose_name = _("Peppol")
    needs_plugins = ['lino_xl.lib.vat']
    # menu_group = "contacts"

    cert_file = None
    key_file = None
    credentials = None

    # use_sandbox = True
    with_suppliers = False
    # with_documents = False
    supplier_id = None
    outbound_model = "trading.VatProductInvoice"
    onboarding_date = None
    inbound_model = "vat.VatAccountInvoice"
    inbound_journal = "INB"
    simulate_endpoints = False
    is_sandbox = False

    def pre_site_startup(self, site):
        if isinstance(self.onboarding_date, (str, int)):
            self.onboarding_date = i2d(self.onboarding_date)
        super().pre_site_startup(site)
        cd = site.site_dir / "secrets"
        cred_file = cd / "credentials.txt"
        if cred_file.exists():
            self.cert_file = cd / "certificate.pem"
            self.key_file = cd / "decrypted_private_key.pem"
            self.credentials = cred_file.read_text().strip()
            if self.credentials.endswith(":valid_client_secret"):
                self.is_sandbox = True
        if self.outbound_model is not None:
            self.outbound_model = site.models.resolve(self.outbound_model)
        if self.inbound_model is not None:
            self.inbound_model = site.models.resolve(self.inbound_model)
        self.inbox_dir = site.media_root / "ibanity_inbox"

    # def post_site_startup(self, site):
    #     super().post_site_startup(site)

    def get_ibanity_session(self, ar):
        if not self.credentials:
            return
        return Session(ar, self.cert_file, self.key_file, self.credentials)

    def setup_main_menu(self, site, user_type, m, ar=None):
        if self.with_suppliers:
            # mg = self.get_menu_group()
            mg = site.plugins.contacts
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m.add_action('peppol.Suppliers')
        if self.supplier_id:
            mg = site.plugins.accounting
            m = m.add_menu(mg.app_label, mg.verbose_name)
            m = m.add_menu(self.app_label, self.verbose_name)
            # mg = self.get_menu_group()
            m.add_action('peppol.Inbox')
            m.add_action('peppol.Archive')
            m.add_action('peppol.Outbox')
            # m.add_action('peppol.Sent')

    # def setup_explorer_menu(self, site, user_type, m, ar=None):
    #     if self.with_suppliers:
    #         # mg = self.get_menu_group()
    #         mg = site.plugins.contacts
    #         m = m.add_menu(mg.app_label, mg.verbose_name)
    #         m.add_action('peppol.OnboardingStates')

    def get_quicklinks(self):
        if self.supplier_id:
            yield "peppol.Inbox"
            yield "peppol.Outbox"
            yield "peppol.SyncPeppol"
