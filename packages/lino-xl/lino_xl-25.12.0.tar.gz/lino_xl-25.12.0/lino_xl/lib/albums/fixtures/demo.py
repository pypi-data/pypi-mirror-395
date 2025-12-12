# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger
from lino.api import rt, dd, _
from lino.utils import Cycler
from lino.modlib.uploads.mixins import make_uploaded_file

try:
    from lino_book import DEMO_DATA
except ImportError:
    DEMO_DATA = None


def objects():
    AlbumItem = rt.models.albums.AlbumItem
    Upload = rt.models.uploads.Upload
    # Volume = rt.models.uploads.Volume

    demo_date = dd.demo_date()
    user = dd.plugins.users.get_demo_user()

    def album(title):
        return rt.models.albums.Album(title=title, user=user)

    # yield album(_("Furniture"))
    # yield album(_("Things")))
    # yield album(_("Services")))
    # yield album(_("Biographies"))
    # yield album(_("Business"))
    # yield album(_("Culture"))
    # yield album(_("Children"))
    # yield album(_("Medicine"))

    thrill = album(_("Thriller book covers"))
    yield thrill

    if DEMO_DATA is None:
        logger.info("No demo data because lino_book is not installed")
        return

    for i, cover in enumerate("""\
MurderontheOrientExpress.jpg Murder_on_the_orient_express_cover
StormIsland.jpg Storm_island_cover
AndThenThereWereNone.jpg And_then_there_were_none
FirstThereWereTen.jpg First_there_were_ten
""".splitlines()):
        name, description = cover.split()
        src = DEMO_DATA / "images" / name
        file = make_uploaded_file(name, src, demo_date)
        obj = Upload(file=file, description=description.replace('_', ' '))
        yield obj
        yield AlbumItem(album=thrill, upload=obj, seqno=i+1)

    photos_album = album(_("Photos"))
    yield photos_album

    # photos_vol = Volume.objects.get(ref="photos")
    for i, obj in enumerate(Upload.objects.filter(volume__ref="photos")):
        yield AlbumItem(album=photos_album, upload=obj, seqno=i+1)
