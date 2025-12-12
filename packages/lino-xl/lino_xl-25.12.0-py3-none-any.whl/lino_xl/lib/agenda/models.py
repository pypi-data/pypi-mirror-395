# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino.core.roles import SiteStaff
from lino.mixins.sequenced import Sequenced


class Item(Sequenced):

    class Meta:
        app_label = 'agenda'
        verbose_name = _("Agenda item")
        verbose_name_plural = _("Agenda items")

    meeting = dd.ForeignKey(dd.plugins.agenda.meeting_model,
                            related_name='items_by_meeting')
    topic = dd.ForeignKey(dd.plugins.agenda.topic_model,
                          related_name='items_by_topic')
    title = dd.CharField(_("Title"), max_length=200, blank=True)
    description = dd.RichTextField(_("Description"),
                                   blank=True,
                                   null=True,
                                   bleached=True)

    allow_cascaded_delete = ['meeting']

    def __str__(self):
        if self.meeting_id:
            return "{} {} in {}".format(self._meta.verbose_name, self.seqno, self.meeting)
        return super().__str__()

    def get_siblings(self):
        if self.meeting_id:
            return self.__class__.objects.filter(meeting=self.meeting)
        return self.__class__.objects.none()

    def full_clean(self):
        if not self.title and self.topic_id is not None:
            self.title = str(self.topic)
        super().full_clean()

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        yield 'meeting'
        yield 'topic'


class Items(dd.Table):
    model = 'agenda.Item'
    required_roles = dd.login_required(SiteStaff)

    insert_layout = """
    meeting
    topic
    title
    """

    detail_layout = dd.DetailLayout("""
    meeting seqno
    topic title
    description
    """)


class ItemsByMeeting(Items):
    required_roles = dd.login_required()
    master_key = 'meeting'
    column_names = 'seqno topic title *'


class ItemsByTopic(Items):
    required_roles = dd.login_required()
    master_key = 'topic'
    column_names = 'seqno meeting title *'
