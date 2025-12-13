# -*- coding: UTF-8 -*-
# Copyright 2008-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


from lino.api import dd, rt, _
from lino.core import constants
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.users.mixins import UserAuthored, PrivacyRelevant, My
from lino.mixins.sequenced import Sequenced
from lino.modlib.uploads.choicelists import ImageFormats, ImageSizes


def filename_leaf(name):
    i = name.rfind('/')
    if i != -1:
        return name[i + 1:]
    return name


class Album(UserAuthored, PrivacyRelevant):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Album')
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")

    title = dd.CharField(_("Title"), max_length=200)
    image_format = ImageFormats.field(blank=True, null=True)
    image_size = ImageSizes.field(blank=True, null=True)

    def __str__(self):
        return f"{self._meta.verbose_name} {self.pk} ({self.title})"


class AlbumItem(Sequenced):

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'AlbumItem')
        verbose_name = _("Album item")
        verbose_name_plural = _("Album items")
        ordering = ['album', 'seqno']

    album = dd.ForeignKey('albums.Album', related_name="items")
    upload = dd.ForeignKey('uploads.Upload')
    title = dd.CharField(_("Title"), max_length=250, blank=True)
    image_format = ImageFormats.field(blank=True, null=True)
    image_size = ImageSizes.field(blank=True, null=True)

    def get_str_words(self, ar):
        if not ar.is_obvious_field("upload"):
            yield str(self.upload)
        if not ar.is_obvious_field("album"):
            yield _("in {album}").format(album=self.album)

    def as_summary_item(self, ar, text=None, **kwargs):
        # raise Exception("20240613")
        if ar is None:
            obj = super()
        elif ar.is_obvious_field('upload'):
            obj = self.album
        elif ar.is_obvious_field('album'):
            obj = self.upload
        else:
            obj = super()
        return obj.as_summary_item(ar, text, **kwargs)

    def get_siblings(self):
        return self.__class__.objects.filter(album=self.album)

    def get_image_format(self):
        return self.image_format or self.album.image_format or ImageFormats.inline

    def get_image_size(self):
        return self.image_size or self.album.image_size or ImageSizes.default

    def get_gallery_item(self, ar):
        return self.upload.get_gallery_item(ar)

    def as_tile(self, ar, prev, **kwargs):
        if self.title:
            kwargs.update(title=self.title)
        kwargs.update(image_format=self.get_image_format())
        kwargs.update(image_size=self.get_image_size())
        return self.upload.as_tile(ar, prev, **kwargs)


# dd.inject_field('uploads.Upload', 'album',
#                 dd.ForeignKey("albums.Album", blank=True, null=True))


class AlbumDetail(dd.DetailLayout):
    main = """
    title image_format image_size id
    user group
    ItemsByAlbum
    """


class Albums(dd.Table):
    model = 'albums.Album'
    required_roles = dd.login_required(OfficeStaff)

    column_names = "title user group id *"
    detail_layout = "albums.AlbumDetail"
    insert_layout = """
    title
    group
    """


class MyAlbums(My, Albums):
    required_roles = dd.login_required(OfficeUser)


class AlbumItems(dd.Table):
    model = 'albums.AlbumItem'
    required_roles = dd.login_required(OfficeStaff)
    detail_layout = dd.DetailLayout("""
    upload upload__preview
    album seqno
    title
    image_format image_size
    """, window_size=('auto', 40))

    insert_layout = """
    album
    upload
    """


class ItemsByAlbum(AlbumItems):
    master_key = "album"
    default_display_modes = {None: constants.DISPLAY_MODE_TILES}
    column_names = "seqno upload upload__thumbnail title image_format image_size *"
    insert_layout = """
    upload
    title
    """


class ItemsByUpload(AlbumItems):
    master_key = "upload"
    default_display_modes = {
        None: constants.DISPLAY_MODE_SUMMARY,
        70: constants.DISPLAY_MODE_GRID}
    column_names = "seqno album title image_format image_size *"
    insert_layout = """
    album
    title
    """
