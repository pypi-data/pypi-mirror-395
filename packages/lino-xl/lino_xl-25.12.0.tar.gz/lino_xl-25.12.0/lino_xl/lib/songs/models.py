# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import re
import subprocess
from PIL import Image, ImageChops
from textwrap import dedent
from jinja2.exceptions import TemplateNotFound
from django.conf import settings
from lino.api import dd, rt, _
from lino.core import constants
from lino.mixins.sequenced import Hierarchical
from lino.mixins import Modified
from lino.mixins.clonable import Clonable
from lino.modlib.bootstrap5 import PAGE_TITLE_TEMPLATE
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.users.mixins import PrivacyRelevant
from lino.modlib.publisher.mixins import PublishableContent  # , TranslatableContent
from lino.modlib.comments.mixins import Commentable
from lino.modlib.memo.mixins import TitledPreviewable
from lino.modlib.uploads.choicelists import ImageFormats, ImageSizes, htmlimg
from lino.utils.html import format_html, escape, mark_safe, tostring
# from lino.utils.config import must_make
from lino.utils.mldbc.mixins import BabelDesignated
from lino_xl.lib.topics.mixins import Taggable
from lino_xl.lib.sources.mixins import Copyrighted
from lino.utils.media import MediaFile
from lino_xl.lib.sources.choicelists import AuthorRoles
from .ui import *

if dd.plugins.songs.use_lilypond:
    from lilyponddist import lilypondbin


AUTHOR_MODEL = dd.plugins.sources.author_model
TICKET_MODEL = dd.get_plugin_setting('publisher', 'ticket_model', None)


def crop_image(pth):
    # thanks to neouyghur https://stackoverflow.com/a/48605963/407239
    im = Image.open(pth)
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    # Bounding box given as a 4-tuple defining the left, upper, right, and lower pixel coordinates.
    # If the image is completely empty, this method returns None.
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        im.save(pth)


class LilyFormat(dd.Choice):
    def __init__(self, name, tplname):
        self.tplname = tplname
        super().__init__(name, name, name)


class LilyFormats(dd.ChoiceList):
    item_class = LilyFormat


add = LilyFormats.add_item
add("web", "songs/satb_web.jinja.ly")
add("a4", "songs/satb_a4.jinja.ly")


class SongType(BabelDesignated, PublishableContent):

    class Meta:
        app_label = "songs"
        verbose_name = _("Song type")
        verbose_name_plural = _("Song types")


class SongProxy:

    def __init__(self, fmt, song):
        self.fmt = fmt
        self.song = song
        # self.errors = self.build_lilypond()
        # self.line_width = fmt.line_width
        # self.pk = song.pk
        # self.tempo = song.scores_tempo
        # self.preamble = song.scores_preamble
        # self.soprano = song.scores_soprano
        # self.alto = song.scores_alto
        # self.tenor = song.scores_tenor
        # self.bass = song.scores_bass
        # self.lyrics = song.scores_lyrics
        # self.chords = song.scores_chords
        # # self.errors = song.scores_errors
        # self.other_font = song.other_font

    @property
    def media_file(self):
        leaf = self.fmt.value + "_" + str(self.song.pk) + ".png"
        return MediaFile(False, "cache", "songs", leaf)

    @property
    def scores_image(self):
        if dd.plugins.songs.use_lilypond:
            if self.song.scores_preamble:
                mf = self.media_file
                mtime = self.song.modified
                if mtime is None or not mf.path.exists() or mtime.timestamp() > mf.path.stat().st_mtime:
                    # print("20251117 must build...")
                    self.song.scores_errors = self.build_lilypond()
                    # print(self.build_lilypond())
                    self.song.touch()
                    self.song.full_clean()
                    self.song.save()
                return mf

    def build_lilypond(self):
        if not dd.plugins.songs.use_lilypond:
            return ""
        mf = self.media_file
        if mf is None:
            return ""
        env = settings.SITE.plugins.jinja.renderer.jinja_env
        try:
            tpl = env.get_template(self.fmt.tplname)
        except TemplateNotFound as e:
            return str(e)
        context = dict()  # ar.get_printable_context()
        context.update(sng=self.song)
        scores_source = tpl.render(**context)
        mf.path.unlink(missing_ok=True)
        src = settings.SITE.site_dir / "tmp.ly"
        src.write_text(scores_source)
        mf.path.parent.mkdir(exist_ok=True, parents=True)
        cmd = [lilypondbin(), '--png', '-o', mf.path.with_suffix(''), src]
        options = dict(stdout=subprocess.PIPE,
                       universal_newlines=True,
                       stderr=subprocess.STDOUT)
        ret = subprocess.run(cmd, **options)
        if mf.path.exists():
            crop_image(mf.path)
        return ret.stdout


class Song(
        UserAuthored, PrivacyRelevant, TitledPreviewable, Commentable,
        PublishableContent, Copyrighted, Taggable, Hierarchical, Modified):

    class Meta:
        app_label = "songs"
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")

    memo_command = "song"

    song_type = dd.ForeignKey('songs.SongType', blank=True, null=True)
    language = dd.ForeignKey('languages.Language', blank=True, null=True)
    # source = dd.ForeignKey('sources.Source', blank=True, null=True)
    scores_tempo = dd.CharField(_("Tempo"), max_length=200, blank=True)
    scores_preamble = dd.CharField(_("Preamble"), max_length=200, blank=True)
    scores_line_width = dd.CharField(_("Line width"), max_length=200, blank=True)
    scores_soprano = dd.RichTextField(_("Soprano"), blank=True, format="plain")
    scores_alto = dd.RichTextField(_("Alto"), blank=True, format="plain")
    scores_tenor = dd.RichTextField(_("Tenor"), blank=True, format="plain")
    scores_bass = dd.RichTextField(_("Bass"), blank=True, format="plain")
    scores_lyrics = dd.RichTextField(_("Lyrics"), blank=True, format="plain")
    scores_chords = dd.RichTextField(_("Chords"), blank=True, format="plain")
    scores_errors = dd.RichTextField(
        _("Compilation output"), format="plain", editable=False)

    other_font = dd.BooleanField(_("Other font in second verse"), default=False)

    def __str__(self):
        return self.title

    def after_duplicate(self, ar, master):
        super().after_duplicate(ar, master)
        self.parent = master

    # def before_ui_save(self, ar, cw):
    #     self.scores_errors = self.build_lilypond()
    #     super().before_ui_save(ar, cw)

    def get_lyrics(self):
        lyrics = dedent(self.scores_lyrics.strip())
        # print(repr(lyrics))
        if lyrics.startswith("- "):
            rv = re.split(r"^\W*- ", lyrics,  flags=re.MULTILINE)
            # print(rv)
            assert rv[0] == ""
            # print(rv[1:])
            return rv[1:]
        return [lyrics]

    @classmethod
    def setup_parameters(cls, fields):
        fields.setdefault(
            'author', dd.ForeignKey(
                AUTHOR_MODEL, verbose_name=_("Author"), blank=True, null=True))
        fields.setdefault(
            'composer', dd.ForeignKey(
                AUTHOR_MODEL, verbose_name=_("Composer"), blank=True, null=True))
        fields.setdefault(
            'topic', dd.ForeignKey(
                'topics.Topic', blank=True, null=True))
        super().setup_parameters(fields)

    @classmethod
    def get_simple_parameters(cls):
        lst = list(super().get_simple_parameters())
        lst.append('group')
        lst.append('song_type')
        lst.append('pub_date')
        return lst

    # def as_tile(self, ar, prev, **kwargs):
    #     s = f"""<span style="font-size:2rem; float:left; padding-right:1rem;">{
    #         ar.obj2htmls(self)}</span> """
    #     s += _("{} pupils").format(Enrolment.objects.filter(group=self).count())
    #     s += "<br>"
    #     sar = rt.models.school.CoursesByGroup.create_request(
    #         parent=ar, master_instance=self)
    #     s += " ".join([
    #         sar.obj2htmls(
    #             obj, obj.subject.icon_text or str(obj.subject), title=str(obj.subject))
    #         for obj in sar])
    #     s = constants.TILE_TEMPLATE.format(chunk=s)
    #     if prev is not None and prev.grade != self.grade:
    #         s = """<p style="display:block;"></p>""" + s
    #     return mark_safe(s)

    def as_tile(self, ar, prev, **kwargs):
        if ar is None:
            return str(self)
        info = []
        if self.song_type:
            info.append(ar.obj2htmls(self.song_type))
        if self.pub_date:
            info.append(str(self.pub_date.year))
        s = mark_safe("|".join(info))

        s += mark_safe("<br>")
        t = _("Published {}")
        t = t.format(self.pub_date)
        s += ar.obj2htmls(self, title=t)

        prl = []
        AuthorCast = rt.models.sources.AuthorCast
        qs = AuthorCast.controlled_rows(self, role=AuthorRoles.author)
        for cast in qs:
            prl.append(ar.obj2htmls(
                cast.author,
                f"{cast.author.first_name} {cast.author.last_name}".strip()))
        if len(prl) > 0:
            # s += format_html(" {} ", _("by"))
            s += format_html("<br>{} ", "👤")  # (U+1F464)
            s += mark_safe(", ".join(prl))

        # if self.body_short_preview:
        #     s += mark_safe("\n" + self.body_short_preview)
        return format_html(constants.TILE_TEMPLATE, chunk=s)

    def as_paragraph(self, ar):
        if ar is None:
            return str(self)
        s = mark_safe("")
        t = _("Published {}")
        t = t.format(self.pub_date)
        s += ar.obj2htmls(self, title=t)

        prl = []
        AuthorCast = rt.models.sources.AuthorCast
        exposed_roles = {AuthorRoles.author, AuthorRoles.composer}
        for cast in AuthorCast.controlled_rows(self, role__in=exposed_roles):
            prl.append(ar.obj2htmls(
                cast.author,
                f"{cast.author.first_name} {cast.author.last_name}".strip()))
        if len(prl) > 0:
            s += format_html(" ({})", mark_safe(", ".join(prl)))

        if self.body_short_preview:
            s += mark_safe("\n" + self.body_short_preview)
        return s

    # def get_page_title(self):
    #     title = dd.babelattr(self, "title")
    #     return PAGE_TITLE_TEMPLATE.format(escape(title))

    def as_page(self, ar, display_mode="detail", title=None, **kwargs):
        yield self.get_title_div(ar)
        # yield title or self.get_page_title()
        items = []
        for pr in AuthorRoles.get_list_items():
            prl = []
            AuthorCast = rt.models.sources.AuthorCast
            for cast in AuthorCast.controlled_rows(self, role=pr):
                prl.append(ar.obj2htmls(cast.author))
            if len(prl) > 1:
                text = pr.text_plural
            elif len(prl) == 1:
                text = pr.text
            else:
                continue
            items.append(format_html("{}: {}", text, mark_safe("; ".join(prl))))

        srcrefs = []
        for srcref in rt.models.sources.SourceRef.controlled_rows(self):
            srcrefs.append(ar.obj2htmls(srcref.source))
        if len(srcrefs):
            text = rt.models.sources.SourceRef._meta.verbose_name_plural
            items.append(format_html("{}: {}", text, mark_safe("; ".join(srcrefs))))

        show_fields = ['song_type', 'parent']
        if False:
            show_fields.append('language')
            show_fields.append('user')
            show_fields.append('group')
        for k in show_fields:
            value = getattr(self, k)
            if value is not None:
                fld = self.__class__._meta.get_field(k)
                items.append(format_html(
                    "{}: {}", fld.verbose_name, ar.obj2htmls(value)))
        if self.license:
            lic = format_html('<a href="{}">{}</a>', self.license.url, self.license)
            if self.copyright_owner:
                items.append(format_html(
                    '&copy; {} ({})', ar.obj2htmls(self.copyright_owner), lic))
            else:
                items.append(lic)

        if TICKET_MODEL:
            qs = rt.models.publisher.PageItem.objects.filter(ticket=self)
            if qs.count() > 0:
                used_in = mark_safe(", ".join([
                    tostring(obj.page.as_summary_item(ar))
                    for obj in qs.order_by('id')]))
                items.append(format_html(
                    "{}: {}", _("Used in"), used_in))

        if len(items):
            txt = " | ".join(items)
            yield """<p class="small">{}</p>""".format(txt)
            # https://getbootstrap.com/docs/3.4/css/#small-text

        sng = SongProxy(LilyFormats.web, self)
        if (mf := sng.scores_image) is not None:
            yield htmlimg(
                src=mf.url,
                # image_size=ImageSizes.solo,
                image_format=ImageFormats.full)

        # print(f"20251023 {self.body}")
        yield self.body_full_preview.replace('<br class="soft-break"/>', "/ ")

    def as_page_item(self, item, ar):
        s = format_html("<h3>{} {}</h3>", item.seqno, self.title)
        sng = SongProxy(LilyFormats.a4, self)
        if (mf := sng.scores_image) is not None:
            s += htmlimg(
                src=f"file://{mf.path}",
                # image_size=ImageSizes.solo,
                image_format=ImageFormats.full)
        s += self.body_full_preview.replace('<br class="soft-break"/>', "/ ")
        return s


dd.update_field(Song, 'user', verbose_name=_("Editor"))
dd.update_field(Song, 'parent', verbose_name=_("Derived from"))
