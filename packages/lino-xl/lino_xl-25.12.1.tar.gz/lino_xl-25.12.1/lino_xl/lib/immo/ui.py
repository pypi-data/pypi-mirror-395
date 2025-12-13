# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.modlib.users.mixins import My
from lino.core import constants
from lino_xl.lib.albums.models import ItemsByAlbum


class EntryTypes(dd.Table):
    required_roles = dd.login_required(dd.SiteStaff)
    model = 'immo.EntryType'
    column_names = 'designation *'
    detail_layout = """id designation
    EntriesByType
    """


class EntryDetail(dd.DetailLayout):
    main = "general addr data desc price more"

    general = dd.Panel("""
    deed_type
    entry_type
    availability_text
    availability_date
    """, label=_("General"))

    addr = dd.Panel("""
    address_text
    region city
    street street_no
    """, label=_("Address"))

    desc = dd.Panel("""
    title
    body
    album
    AlbumItemsByEntry
    """, label=_("Description"))

    data = dd.Panel("""
    bedrooms bathrooms
    livable_space land
    """, label=_("Data"))

    price = dd.Panel("""
    sale_price
    rent_price
    """, label=_("Price"))

    more = dd.Panel("""
    pub_date id
    user group
    """, label=_("More"))


# class EntryDetail(dd.DetailLayout):
#     main = """
#     id entry_type user group
#     region city street street_no
#     price bedrooms bathrooms livable_space land
#     availability_text availability_date
#     pub_date album
#     title
#     body
#     """


class Entries(dd.Table):
    model = "immo.Entry"
    column_names = 'title group pub_date *'
    default_display_modes = {
        None: constants.DISPLAY_MODE_TILES}
    detail_layout = "immo.EntryDetail"
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


class AlbumItemsByEntry(ItemsByAlbum):
    label = _("Pictures")

    @classmethod
    def get_filter_kw(self, ar, **kw):
        if (mi := ar.master_instance) is None or mi.album is None:
            return None
        kw.update(album=mi.album)
        return kw
        # return super().get_filter_kw(ar, **kw)
