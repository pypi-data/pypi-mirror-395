# -*- coding: UTF-8 -*-
# Copyright 2013-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models

from lino.api import dd, rt, _


class NicknameField(dd.VirtualField):
    """

    An editable virtual field to get and set my nickname for this database row.

    The nickname itself is stored in the Naming model.

    """

    editable = True
    empty_values = set([None])

    def __init__(self, *args, **kwargs):
        kwargs.update(blank=True)
        dd.VirtualField.__init__(
            self, models.CharField(max_length=200, *args, **kwargs), None)

    def set_value_in_object(self, ar, obj, value):
        if ar is None:
            raise Exception("20201215")
            # dd.logger.info("20201215 oops")
            # return
        Naming = rt.models.nicknames.Naming
        user = ar.get_user()
        if value:
            obj, c = Naming.objects.get_or_create(user=user, named=obj)
            obj.nickname = value
            obj.full_clean()
            obj.save()
        else:
            Naming.objects.filter(user=user, named=obj).delete()

    def value_from_object(self, obj, ar=None):
        return obj.get_my_nickname(ar)


class Nicknameable(dd.Model):

    class Meta:
        app_label = 'nicknames'
        abstract = True

    my_nickname = NicknameField(_("My nickname"))

    def get_my_nickname(self, ar):
        # print("20240114 get_my_nickname")
        if ar is None:
            return
        Naming = rt.models.nicknames.Naming
        u = ar.get_user()
        if u.is_anonymous:
            return
        obj = Naming.objects.filter(user=u, named=self).first()
        if obj:
            return obj.nickname
