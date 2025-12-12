# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""User roles for `lino_xl.lib.tickets`.

"""

from lino.core.roles import UserRole


class TicketsReader(UserRole):
    pass

class Reporter(TicketsReader):
    """
    Can create new tickets and edit their own tickets.
    """

class Searcher(TicketsReader):
    """
    Can see all tickets.
    """


class Triager(TicketsReader):
    """
    Can modify administrative ticket data like assigned worker, site,
    ticket type....
    """


class TicketsStaff(TicketsReader):
    """
    Can configure tickets functionality.
    """
