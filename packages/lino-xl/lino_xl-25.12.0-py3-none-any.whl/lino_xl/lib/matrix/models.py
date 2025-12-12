# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _


class UserTrait(dd.Model):
    class Meta:
        app_label = "matrix"
        abstract = dd.is_abstract_model(__name__, "UserTrait")
        verbose_name = _("User trait")
        verbose_name_plural = _("User traits")

    user = dd.OneToOneField("users.User", related_name="matrix", null=False, blank=False)
    matrix_user_id = dd.CharField(_("Matrix user ID"), max_length=300)
    direct_room = dd.CharField(_("Matrix direct room ID"), max_length=300, blank=True)


# class UserTraits(dd.Table):
#     model = "matrix.UserTrait"
#     column_names = "matrix_user_id direct_room"
