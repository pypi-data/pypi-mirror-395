# -*- coding: UTF-8 -*-
# Copyright 2009-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from io import StringIO
from lxml import etree
from html import escape

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext
from django.utils.html import format_html
from django.utils import timezone
from lino.utils.html import E, tostring
from lino.utils.soup import MORE_MARKER

from lino.api import dd, rt
from lino.core.constants import DISPLAY_MODE_LIST, DISPLAY_MODE_STORY, DISPLAY_MODE_SUMMARY
from lino.core.gfks import gfk2lookup, ContentType
# from lino.modlib.uploads.mixins import UploadBase
# from lino.core.utils import models_by_base
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import My, UserAuthored
from lino.modlib.publisher.mixins import TranslatableContent, PublishableContent, Illustrated
# from lino.modlib.publisher.choicelists import PublisherViews
from lino.modlib.comments.mixins import Commentable
from lino_xl.lib.topics.mixins import Taggable
# from lino.modlib.printing.mixins import PrintableType, TypedPrintable
from lino.utils.mldbc.mixins import BabelNamed
from lino.core.requests import BaseRequest
from lino.modlib.memo.mixins import TitledPreviewable
from lino.modlib.system.mixins import format_time
from lino.modlib.office.roles import OfficeUser
from lino.utils import join_elems
from lino.modlib.publisher.choicelists import SpecialPages

# from lino_xl.lib.pages.models import Node, NodeDetail
# from lino_xl.lib.pages.choicelists import PageTypes

from .roles import BlogsReader

html_parser = etree.HTMLParser()


class EntryType(BabelNamed):

    templates_group = 'blogs/Entry'

    class Meta():
        app_label = 'blogs'
        abstract = dd.is_abstract_model(__name__, 'EntryType')
        verbose_name = _("Blog Entry Type")
        verbose_name_plural = _("Blog Entry Types")

    # ~ name = models.CharField(max_length=200)
    important = models.BooleanField(verbose_name=_("important"), default=False)
    remark = models.TextField(verbose_name=_("Remark"), blank=True)

    def __str__(self):
        return self.name


class EntryTypes(dd.Table):
    model = 'blogs.EntryType'
    # column_names = 'name build_method template *'
    order_by = ["name"]

    detail_layout = """
    id name
    # build_method template
    remark:60x5
    blogs.EntriesByType
    """


# class Entry(Node, UserAuthored, Controllable, CombinedDateTime, TranslatablePublishableContent):
class Entry(TitledPreviewable, Commentable, UserAuthored, Controllable,
            PublishableContent, Illustrated, TranslatableContent, Taggable):

    class Meta:
        app_label = 'blogs'
        abstract = dd.is_abstract_model(__name__, 'Entry')
        verbose_name = _("Blog entry")
        verbose_name_plural = _("Blog entries")

    memo_command = "blog"

    entry_type = dd.ForeignKey('blogs.EntryType', blank=True, null=True)

    def __str__(self):
        if self.title:
            return self.title
        if self.pub_date:
            return _("{} by {}").format(self.pub_date, self.user)
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    # def get_detail_action(self, ar):
    #     user = ar.get_user()
    #     if user.user_type.has_required_roles([BlogsReader]) and \
    #         user == self.user:
    #         return super().get_detail_action(ar)
    #     return rt.models.blogs.PublicEntries.detail_action

    # def get_page_type(self):
    #     return PageTypes.blogs

    # @dd.htmlbox(_("Preview"))
    @dd.htmlbox()
    def preview(self, ar):
        if ar is None:
            return
        return ''.join(self.as_page(ar))

    # def get_item_preview(self, ar):
    #     if ar is None:
    #         return
    #     return ar.row_as_paragraph(self)

    # @dd.htmlbox()
    # def item_preview(self, ar):
    #     return self.get_item_preview(ar)

    # def as_story_item(self, ar):
    #     if ar is None:
    #         return
    #     return ''.join(ar.row_as_page(self))
    #     # return ar.row_as_paragraph(self)

    # def get_primary_image(self):
    #     Mention = rt.models.memo.Mention
    #     # stypes = [ContentType.objects.get_for_model(m)
    #     #     for m in models_by_base(UploadBase)]
    #     # qs = Mention.objects.filter(**gfk2lookup(
    #     #     Mention.owner, self, source_type__in=stypes))
    #     file_type = ContentType.objects.get_for_model(rt.models.uploads.Upload)
    #     qs = Mention.objects.filter(**gfk2lookup(
    #         Mention.owner, self, source_type=file_type))
    #         # Mention.owner, self, source_type__in=stypes))
    #     for obj in qs:
    #         if obj.source.file is not None:
    #             return obj.source

    def get_node_info(self, ar):
        # print("20231031", ar.renderer)
        if self.pub_time:
            when = _("on {date} at {time}").format(
                date=self.pub_date.isoformat(),
                time=format_time(self.pub_time))
        else:
            when = _("on {date}").format(date=self.pub_date.isoformat())
        return _("Published {when} by {author}").format(author=tostring(
            ar.obj2html(self.user)),
                                                        when=when)

    def as_page(self, ar, display_mode="detail", **kwargs):
        hlevel = 1
        yield "<h{0}>{1}</h{0}>".format(hlevel, escape(self.title))
        info = self.get_node_info(ar)
        if info:
            yield """<p class="small">{}</p>""".format(info)
            # https://getbootstrap.com/docs/3.4/css/#small-text

        yield self.body_full_preview

    def unused_as_page(self, ar, **kwargs):
        title = self.title or self
        # img = self.get_primary_image()
        pub_info = _("Published {date} by {author}").format(
            date=self.pub_date.isoformat(),
            author=tostring(ar.obj2html(self.user)))
        if False:  # ar.get_user() == self.user:
            btn = tostring(
                ar.row_action_button(self,
                                     rt.models.blogs.MyEntries.detail_action,
                                     label='edit',
                                     icon_name=None,
                                     CLASS='pi pi-pencil'))
            title += '<span style="float: right;">{}</span>'.format(btn)

        # yield """<div style="display:flex; max-width:80ch; margin:auto;">"""
        yield """<div style="max-width:80ch; margin:auto;">"""
        yield "<h1>{}</h1>".format(title)
        # if img is not None:
        #     yield """
        #     <p><figure>
        #     {img.thumbnail_large}
        #     <figcaption style="text-align: center;">{img.description}</figcaption>
        #     </figure></p>
        #     """.format(img=img, obj=self)
        yield """<p><em>{}</em></p>""".format(pub_info)
        yield """<hr/>"""
        yield self.body_full_preview
        yield "</div>"

    def unused_as_paragraph(self, ar):
        title = self.title or self
        pub_info = format_html(_("Published {date} by {author}"),
                               date=self.pub_date.isoformat(), author=self.user)
        # url = escape(ar.obj2url(self))
        # url = self.publisher_url(ar)
        url = ar.obj2url(self)
        s = format_html("""<a href="{}"><strong>{}</strong> — """, url, title)
        s += format_html("""<span style="font-size:70%;"><em>{}</em></span></a>""",
                         pub_info)
        # s += "<p>{}</p>".format(self.body_short_preview)
        s += """<div style="display:flex;">"""
        # img = self.get_primary_image()
        # if img is not None:
        #     s += f"""<div style="margin-right:20px;"><a href="{url}">{img.thumbnail}</a></div>"""
        # else:
        #     s += """<div>no image</div>"""
        s += """<div><p style="text-align:justify;">"""
        s += self.body_short_preview
        s += """</p></div>"""
        s += """</div>"""
        return s

    @classmethod
    def unused_get_dashboard_items(cls, user):
        qs = cls.objects.filter(pub_date__isnull=False).order_by("-pub_date")
        return qs[:5]

    @classmethod
    def get_dashboard_objects(cls, ar):
        # qs = cls.objects.filter(pub_date__isnull=False).order_by('-pub_date')
        # return qs[:5]
        return cls.get_dashboard_items(ar.get_user())

    # def compute_summary_values(self):
    #     print("20231029 jaa")
    #     prev = None
    #     for node in self.__class__.objects.order_by('pub_date', 'pub_time'):
    #         node.set_prev(prev)
    #         prev = node

    # @classmethod
    # def latest_entries(cls, ar, max_num=10, **context):
    #     context = ar.get_printable_context(**context)
    #     qs = cls.objects.filter(pub_date__isnull=False)
    #     qs = qs.order_by("-pub_date")
    #     s = ''
    #     render = dd.plugins.jinja.render_jinja
    #     for num, e in enumerate(qs):
    #         if num >= max_num:
    #             break
    #         context.update(obj=e)
    #         s += render(ar, 'blogs/entry.html', context)
    #     return s


# class Tagging(dd.Model):
#     """A **tag** is the fact that a given entry mentions a given topic.

#     """
#     class Meta:
#         app_label = 'blogs'
#         verbose_name = _("Tagging")
#         verbose_name_plural = _('Taggings')

#     allow_cascaded_delete = ['entry', 'topic']

#     topic = dd.ForeignKey(
#         'topics.Topic',
#         related_name='tags_by_topic')

#     entry = dd.ForeignKey(
#         'blogs.Entry',
#         related_name='tags_by_entry')

# class EntryDetail(NodeDetail):
#
#     right_panel = """
#     entry_type
#     pub_date pub_time
#     user:10
#     parent seqno
#     child_node_depth
#     page_type filler
#     language
#     owner
#     """


class EntryDetail(dd.DetailLayout):

    main = "general preview_panel more"

    general = dd.Panel("""
    content_panel:60 right_panel:20
    """,
                       label=_("General"),
                       required_roles=dd.login_required(OfficeUser))

    preview_panel = dd.Panel("""
    preview
    """, label=_("Preview"))

    more = dd.Panel("""
    topics.TagsByOwner:20 comments.CommentsByRFC:60
    """,
                    label=_("More"),
                    required_roles=dd.login_required(OfficeUser))

    content_panel = """
    title
    body
    # pages.NodesByParent
    """

    right_panel = """
    user:10
    entry_type
    pub_date pub_time
    # publisher_tree
    id
    owner
    """


class ItemLayout(dd.DetailLayout):
    main = "layout"

    layout = "meta:30 body_short_preview:70"

    meta = """
    user
    pub_date
    """


class Entries(dd.Table):
    required_roles = set([BlogsReader])

    model = 'blogs.Entry'
    column_names = "id pub_date user entry_type title *"
    order_by = ["-id"]

    hide_top_toolbar = False

    default_display_modes = {70: DISPLAY_MODE_LIST, None: DISPLAY_MODE_STORY}

    insert_layout = """
    title
    entry_type
    """

    detail_layout = 'blogs.EntryDetail'
    # list_layout = ItemLayout()

    @classmethod
    def collect_extra_actions(cls):
        yield dd.WrappedAction(rt.models.blogs.PublicEntries.detail_action,
                               label=_("Pretty view"),
                               icon_name=None)


# PageTypes.add_item(Entries, "blogs")


class PublicEntries(Entries):
    required_roles = set()  # also for anonymous
    # hide_top_toolbar = True
    # detail_layout = """
    # preview
    # comments.CommentsByRFC
    # """

    @classmethod
    def collect_extra_actions(cls):
        return []

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)
        if ar.request is not None and ar.request.LANGUAGE_CODE:
            qs = qs.filter(language__in={ar.request.LANGUAGE_CODE, ''})
            # filter.setdefault('language', ar.request.LANGUAGE_CODE)
        return qs


# PublisherViews.add_item_lazy("b", PublicEntries)


class MyEntries(My, Entries):
    required_roles = dd.login_required(BlogsReader, dd.SiteStaff)
    # ~ master_key = 'user'
    column_names = "id pub_date entry_type title body *"
    # order_by = ["-modified"]


class AllEntries(Entries):
    required_roles = dd.login_required(dd.SiteStaff)


# ~ class NotesByProject(Notes):
# ~ master_key = 'project'
# ~ column_names = "date subject user *"
# ~ order_by = "date"

# ~ class NotesByController(Notes):
# ~ master_key = 'owner'
# ~ column_names = "date subject user *"
# ~ order_by = "date"


class EntriesByType(Entries):
    master_key = 'entry_type'
    column_names = "pub_date title user *"
    order_by = ["pub_date-"]
    # ~ label = _("Notes by person")


class EntriesByController(Entries):  # currently not used anywhere
    master_key = 'owner'
    column_names = "pub_date title user *"
    order_by = ["-pub_date"]
    default_display_modes = {None: DISPLAY_MODE_SUMMARY}

    @classmethod
    def table_as_summary(self, ar):
        def fmt(obj):
            return str(obj)

        elems = []
        for obj in ar:
            # if len(elems) > 0:
            #     elems.append(', ')

            lbl = fmt(obj)
            # if obj.state.button_text:
            #     lbl = "{0}{1}".format(lbl, obj.state.button_text)
            elems.append(ar.obj2html(obj, lbl))
        elems = join_elems(elems, sep=', ')
        toolbar = []
        ar2 = self.insert_action.request_from(ar)
        if ar2.get_permission():
            btn = ar2.ar2button()
            toolbar.append(btn)

        if len(toolbar):
            toolbar = join_elems(toolbar, sep=' ')
            elems.append(E.p(*toolbar))

        return tostring(elems)


class LatestEntries(PublicEntries):
    """Show the most recent blog entries."""
    label = _("Latest blog entries")
    column_names = "pub_date title user *"
    order_by = ["-pub_date"]
    filter = models.Q(pub_date__isnull=False)
    default_display_modes = {None: DISPLAY_MODE_LIST}
    # editable = False
    insert_layout = None  # disable the (+) button but permit editing


# PublisherViews.add_item_lazy("latest", LatestEntries)


SpecialPages.add_item(
    "blog",  # filler=filler,
    body=_("This page is our blog.") + MORE_MARKER + " [show blogs.LatestEntries]",
    title=_("Blog"),
    parent='home')


# class Taggings(dd.Table):
#     model = 'blogs.Tagging'

# class AllTaggings(Taggings):
#     required_roles = dd.login_required(dd.SiteStaff)

# class TaggingsByEntry(Taggings):
#     master_key = 'entry'
#     column_names = 'topic *'

# class TaggingsByTopic(Taggings):
#     master_key = 'topic'
#     column_names = 'entry *'
