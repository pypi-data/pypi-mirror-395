# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Adds functionality for managing contacts.

See :doc:`/plugins/contacts`.

.. autosummary::
   :toctree:

    utils
    dummy


"""
import typing

from lino.api import ad, _
from django.utils.html import format_html, mark_safe


class Plugin(ad.Plugin):
    verbose_name = _("Contacts")
    needs_plugins = ['lino_xl.lib.countries', 'lino.modlib.system']

    region_label = _('Region')
    """The verbose name of the :attr:`Partner.region` field."""

    use_vcard_export = False
    """Whether Lino should provide a button for exporting contact
    data as a vcf file.

    This feature is not used and not tested.

    If this is `True`, Lino will install `vobject
    <http://eventable.github.io/vobject/>`__ into your Python environment.
    """

    with_roles_history = False
    """Whether we maintain a history of contact persons.

    Setting this to True will define two additional fields
    :attr:`Role.start_date` and :attr:`Role.end_date`.

    """

    show_birthdays = True
    """Whether to show birthdays in the dashboard as welcome messages.

    """

    demo_region = None
    """
    Distribution of demo names to use. Available dists are BE and EE and UY.
    """

    with_partner_ref = False
    """
    Whether to use the field `Partner.partner_ref`.
    """

    site_owner_lookup: None | dict[str, typing.Any] = None
    site_owner_id = 1
    """
    The id (primary key) of the :term:`business partner` who represents the
    site owner.
    """

    _site_owner = None

    def on_plugins_loaded(self, site):
        if self.site_owner_lookup is None:
            # if site.is_installed('vat'):
            #     self.site_owner_lookup = dict(vat_id="EE100588749")
            # else:
            #     self.site_owner_lookup = dict(id=1)
            self.site_owner_lookup = dict(id=self.site_owner_id)
        super().on_plugins_loaded(site)

    @property
    def site_owner(self):
        if self._site_owner is None:
            # print(f"20250615 Lookup {self.site_owner_lookup}")
            qs = self.site.models.contacts.Company.objects.filter(
                **self.site_owner_lookup)
            self._site_owner = qs.first()  # might return None
            # print(f"20250615 Lookup returned {self._site_owner}")
        return self._site_owner

    def get_requirements(self, site):
        if site.plugins.contacts.use_vcard_export:
            yield 'vobject'

    # def post_site_startup(self, site):
    #     if not site.is_installed('memo'):
    #         return
    #     rdm = site.plugins.memo.parser.register_django_model
    #     rdm('person', site.models.contacts.Person)
    #     rdm('company', site.models.contacts.Company)

    def setup_main_menu(self, site, user_type, m, ar=None):
        m = m.add_menu(self.app_label, self.verbose_name)
        # We use the string representations and not the classes because
        # other installed applications may want to override these tables.
        for a in ('contacts.Persons', 'contacts.Companies'):
            m.add_action(a)

    def setup_config_menu(self, site, user_type, m, ar=None):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('contacts.CompanyTypes')
        m.add_action('contacts.RoleTypes')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('contacts.Roles')
        m.add_action('contacts.Partners')

    def get_site_info(self, ar=None):

        if (obj := self.site_owner) is None:
            return ""

        # text = mark_safe(obj.get_address_html())
        text = obj.get_address(", ")

        if ar is not None:
            text = ar.obj2htmls(obj, text)

        return format_html("<p>{}: {}</p>", _("Site owner"), text)


# @dd.when_prepared('contacts.Person', 'contacts.Company')
# def hide_region(model):
#     model.hide_elements('region')
