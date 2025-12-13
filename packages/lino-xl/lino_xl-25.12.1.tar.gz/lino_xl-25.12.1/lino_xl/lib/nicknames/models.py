# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models

from lino.utils.html import E
from lino.utils import join_elems
from lino.modlib.users.mixins import UserAuthored
from lino.api import dd, rt, _

named_model = dd.get_plugin_setting('nicknames', 'named_model', None)

if named_model is not None:

    class Naming(UserAuthored):

        class Meta:
            app_label = 'nicknames'
            abstract = dd.is_abstract_model(__name__, 'Naming')
            verbose_name = _("Nicknaming")
            verbose_name_plural = _("Nicknamings")
            unique_together = ["user", "nickname"]

        allow_cascaded_delete = 'user named'

        named = dd.ForeignKey(named_model, related_name="namings")
        nickname = models.CharField(_("Nickname"),
                                    max_length=200,
                                    blank=False,
                                    null=False)

    class Namings(dd.Table):
        model = Naming


def welcome_messages(ar):
    Naming = rt.models.nicknames.Naming
    named_model = dd.plugins.nicknames.named_model
    if named_model is None:
        return
    qs = Naming.objects.filter(user=ar.get_user())
    qs = qs.order_by('nickname')
    if qs.count() > 0:
        chunks = [
            str(
                _("Your nicknamed {0} are ").format(
                    named_model._meta.verbose_name_plural))
        ]
        chunks += join_elems(
            [ar.obj2html(obj.named, obj.nickname) for obj in qs], sep=", ")
        chunks.append('.')
        yield E.span(*chunks)


dd.add_welcome_handler(welcome_messages)
