# -*- coding: UTF-8 -*-
# Copyright 2011-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils.html import E
from lino.api import dd, rt, _
from django.db import models

# from lino.core.utils import comma
from lino.core.gfks import gfk2lookup
from lino.mixins import BabelNamed
from lino.mixins.ref import StructuredReferrable
from lino.utils import join_elems
from lino.utils.instantiator import create_row
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.publisher.mixins import Publishable
from lino.core import constants
from .roles import TopicsUser

partner_model = dd.get_plugin_setting("topics", "partner_model", None)


class Topic(StructuredReferrable, BabelNamed, Publishable):

    ref_max_length = 5

    class Meta:
        app_label = 'topics'
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        abstract = dd.is_abstract_model(__name__, 'Topic')

    # name = models.CharField(max_length=200, verbose_name=_("Designation"))
    description_text = dd.TextField(verbose_name=_("Long description"),
                                    blank=True,
                                    null=True)


class TopicDetail(dd.DetailLayout):

    main = """
    general1 general2
    """

    general1 = """
    name
    id ref
    description_text
    """

    general2 = """
    InterestsByTopic
    TagsByTopic
    """


class Topics(dd.Table):
    required_roles = dd.login_required(TopicsUser)
    model = 'topics.Topic'
    order_by = ["ref"]
    column_names = "ref name *"

    insert_layout = """
    ref
    name
    """

    detail_layout = "topics.TopicDetail"


class AllTopics(Topics):
    required_roles = dd.login_required(dd.SiteStaff)


class Tag(Controllable):

    class Meta:
        app_label = 'topics'
        verbose_name = _("Tag")
        verbose_name_plural = _('Tags')

    topic = dd.ForeignKey('topics.Topic', related_name='tags_by_topic')

    def __str__(self):
        return "Tag({}->{})".format(self.owner, self.topic)

    def as_summary_item(self, ar, *args, **kwargs):
        # link either to the owner or to the topic.
        if ar and ar.is_obvious_field('owner') and self.topic_id:
            return self.topic.as_summary_item(ar, *args, **kwargs)
        if self.owner:
            return self.owner.as_summary_item(ar, *args, **kwargs)
        return super().as_summary_item(ar, *args, **kwargs)


dd.update_field(Tag, 'owner', verbose_name=_("Owner"))


class Tags(dd.Table):
    required_roles = dd.login_required(dd.SiteStaff)
    model = 'topics.Tag'
    column_names = "topic owner *"


class TagsByOwner(Tags):
    required_roles = dd.login_required(TopicsUser)
    master_key = 'owner'
    order_by = ["topic"]
    column_names = 'topic *'
    # stay_in_grid = True
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    insert_layout = dd.InsertLayout("topic\n", window_size=(60, 'auto'))


class TagsByTopic(Tags):
    required_roles = dd.login_required(TopicsUser)
    master_key = 'topic'
    order_by = ["id"]
    column_names = 'owner *'
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    # details_of_master_template = _("%(details)s in %(master)s")
    label = _("Tagged by")


if partner_model is not None:

    class Interest(dd.Model):

        class Meta:
            app_label = 'topics'
            verbose_name = _("Interest")
            verbose_name_plural = _('Interests')

        allow_cascaded_delete = ["partner"]

        topic = dd.ForeignKey('topics.Topic', related_name='interests_by_topic')
        remark = dd.RichTextField(_("Remark"), blank=True, format="plain")
        partner = dd.ForeignKey(partner_model,
                                related_name='interests_by_partner',
                                blank=True,
                                null=True)

        def __str__(self):
            return "Interest({}->{})".format(self.partner, self.topic)

        def as_paragraph(self, ar, **kwargs):
            if ar.is_obvious_field('partner'):
                s = str(self.topic)
                if ar is None:
                    return s
                else:
                    return ar.obj2htmls(self, s)
            s = str(self.partner)
            if ar is None:
                return s
            else:
                return ar.obj2htmls(self, s)

    # dd.update_field(Interest, 'user', verbose_name=_("User"))

    class Interests(dd.Table):
        required_roles = dd.login_required(TopicsUser)
        model = 'topics.Interest'
        column_names = "partner topic *"
        default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
        insert_layout = """
            partner
            topic
            remark
            """
        detail_layout = dd.DetailLayout("""
            partner
            topic
            remark
            """,
                                        window_size=(60, 15))

    class AllInterests(Interests):
        required_roles = dd.login_required(dd.SiteStaff)
        default_display_modes = {None: constants.DISPLAY_MODE_GRID}
        stay_in_grid = True

    class InterestsByTopic(Interests):
        master_key = 'topic'
        order_by = ["id"]
        column_names = 'partner *'
        label = _("Interested partners")

    class InterestsByPartner(Interests):
        master_key = 'partner'
        order_by = ["topic"]
        column_names = 'topic *'
        label = _("Interested in")
        details_of_master_template = _("%(master)s is interested in")

        insert_layout = dd.InsertLayout("""
        topic
        remark
        """, window_size=(60, 10))


else:

    class InterestsByTopic(dd.Dummy):
        pass
