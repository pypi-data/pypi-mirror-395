# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino.core import constants
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.users.mixins import PrivacyRelevant
from lino.modlib.bootstrap5 import PAGE_TITLE_TEMPLATE
from lino.modlib.publisher.mixins import Publishable, PublishableContent, Illustrated
from lino.modlib.comments.mixins import Commentable
from lino.modlib.memo.mixins import BabelPreviewable
from lino.modlib.uploads.choicelists import ImageFormats, ImageSizes
from lino.utils.html import format_html, escape, mark_safe
from lino.utils.mldbc.mixins import BabelDesignated
from lino_xl.lib.topics.mixins import Taggable
from lino_vedi.lib.contacts.choicelists import PartnerRoles

from .ui import *

WITH_CAROUSEL = True


class EntryType(BabelDesignated, PublishableContent):

    class Meta:
        app_label = "immo"
        verbose_name = _("Object type")
        verbose_name_plural = _("Object types")


class Entry(
        UserAuthored, PrivacyRelevant, BabelPreviewable, Commentable,
        PublishableContent, Illustrated, Taggable):

    class Meta:
        app_label = "immo"
        verbose_name = _("Real estate object")
        verbose_name_plural = _("Real estate objects")

    memo_command = "entry"

    entry_type = dd.ForeignKey('immo.EntryType')
    title = dd.BabelCharField(_("Title"), max_length=200)

    def __str__(self):
        return dd.babelattr(self, "title")

    @classmethod
    def setup_parameters(cls, fields):
        fields.setdefault(
            'author', dd.ForeignKey(
                'contacts.Person', verbose_name=_("Author"), blank=True, null=True))
        fields.setdefault(
            'mentor', dd.ForeignKey(
                'contacts.Person', verbose_name=_("Mentor"), blank=True, null=True))
        fields.setdefault(
            'topic', dd.ForeignKey(
                'topics.Topic', blank=True, null=True))
        super().setup_parameters(fields)

    @classmethod
    def get_simple_parameters(cls):
        lst = list(super().get_simple_parameters())
        # lst.append('group')
        lst.append('entry_type')
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
        if self.entry_type:
            info.append(ar.obj2htmls(self.entry_type))
        if self.pub_date:
            info.append(str(self.pub_date.year))
        s = mark_safe("|".join(info))

        s += mark_safe("<br>")
        if (img := self.main_image) is not None:
            if (mf := img.get_media_file()) is not None:
                s += img.as_html(
                    ar, mf, image_size=ImageSizes.solo,
                    image_format=ImageFormats.square)

        s += mark_safe("<br>")
        t = _("Published {}")
        t = t.format(self.pub_date)
        s += ar.obj2htmls(self, title=t)

        # prl = []
        # PartnerCast = rt.models.contacts.PartnerCast
        # for cast in PartnerCast.objects.filter(
        #         entry=self, role=PartnerRoles.author):
        #     prl.append(ar.obj2htmls(
        #         cast.partner,
        #         f"{cast.partner.first_name} {cast.partner.last_name}".strip()))
        # if len(prl) > 0:
        #     # s += format_html(" {} ", _("by"))
        #     s += format_html("<br>{} ", "👤")  # (U+1F464)
        #     s += mark_safe(", ".join(prl))

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

        # prl = []
        # PartnerCast = rt.models.contacts.PartnerCast
        # for cast in PartnerCast.objects.filter(
        #         entry=self, role=PartnerRoles.author):
        #     prl.append(ar.obj2htmls(
        #         cast.partner,
        #         f"{cast.partner.first_name} {cast.partner.last_name}".strip()))
        # if len(prl) > 0:
        #     s += format_html(" {} ", _("by"))
        #     s += mark_safe(", ".join(prl))

        if (img := self.main_image) is not None:
            if (mf := img.get_media_file()) is not None:
                s += img.as_html(
                    ar, mf, image_size=ImageSizes.small,
                    image_format=ImageFormats.right)
        if self.body_short_preview:
            s += mark_safe("\n" + self.body_short_preview)
        return s

    def as_page(self, ar, display_mode="detail", **kwargs):
        title = dd.babelattr(self, "title")
        yield PAGE_TITLE_TEMPLATE.format(escape(title))
        items = []
        for pr in PartnerRoles.get_list_items():
            prl = []
            PartnerCast = rt.models.contacts.PartnerCast
            for cast in PartnerCast.objects.filter(entry=self, role=pr):
                prl.append(ar.obj2htmls(cast.partner))
            if len(prl) > 1:
                text = pr.text_plural
            elif len(prl) == 1:
                text = pr.text
            else:
                continue
            items.append(format_html("{}: {}", text, mark_safe("; ".join(prl))))

        for k in ('entry_type', 'group', 'user'):
            value = getattr(self, k)
            if value is not None:
                fld = self.__class__._meta.get_field(k)
                items.append(format_html(
                    "{}: {}", fld.verbose_name, ar.obj2htmls(value)))
        if len(items):
            txt = " | ".join(items)
            yield """<p class="small">{}</p>""".format(txt)
            # https://getbootstrap.com/docs/3.4/css/#small-text

        if self.album_id:
            yield '<div class="bg-secondary-subtle border-secondary-subtle rounded-3">'
            for item in self.album.items.filter(upload__isnull=False):
                if (mf := item.upload.get_media_file()) is not None:
                    yield item.upload.as_html(
                        ar, mf,
                        image_format=item.get_image_format(),
                        image_size=item.get_image_size(),
                        title=self.title)
            yield '</div>'

        yield dd.babelattr(self, "body_full_preview")

        if self.album_id:
            if WITH_CAROUSEL:
                carouselid = self.__class__.__name__ + str(self.pk)
                yield f"""
                <div id="{carouselid}" class="carousel slide" data-bs-ride="carousel">
                  <div class="carousel-inner">
                """
                active = "active"
                for item in self.album.items.filter(upload__isnull=False):
                    if (mf := item.upload.get_media_file()) is not None:
                        yield f"""<div class="carousel-item {active}">"""
                        active = ""
                        yield item.upload.as_html(
                            ar, mf,
                            image_format=ImageFormats.carousel,
                            image_size=ImageSizes.big,
                            # image_size=item.get_image_size(),
                            class_names="d-block w-100",
                            # class_names="d-block",
                            title=self.title, clickable=False)
                        yield """</div>"""
                yield f"""
                  </div>
                  <button class="carousel-control-prev" type="button" data-bs-target="#{carouselid}" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                  </button>
                  <button class="carousel-control-next" type="button" data-bs-target="#{carouselid}" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                  </button>
                </div>
                """


dd.update_field(Entry, 'user', verbose_name=_("Editor"))
