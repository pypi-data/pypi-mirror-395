# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Add functionality for importing lecacy data from a TIM database.

See :doc:`/specs/tim2lino`.


"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Import from TIM")

    needs_plugins = ['lino_xl.lib.finan']

    languages = None
    """The language distribution used in the database to import. Mandatory
    parameter. No default value.

    """

    tim_data_path = None

    send_peppol_attr = "P"

    use_dbfread = False
    """

    Whether to use Ole Martin Bjorndalen's `dbfread
    <https://github.com/olemb/dbfread>`_ package  instead of
    :mod:`lino.utils.dbfreader` to read DBF files.

    When this is True, you must run "pip install dbfread".
    """

    use_dbf_py = False
    """
    Whether to use Ethan Furman's `dbf <http://pypi.python.org/pypi/dbf/>`_
    package instead of :mod:`lino.utils.dbfreader` to read DBF files.

    Set it to `True` when reading data from a TIM with FOXPRO DBE,
    leave it at `False` when reading DBFNTX files.

    When this is True, you must run "pip install enum34 dbf" (note
    enum34, not enum) and then you must manually patch
    :file:`site-packages/dbf/ver_2.py` to support file names ending
    with '.FOX' by replacing two lines of code::

            # if ext.lower() != '.dbf':
            if ext.lower() not in ('.dbf', '.fox'):


    """

    dbf_table_ext = '.DBF'
    # dbf_table_ext = '.FOX'
    """The file extension of TIM tables. Meaningful values are `'.DBF'` or
    `.FOX`.

    """

    timloader_module = 'lino_xl.lib.tim2lino.timloader1'
    """The module that contains the TimLoader class to be used by the tim2lino fixture.
    """

    timloader_kwargs = {}
    """The options to pass as keyword arguments when instantiating the
    TimLoader class."""

    # site_owner_id = None
    # """
    # The id (primary key) of the :term:`business partner` who represents the
    # site owner.
    # """

    ignore_journals = {}
    "A set of journal refs to *not* import"

    ignore_diffs_below = 0.02
    """
    Don't warn when a total amount differs from TIM by less then this after
    registration of an invoice.
    """

    import_finan = True

    load_listeners = []

    # siteconfig_accounts = dict(
    #     clients_account='400000',
    #     suppliers_account='440000',
    #     tax_offices_account='450000',
    #     wages_account='460000',
    #     sales_account='704000',
    #     # sales_vat_account='411000',  # vat paid 411000, 472100
    #     purchases_account='610000',
    #     # purchases_vat_account='451000',  # due vat 451000, 472200
    #     clearings_account='499000')  # 462100

    def on_plugins_loaded(self, site):
        super().on_plugins_loaded(site)
        if self.tim_data_path is None:
            self.tim_data_path = site.site_dir / 'timdata'

    def add_load_listener(self, tableName, func):
        self.load_listeners.append((tableName, func))

    # def override_voucher_type(self, row, vtt):
    #     return vtt

    # def override_product_attrs(self, attrs):
    #     return attrs

    def on_row_create(self, site, obj):
        pass

    def override_voucher_type(self, row, vtt):
        if row.idjnl.strip() in {"EKP", "EKS"}:
            return self.site.models.trading.InvoicesByJournal
        return vtt
