# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.modlib.users.mixins import My
from lino.core import constants
from lino_xl.lib.contacts.roles import ContactsStaff, ContactsUser
from lino_xl.lib.sources.choicelists import AuthorRoles


class SongTypes(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'songs.SongType'
    column_names = 'designation *'
    detail_layout = """id designation
    SongsByType
    """


class SongDetail(dd.DetailLayout):
    main = "general scores more"

    general = dd.Panel("""
    title:60 language:10
    subtitle parent
    body
    """, label=_("General"))

    more = dd.Panel("""
    id user group private song_type
    publishing_state pub_date
    license copyright_owner year_published
    sources.SourcesByOwner sources.ComposersByOwner sources.AuthorsByOwner topics.TagsByOwner
    songs.SongsByParent
    """, label=_("More"))

    scores = dd.Panel("""
    scores_tempo scores_preamble scores_line_width other_font
    scores_lyrics scores_chords
    scores_soprano scores_alto scores_tenor scores_bass
    scores_errors
    """, label=_("Scores"))


class Songs(dd.Table):
    model = "songs.Song"
    column_names = 'id title language *'
    detail_layout = "songs.SongDetail"
    # params_panel_pos = 'left'
    # params_layout = """
    # group
    # user
    # author
    # mentor
    # """


class SongsByType(Songs):
    master_key = 'song_type'


class SongsByGroup(Songs):
    master_key = 'group'


class SongsByCopyrightOwner(Songs):
    master_key = 'copyright_owner'


class SongsByParent(Songs):
    label = _("Derived songs")
    master_key = 'parent'


class MySongs(My, Songs):
    required_roles = dd.login_required(ContactsUser)
    # label = _("My entries")


class LatestSongs(Songs):
    required_roles = set()  # also for anonymous
    label = _("Latest songs")
    column_names = "pub_date title user *"
    order_by = ["-pub_date"]
    filter = dd.Q(pub_date__isnull=False)
    # default_display_modes = {None: constants.DISPLAY_MODE_LIST}
    # editable = False
    insert_layout = None  # disable the (+) button but permit editing
    default_display_modes = {
        None: constants.DISPLAY_MODE_LIST}
