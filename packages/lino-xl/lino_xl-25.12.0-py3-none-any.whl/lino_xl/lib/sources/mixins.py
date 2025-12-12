# -*- coding: UTF-8 -*-
# Copyright 2024-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from lino.api import dd, rt, _


class Copyrighted(dd.Model):

    class Meta:
        abstract = True

    copyright_owner = dd.ForeignKey("contacts.Company", verbose_name=_(
        "Copyright owner"), blank=True, null=True)
    year_published = models.CharField(_("Year published"), max_length=20, blank=True)
    license = dd.ForeignKey("sources.License", blank=True, null=True)
