# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Model mixins for this plugin.
"""

from lino.api import dd, rt, _
from lino.utils.instantiator import create_row, create_or_update_row
from lino.modlib.notify.mixins import ChangeNotifier
from .choicelists import VoteStates
from .actions import CreateVote, EditVote, VotableEditVote


class Votable(ChangeNotifier):
    """Base class for models that can be used as
    :attr:`lino_xl.lib.votes.Plugin.votable_model`.

    """

    class Meta(object):
        abstract = True

    if dd.is_installed('votes'):

        create_vote = CreateVote()
        edit_vote = VotableEditVote()

        # def get_project_for_vote(self, vote):
        #     return None

        def get_vote_raters(self):
            """Yield or return a list of the users who are allowed to rate the
            votes on this votable.

            Lino automatically (in :meth:`after_ui_save`) creates an
            **author vote** for each of them.

            """
            return []

        def get_favourite(self, user):
            """
            Return the vote of the given user about this votable, or None if no
            vote exists.

            There should be either 0 or 1 vote per user and votable.
            """
            qs = rt.models.votes.Vote.objects.filter(votable=self, user=user)
            return qs.first()

        def get_change_observers(self, ar=None):
            for x in super().get_change_observers(ar):
                yield x
            for vote in rt.models.votes.Vote.objects.filter(votable=self):
                yield (vote.user, vote.mail_mode or vote.user.mail_mode)

        def set_author_votes(self):
            """Verify that every vote rater has a vote.

            The raters of a vote are returned by :meth:`get_vote_raters`.

            """
            # wanted_votes = dict()
            # def collect(user, state):
            #     if user in wanted_votes:
            #         return
            if dd.plugins.votes.with_candidatures:
                for user in self.get_vote_raters():
                    new_values = dict(user=user,
                                      votable=self,
                                      state=VoteStates.author)
                    create_or_update_row(rt.models.votes.Vote,
                                         dict(user=user, votable=self),
                                         new_values)

        def after_ui_create(self, ar):
            """Automatically call :meth:`set_author_votes` after creation.

            """
            super().after_ui_create(ar)
            self.set_author_votes()
