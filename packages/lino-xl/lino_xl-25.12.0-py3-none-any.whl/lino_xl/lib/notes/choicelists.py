# -*- coding: UTF-8 -*-
# Copyright 2015-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino.core.choicelists import PointingChoice

# class MissingObject:
#     pass


class SpecialType(PointingChoice):

    pointing_field_name = 'notes.NoteType.special_type'

    # _instance = None

    def create_object(self, **kwargs):
        kwargs.update(special_type=self)
        return rt.models.notes.NoteType(**kwargs)

    # def set_object(self, obj):
    #     self._instance = obj

    # def get_object(self):
    #     if self._instance is None:
    #         NoteType = rt.models.notes.NoteType
    #         try:
    #             self._instance = NoteType.objects.get(special_type=self)
    #         except Note.DoesNotExist:
    #             self._instance = MissingObject()
    #     return self._instance

    def get_notes(self, **kw):
        return rt.models.notes.Note.objects.filter(type__special_type=self,
                                                   **kw)


class SpecialTypes(dd.ChoiceList):
    verbose_name = _("Special note type")
    verbose_name_plural = _("Special note types")
    item_class = SpecialType
    max_length = 5
