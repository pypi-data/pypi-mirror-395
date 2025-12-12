# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from lino.api import dd, _


class AuthorRole(dd.Choice):
    text_plural = None

    def __init__(self, value, text, text_plural, name):
        super().__init__(value, text, name)
        self.text_plural = text_plural


class AuthorRoles(dd.ChoiceList):
    item_class = AuthorRole
    verbose_name = _("Author role")
    verbose_name_plural = _("Author roles")
    column_names = "value name text text_plural *"

    @dd.virtualfield(models.CharField(_("Plural text")))
    def text_plural(cls, choice, ar):
        return choice.text_plural


add = AuthorRoles.add_item
add('100', _("Text author"), _("Text authors"), 'author')
add('200', _("Composer"), _("Composers"), 'composer')
add('210', _("Arranger"), _("Arrangers"), 'arranger')
add('300', _("Translator"), _("Translators"), 'translator')
add('400', _("Performer"), _("Performers"), 'performer')
