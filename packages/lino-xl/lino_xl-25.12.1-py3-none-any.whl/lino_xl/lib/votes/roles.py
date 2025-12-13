# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""User roles for this plugin. """

from lino.core.roles import UserRole


class SimpleVotesUser(UserRole):
    """Access to basic votes functionality.

    """


class VotesUser(SimpleVotesUser):
    """Access to full votes functionality.

    """


class VotesStaff(VotesUser):
    """Configure votes functionality.

    """
