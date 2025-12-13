# -*- coding: UTF-8 -*-
# Copyright 2024-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import requests
from bs4 import BeautifulSoup
from django.db import models

from lino import logger
from lino.api import dd, rt, _
from lino.core.roles import SiteAdmin
from lino.utils.html import format_html
from lino.core import constants
from lino.mixins import Referrable
from lino.mixins.human import Human, Born
from lino.mixins.sequenced import Sequenced, Hierarchical
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.comments.mixins import Commentable
from lino.modlib.publisher.mixins import Publishable
from lino.utils.mldbc.mixins import BabelDesignated
from lino_xl.lib.contacts.roles import ContactsStaff, ContactsUser
from .mixins import Copyrighted
from .choicelists import AuthorRoles

USER_AGENT = dd.get_plugin_setting('sources', 'user_agent', None)
TEST_REQUESTS = {
    'https://en.wikipedia.org/wiki/History_of_PDF': 'History of PDF - Wikipedia'}


class Source(Referrable, Hierarchical, Commentable, Publishable, Copyrighted):

    class Meta:
        app_label = 'sources'
        abstract = dd.is_abstract_model(__name__, 'Source')
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    memo_command = "src"

    url = models.URLField(_("URL"), blank=True)
    title = models.CharField(_("Title"), max_length=200, blank=True)
    author = dd.ForeignKey("sources.Author", blank=True, null=True)

    def __str__(self):
        if self.author is None:
            if self.title:
                s = self.title
            elif self.url:
                s = self.url
            else:
                s = super().__str__()
        else:
            s = "{0.title} by {0.author}".format(self)
        return s

    def full_clean(self):
        super().full_clean()
        if self.title or not self.url:
            return
        if USER_AGENT is None:
            self.title = TEST_REQUESTS.get(self.url, "")
        else:
            r = requests.get(self.url, headers={'user-agent': USER_AGENT})
            if r.status_code != 200:
                logger.info("Failed to fetch %s : %s", self.url, r)
                return
            soup = BeautifulSoup(r.content, 'lxml')
            if soup.title:
                self.title = soup.title.string
            else:
                self.title = "(no title)"
            logger.info("Online request succeeded: %s --> %s", self.url, self.title)


dd.update_field(Source, 'parent', verbose_name=_("Part of"))


class SourceRef(Controllable):

    class Meta:
        app_label = "sources"
        verbose_name = _("Source reference")
        verbose_name_plural = _("Source references")

    source = dd.ForeignKey('sources.Source')

    allow_cascaded_delete = ['owner']

    def get_str_words(self, ar):
        if not ar.is_obvious_field("source"):
            yield str(self.source)
        if not ar.is_obvious_field("owner"):
            yield str(self.owner)


class SourceRefs(dd.Table):
    model = "sources.SourceRef"


class SourcesByOwner(SourceRefs):
    master_key = "owner"
    default_display_modes = {
        None: constants.DISPLAY_MODE_LIST}


class Author(Human, Born):

    class Meta:
        app_label = 'sources'
        abstract = dd.is_abstract_model(__name__, 'Author')
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    death_date = dd.IncompleteDateField(
        blank=True, verbose_name=_("Death date"))
    birth_place = dd.ForeignKey("countries.Place",
                                verbose_name=_("Birth place"),
                                blank=True, null=True, related_name="authors_born")
    death_place = dd.ForeignKey("countries.Place",
                                verbose_name=_("Death place"),
                                blank=True, null=True, related_name="authors_died")

    def __str__(self):
        s = super().__str__()
        if self.birth_date:
            if self.death_date:
                s += " ({}—{})".format(self.birth_date, self.death_date)
            else:
                s += " (*{})".format(self.birth_date)
        elif self.death_date:
            s += " (†{})".format(self.birth_date)
        return s


class License(BabelDesignated, Referrable):

    class Meta:
        app_label = 'sources'
        abstract = dd.is_abstract_model(__name__, 'License')
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")

    url = models.URLField(_("URL"), blank=True)


class Sources(dd.Table):
    model = 'sources.Source'
    column_names = 'id title author url *'
    order_by = ['ref']

    insert_layout = """
    url
    title
    author
    """

    detail_layout = """
    url
    ref:10 title:60 id
    author  parent
    SourcesByParent uploads.UploadsBySource comments.CommentsByRFC
    """


class SourcesByParent(Sources):
    label = _("Parts")
    master_key = 'parent'
    column_names = 'title ref *'
    default_display_modes = {
        None: constants.DISPLAY_MODE_SUMMARY}


class SourcesByCopyrightOwner(Sources):
    master_key = 'copyright_owner'


class Licenses(dd.Table):
    model = 'sources.License'
    column_names = 'ref designation *'
    required_roles = dd.login_required(SiteAdmin)


class Authors(dd.Table):
    model = 'sources.Author'
    column_names = 'last_name first_name birth_date *'
    required_roles = dd.login_required(SiteAdmin)
    order_by = ['last_name', 'first_name', 'birth_date', 'id']
    detail_layout = """
    last_name first_name id
    birth_date birth_place
    death_date death_place
    CastsByAuthor
    """


AUTHOR_MODEL = dd.plugins.sources.author_model


class AuthorCast(Sequenced, Controllable):

    class Meta:
        app_label = "sources"
        verbose_name = _("Author cast")
        verbose_name_plural = _("Author casts")

    author = dd.ForeignKey(AUTHOR_MODEL)
    role = AuthorRoles.field()

    allow_cascaded_delete = ['owner']

    def __str__(self):
        return f"{self.author} as {self.role} for {self.owner}"

    def get_siblings(self):
        return self.__class__.objects.filter(
            owner_id=self.owner_id, owner_type=self.owner_type)

    def get_str_words(self, ar):
        if not ar.is_obvious_field("author"):
            yield str(self.author)
        if not ar.is_obvious_field("role"):
            yield _("as {role}").format(role=self.role)
        if not ar.is_obvious_field("owner"):
            yield _("for {owner}").format(owner=self.owner)

    def as_summary_item(self, ar, text=None, **kwargs):
        # raise Exception("20240613")
        if ar is None:
            obj = super()
        elif ar.is_obvious_field('author'):
            obj = self.owner
        elif ar.is_obvious_field('owner'):
            obj = self.author
        else:
            obj = super()
        if self.role is None or ar.is_obvious_field('role'):
            text = str(obj)
        else:
            text = "{} ({})".format(obj, self.role)
        return obj.as_summary_item(ar, text, **kwargs)


class AuthorCasts(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sources.AuthorCast'


class CastsByAuthor(AuthorCasts):
    master_key = 'author'
    required_roles = dd.login_required()
    column_names = "owner role *"
    # required_roles = dd.login_required(ContactsUser)
    # details_of_master_template = _("%(details)s")
    # insert_layout = """
    # song
    # role
    # """
    obvious_fields = {'author'}
    # default_display_modes = {  # temporary workaround
    #     None: constants.DISPLAY_MODE_SUMMARY}


class CastsByOwner(AuthorCasts):
    master_key = 'owner'
    required_roles = dd.login_required(ContactsUser)
    # details_of_master_template = _("%(details)s")
    insert_layout = """
    author
    role
    """
    obvious_fields = {'owner', 'role'}
    default_display_modes = {  # temporary workaround
        None: constants.DISPLAY_MODE_SUMMARY}


class AuthorsByOwner(CastsByOwner):
    label = _("Authors")
    known_values = dict(role=AuthorRoles.author)
    insert_layout = """
    author
    """


class ComposersByOwner(CastsByOwner):
    label = _("Composers")
    known_values = dict(role=AuthorRoles.composer)
    insert_layout = """
    author
    """


def authors_summary_by_role(page):
    tickets = set([pi.ticket for pi in page.items.all()])
    html = ""
    for role in AuthorRoles.get_list_items():
        authors = dict()
        for cast in AuthorCast.objects.filter(role=role):
            if cast.owner in tickets:
                lst = authors.setdefault(cast.author, [])
                lst.append(cast.owner)
        if len(authors):
            chunks = []
            for author, works in authors.items():
                chunks.append("{} ({})".format(
                    author, ", ".join([str(w) for w in works])))
            html += format_html("<p>{}: {} </p>", role, "; ".join(chunks))
        # else:
        #     html += format_html("<p>{} : nobody</p>", role)
    return html


def authors_summary(page, title):
    # tickets = set([pi.ticket for pi in page.items.all()])
    html = format_html("<h1>{}</h1>", title)
    for author in Author.objects.order_by('last_name', 'first_name'):
        seqnos = set([])
        for cast in AuthorCast.objects.filter(author=author):
            for pi in page.items.all():
                if cast.owner == pi.ticket:
                    seqnos.add(str(pi.seqno))
        if len(seqnos):
            seqnos = sorted(seqnos)
            atext = "{}, {}".format(author.last_name, author.first_name)
            html += format_html("<p>{}: {} </p>", atext, ", ".join(seqnos))
    return html


def copyright_summary(page, title):
    html = format_html("<h1>{}</h1>", title)
    Company = rt.models.contacts.Company
    for co in Company.objects.order_by('name'):
        seqnos = set([])
        for pi in page.items.all():
            if pi.ticket.copyright_owner == co:
                seqnos.add(str(pi.seqno))
        if len(seqnos):
            seqnos = sorted(seqnos)
            # cotext = str(co)
            cotext = ", ".join(co.get_address_lines())
            html += format_html("<p>{} : {}</p>", cotext, ", ".join(seqnos))
    return html
