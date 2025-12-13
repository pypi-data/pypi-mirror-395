# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation

from lino.utils.html import format_html, tostring
from lino.api import dd, rt, _
from lino.mixins import BabelNamed, Referrable
from lino.modlib.comments.mixins import Commentable
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.notify.mixins import ChangeNotifier
from lino.modlib.checkdata.choicelists import Checker
from lino.core.roles import SiteAdmin, SiteUser  # , UserRole
from lino.core import constants
from lino.core.utils import dbfield2params_field
from lino.core.inject import inject_action
from lino.modlib.users.mixins import PrivacyRelevant


class Group(BabelNamed, Referrable, ChangeNotifier, Commentable):

    class Meta:
        app_label = 'groups'
        abstract = dd.is_abstract_model(__name__, 'Group')
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    memo_command = "group"

    description = dd.RichTextField(_("Description"), blank=True, format='plain')
    private = models.BooleanField(_("Private"), default=False)

    # comments = GenericRelation('comments.Comment',
    #                            content_type_field='owner_type',
    #                            object_id_field='owner_id',
    #                            related_query_name="group")
    # needed by get_request_queryset()

    @classmethod
    def setup_parameters(cls, fields):
        # Add the `user` filter parameter field.
        fields.setdefault('user',
                          dd.ForeignKey('users.User', blank=True, null=True))
        super().setup_parameters(fields)

    def on_create_comment(self, comment, ar):
        comment.group = self
        super().on_create_comment(comment, ar)

    def get_change_observers(self, ar=None):
        for x in super().get_change_observers(ar):
            yield x
        for mbr in self.members.all():
            yield (mbr.user, mbr.user.mail_mode)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)
        me = ar.get_user()
        if me.is_anonymous:
            return qs.none()
        if not me.user_type.has_required_roles([SiteAdmin]):
            # either a public group, or I am a member
            q1 = Q(private=False)
            q2 = Q(members__user=me)
            qs = qs.filter(q1 | q2).distinct()
        if (pv := ar.param_values) is None:
            return qs
        if pv.user:
            qs = qs.filter(Q(members__user=pv.user))
        return qs

    # @classmethod
    # def add_comments_filter(cls, qs, ar):
    #     groups = cls.get_request_queryset(ar)
    #     return qs.filter(Q(group=None) | Q(group__in=groups))
    #     # if groups.exists():
    #     #     return qs.filter(Q(group=None) | Q(group__in=groups))
    #     # return qs.filter(group=None)


class GroupDetail(dd.DetailLayout):
    main = """
    name
    ref:10 id private
    description MembershipsByGroup
    comments.CommentsByRFC
    """


class Groups(dd.Table):
    model = 'groups.Group'
    column_names = 'ref detail_link *'
    order_by = ['ref']
    required_roles = dd.login_required(SiteAdmin)

    insert_layout = """
    name
    ref private
    description
    """

    detail_layout = "groups.GroupDetail"


class MyGroups(My, Groups):
    # column_names = 'overview:10 recent_comments *'
    required_roles = dd.login_required(SiteUser)


class Membership(UserAuthored):

    class Meta:
        app_label = 'groups'
        abstract = dd.is_abstract_model(__name__, 'Membership')
        verbose_name = _("Group membership")
        verbose_name_plural = _("Group memberships")
        unique_together = ['user', 'group']

    group = dd.ForeignKey('groups.Group', related_name="members")
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    allow_cascaded_delete = ['user', 'group']

    def __str__(self):
        return _('{} in {}').format(self.user, self.group)


dd.update_field(Membership, "user", verbose_name=_("User"))


class Memberships(dd.Table):
    model = 'groups.Membership'
    required_roles = dd.login_required(SiteAdmin)
    insert_layout = dd.InsertLayout("""
    user
    group
    remark
    """, window_size=(60, 'auto'))

    detail_layout = dd.DetailLayout("""
    user
    group
    remark
    """, window_size=(60, 'auto'))


class MembershipsByGroup(Memberships):
    label = _("Memberships")
    master_key = 'group'
    column_names = "user remark workflow_buttons *"
    stay_in_grid = True
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

    # summary_sep = comma

    @classmethod
    def row_as_summary(cls, ar, obj, text=None, **kwargs):
        return obj.user.as_summary_item(ar, text, **kwargs)


class MembershipsByUser(Memberships):
    master_key = 'user'
    column_names = "group remark *"
    order_by = ['group__ref']
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    required_roles = dd.login_required(SiteUser)

    @classmethod
    def row_as_summary(cls, ar, obj, text=None, **kwargs):
        return obj.group.as_summary_item(ar, text, **kwargs)


class AllMemberships(Memberships):
    required_roles = dd.login_required(SiteAdmin)
    order_by = ['group', 'user']
    column_names = "group user remark *"


current_group = dd.ForeignKey(
        "groups.Group",
        related_name="current_users",
        verbose_name=_("Current group"),
        help_text=_("The group in which you have been working recently."),
        blank=True, null=True)

dd.inject_field(settings.SITE.user_model, 'current_group', current_group)


class SetCurrentGroup(dd.Action):
    label = _("Set my current group")
    # button_text = "▣"
    icon_name = None
    # show_in_toolbar = False
    params_layout = "current_group"

    def action_param_defaults(self, ar, obj, **kw):
        # Never gets called. An example for #6248 (Window actions should call
        # param_defaults())
        kw = super().action_param_defaults(ar, obj, **kw)
        obj = ar.get_user()
        kw.update(current_group=obj.current_group)
        print(f"20250803 param_defaults() returns {kw} {obj}")
        return kw

    def setup_parameters(cls, params):
        params.update(current_group=dbfield2params_field(current_group))

    def get_action_permission(self, ar, obj, state):
        return not ar.get_user().is_anonymous

    def run_from_ui(self, ar, **kw):
        obj = ar.get_user()
        pv = ar.action_param_values
        for k, v in pv.items():
            setattr(obj, k, v)
        obj.before_ui_save(ar, None)
        obj.full_clean()
        obj.save()
        ar.success(refresh=True)


inject_action('system.SiteConfig', set_current_group=SetCurrentGroup())


def welcome_messages(ar):
    me = ar.get_user()
    if me.current_group:
        # ia = settings.SITE.site_config.set_current_group
        # ba = rt.models.system.SiteConfigs.set_current_group
        # grp = tostring(ar.action_button(ba, None, text=str(me.current_group)))
        grp = me.current_group
        yield format_html(_("Member of {group}."), group=grp)


dd.add_welcome_handler(welcome_messages)


class GroupwiseChecker(Checker):
    model = PrivacyRelevant
    verbose_name = _("Check whether this belongs to the right group")

    def get_checkdata_problems(self, ar, obj, fix=False):
        grp = obj.get_default_group()
        if grp is None:
            return
        if grp.private and not obj.private:
            yield True, _("{} should be private").format(obj)
            if fix:
                obj.private = True
                obj.full_clean()
                obj.save()
        if obj.group != grp:
            yield True, _("{} should be {}").format(
                Group._meta.verbose_name, grp)
            if fix:
                obj.group = grp
                obj.full_clean()
                obj.save()
        # The following is *no* problem. The author may have left the group.
        # if obj.group_id and isinstance(obj, UserAuthored) and obj.user_id:
        #     qs = obj.group.members.filter(user=obj.user)
        #     if not qs.exists():
        #         yield False, _("{user} is not member of {group}").format(
        #             user=obj.user, group=obj.group)


GroupwiseChecker.activate()
