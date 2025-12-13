# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from lino.api import dd, rt, _
from lino.utils import Cycler


def objects():

    polls = rt.models.polls

    USERS = Cycler(settings.SITE.user_model.objects.all())

    pf = None

    for p in polls.Poll.objects.exclude(questions_to_add=''):
        if p.title == "Participant feedback":
            pf = p
        p.after_ui_save(None, None)
        yield polls.Response(poll=p,
                             user=USERS.pop(),
                             date=dd.today(),
                             state=polls.ResponseStates.draft)


    if pf is not None:
        cs = polls.ChoiceSet(
            choice_type=rt.models.gfks.ContentType.objects.get_for_model(rt.models.users.User),
            **dd.str2kw("name", _("Person")))
        yield cs

        yield polls.Question(poll=pf, title="Who should become president?", choiceset=cs, number="5")
