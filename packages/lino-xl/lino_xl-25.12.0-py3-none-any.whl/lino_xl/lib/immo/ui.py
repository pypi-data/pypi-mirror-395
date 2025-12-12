# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.modlib.users.mixins import My
from lino.core import constants


class EntryTypes(dd.Table):
    required_roles = dd.login_required(dd.SiteStaff)
    model = 'immo.EntryType'
    column_names = 'designation *'
    detail_layout = """id designation
    EntriesByType
    """


class Entries(dd.Table):
    model = "immo.Entry"
    column_names = 'title group pub_date *'
    default_display_modes = {
        None: constants.DISPLAY_MODE_TILES}
    detail_layout = """
    id entry_type user group
    title
    pub_date album
    # contacts.AuthorsByEntry contacts.MentorsByEntry
    # topics.TagsByOwner topics.InterestsByTopic
    body
    """
    # params_panel_pos = 'left'
    # params_layout = """
    # group
    # user
    # author
    # mentor
    # """


class EntriesByType(Entries):
    master_key = 'entry_type'


class EntriesByGroup(Entries):
    master_key = 'group'


class MyEntries(My, Entries):
    required_roles = dd.login_required(dd.SiteUser)
    # label = _("My entries")


class LatestEntries(Entries):
    required_roles = set()  # also for anonymous
    label = _("Latest entries")
    column_names = "pub_date title user *"
    order_by = ["-pub_date"]
    filter = dd.Q(pub_date__isnull=False)
    # default_display_modes = {None: constants.DISPLAY_MODE_LIST}
    # editable = False
    insert_layout = None  # disable the (+) button but permit editing
