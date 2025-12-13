# -*- coding: UTF-8 -*-
# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models

from lino.api import dd, rt, _
from lino.core.choicelists import PointingChoice


class DoYouLike(dd.ChoiceList):
    verbose_name = _("Do you like?")


add = DoYouLike.add_item
add('0', _("certainly not"))
add('1', _("rather not"))
add('2', _("normally"), "default")
add('3', _("quite much"))
add('4', _("very much"))


class HowWell(dd.ChoiceList):

    verbose_name = _("How well?")


add = HowWell.add_item
add('0', _("not at all"))
add('1', _("a bit"))
add('2', _("moderate"), "default")
add('3', _("quite well"))
add('4', _("very well"))


class PropertyArea(PointingChoice):
    pointing_field_name = 'properties.PropGroup.property_area'
    data_view = None


class PropertyAreas(dd.ChoiceList):
    item_class = PropertyArea
    verbose_name = _("Property area")
    verbose_name_plural = _("Property areas")
    column_names = "value name text data_view *"

    @dd.virtualfield(models.CharField(_("Data table")))
    def data_view(cls, choice, ar):
        return choice.data_view


# add = PropertyAreas.add_item
# add('100', _("Properties"), 'default')
