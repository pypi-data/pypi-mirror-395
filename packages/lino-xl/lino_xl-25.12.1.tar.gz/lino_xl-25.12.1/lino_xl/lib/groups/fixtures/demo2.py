# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino.utils import Cycler
from lino.utils.instantiator import create_row


def objects():
    Group = rt.models.groups.Group
    User = rt.models.users.User
    Membership = rt.models.groups.Membership
    if dd.is_installed('comments'):
        Comment = rt.models.comments.Comment

    USERS = Cycler(User.objects.all())

    # for grp in Group.objects.exclude(ref=dd.plugins.groups.default_group_ref):
    for grp in Group.objects.all():
        for i in range(2):
            u = USERS.pop()
            mbr = create_row(Membership, group=grp, user=u)
            yield mbr
            if dd.is_installed('comments'):
                txt = _("Hi all, my name is {} and I am new here.").format(u)
                yield Comment(owner=grp, user=u, body=txt, group=grp)
