# -*- coding: UTF-8 -*-
# Copyright 2012-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Read Belgian eID cards and store that data in the database.

See :doc:`/specs/beid`.

"""

# When this plugin is installed, you can still easily disable it by
# setting :attr:`use_java <lino.core.site.Site.use_java>` to `False`
# in your :xfile:`settings.py`.

# When this plugin is activated, then you must also add the `.jar` files
# required by :ref:`eidreader` into your media directory, in a
# subdirectory named "eidreader".  TODO: move :ref:`eidreader` to a
# `static` directory in the Lino repository.

# An (untested) alternative implementation of the same functionality is
# :mod:`lino_xl.lib.eid_jslib.beid` which overrides this plugin and does
# the same except that it uses `eidjslib` instead of :ref:`eidreader`.

from os.path import join
from lino.api import ad, _
from lino.utils import Cycler


class Plugin(ad.Plugin):  # was: use_eidreader

    site_js_snippets = ['beid/eidreader.js']
    media_name = 'eidreader'
    data_collector_dir = None
    data_cache_dir = None
    eidreader_timeout = 15
    read_only_simulate = False

    simulate_eidreader_path = None

    urlhandler_prefix = 'beid://'

    preprocessor_delay = 0

    def pre_site_startup(self, kernel):

        from lino_xl.lib.beid.mixins import BeIdCardHolder
        from lino.core.utils import models_by_base

        super().pre_site_startup(kernel)

        if self.data_cache_dir is None:
            self.data_cache_dir = self.site.site_dir / 'media' / 'cache' / 'beid'
            # self.data_cache_dir = join(
            #     self.site.site_dir, 'media', 'beidtmp')
        self.site.makedirs_if_missing(self.data_cache_dir)

        cmc = list(models_by_base(BeIdCardHolder, toplevel_only=True))
        if len(cmc) > 1:
            msg = "There must be exactly one BeIdCardHolder model " \
                  "in your Site! You have {}. ".format(cmc)
            raise Exception(msg)
        if len(cmc) == 0:
            self.site.logger.warning(
                "You have lino_xl.lib.beid installed, "
                "but there is no implementation of BeIdCardHolder.")
            return
        self.holder_model = cmc[0]
        if self.urlhandler_prefix is not None:
            if not self.urlhandler_prefix.endswith("://"):
                msg = "Invalid urlhandler_prefix {} (must end with '://')"
                raise Exception(msg.format(self.urlhandler_prefix))

        if self.simulate_eidreader_path is not None:
            self.SIMULATION_FILES = Cycler(
                self.simulate_eidreader_path.iterdir())

        return

    def get_patterns(self):
        # from django.conf.urls import url
        from django.urls import re_path as url
        from . import views
        urls = [url('^eid/(?P<uuid>.+)', views.EidStore.as_view())]
        return urls
