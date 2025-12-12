# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""See :doc:`/specs/countries`.

.. autosummary::
   :toctree:

    utils
    fixtures

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "The countries plugin."

    verbose_name = _("Places")
    needs_plugins = ['lino.modlib.office', 'lino_xl.lib.xl']

    allow_duplicate_cities = False
    hide_region = False
    region_label = _("County")
    country_code = 'BE'
    municipality_type = '50'
    full_data = False

    def before_analyze(self):
        super().before_analyze()
        from lino_xl.lib.countries.mixins import AddressLocation
        from lino.core.utils import models_by_base
        if self.hide_region:
            for m in models_by_base(AddressLocation):
                m.hide_elements('region')

    def pre_site_startup(self, site):
        if self.country_code is None:
            raise Exception(
                "countries plugin requires a nonempty `country_code` setting.")

    def setup_config_menu(self, site, user_type, m, ar=None):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('countries.Countries')
        m.add_action('countries.Places')

    def get_my_country(self):
        """Return the :class:`Country` instance configured by
:attr:`country_code`."""
        Country = self.site.models.countries.Country
        try:
            return Country.objects.get(pk=self.country_code)
        except Country.DoesNotExist:
            return
