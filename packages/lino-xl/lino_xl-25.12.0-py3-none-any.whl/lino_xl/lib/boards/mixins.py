# Copyright 2008-2015 Rumma & Ko Ltd
#
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Model mixins for `lino.modlib.boards`.

"""

from lino import logger

from lino.api import dd, rt, _
from django.db import models

from lino.modlib.users.mixins import UserAuthored


class BoardDecision(UserAuthored):
    """Mixin for models that represent a board decision.  Base class for
    :class:`lino_welfare.modlib.aids.mixins.Confirmation`.

    """

    class Meta:
        abstract = True

    decision_date = models.DateField(verbose_name=_('Decided'),
                                     blank=True,
                                     null=True)
    board = dd.ForeignKey('boards.Board', blank=True, null=True)

    @dd.chooser()
    def board_choices(self, decision_date):
        qs = rt.models.boards.Board.objects.all()
        if decision_date:
            qs = dd.PeriodEvents.active.add_filter(qs, decision_date)
        return qs
