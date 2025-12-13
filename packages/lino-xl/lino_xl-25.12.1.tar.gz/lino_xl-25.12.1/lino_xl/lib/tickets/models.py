# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.html import mark_safe, format_html, SafeString
from django.contrib.contenttypes.fields import GenericRelation
from lino.utils.html import E, tostring
from etgen.utils import join_elems, forcetext
from lino import mixins
from lino.api import dd, rt, _, pgettext, gettext
from lino.mixins.ref import Referrable
from lino.mixins.sequenced import Hierarchical
from lino.modlib.comments.mixins import Commentable
from lino.modlib.notify.choicelists import MessageTypes
from lino.modlib.memo.mixins import rich_text_to_elems, MemoReferrable
from lino.modlib.uploads.mixins import UploadController
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.users.mixins import Assignable
from lino.modlib.publisher.mixins import Publishable

from lino.modlib.users.mixins import PrivacyRelevant
from lino_xl.lib.skills.mixins import Feasible
from lino_xl.lib.stars.mixins import Starrable
# from lino_xl.lib.votes.choicelists import VoteStates
from lino_xl.lib.votes.mixins import Votable
from lino_xl.lib.working.choicelists import ReportingTypes
from lino_xl.lib.working.mixins import Workable
from .choicelists import TicketStates
from .roles import TicketsReader, Triager, TicketsStaff
from .ui import *


MessageTypes.add_item("tickets", dd.plugins.tickets.verbose_name)

# site_model = dd.plugins.tickets.site_model
milestone_model = dd.plugins.tickets.milestone_model
end_user_model = dd.plugins.tickets.end_user_model
order_model = dd.get_plugin_setting('invoicing', 'order_model', None)

# if dd.is_installed('tickets'):
#     site_model = dd.plugins.tickets.site_model
#     milestone_model = dd.plugins.tickets.milestone_model
# else:
#     site_model = None
#     milestone_model = None


class QuickAssignTo(dd.Action):
    """Quickly assign a ticket to another team member."""

    label = _("Assign to")
    icon_name = None
    show_in_toolbar = False
    no_params_window = True
    parameters = dict(
        assign_to=dd.ForeignKey("users.User"),
        comment=models.CharField(_("Comment"), max_length=200, blank=True),
    )

    params_layout = """
    assign_to
    comment
    """

    def get_action_permission(self, ar, obj, state):
        return not ar.get_user().is_anonymous

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        pv = ar.action_param_values
        obj.assigned_to = pv.assign_to
        obj.full_clean()
        obj.save()
        ar.success(refresh=True)
        ar.check_visibility()


class TimeInvestment(Commentable):
    class Meta:
        abstract = True

    closed = models.BooleanField(_("Closed"), default=False)

    planned_time = dd.DurationField(_("Planned time"), blank=True, null=True)

    # invested_time = models.TimeField(
    #     _("Invested time"), blank=True, null=True, editable=False)


# class ProjectType(mixins.BabelNamed):

#     class Meta:
#         app_label = 'tickets'
#         verbose_name = _("Project Type")
#         verbose_name_plural = _('Project Types')


class TicketType(mixins.BabelNamed):
    """The type of a :class:`Ticket`."""

    class Meta:
        app_label = "tickets"
        verbose_name = _("Ticket type")
        verbose_name_plural = _("Ticket types")

    reporting_type = ReportingTypes.field(blank=True)


# class Repository(UserAuthored):
#     class Meta:
#         verbose_name = _("Repository")
#         verbose_name_plural = _('Repositories')
#


# class CloseTicket(dd.Action):
#     #label = _("Close ticket")
#     label = "\u2611"
#     help_text = _("Mark this ticket as closed.")
#     show_in_workflow = True
#     show_in_toolbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is not None or obj.closed is not None:
#             return False
#         return super(CloseTicket, self).get_action_permission(ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         now = datetime.datetime.now()
#         for obj in ar.selected_rows:
#             obj.closed = now
#             obj.save()
#             ar.set_response(refresh=True)

# class StandbyTicket(dd.Action):
#     #label = _("Standby mode")
#     label = "\u2a37"
#     label = "\u2609"
#     help_text = _("Put this ticket into standby mode.")
#     show_in_workflow = True
#     show_in_toolbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is not None or obj.closed is not None:
#             return False
#         return super(StandbyTicket, self).get_action_permission(
#             ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         now = datetime.datetime.now()
#         for obj in ar.selected_rows:
#             obj.standby = now
#             obj.save()
#             ar.set_response(refresh=True)

# class ActivateTicket(dd.Action):
#     # label = _("Activate")
#     label = "☀"  # "\u2600"
#     help_text = _("Reactivate this ticket from standby mode or closed state.")
#     show_in_workflow = True
#     show_in_toolbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is None and obj.closed is None:
#             return False
#         return super(ActivateTicket, self).get_action_permission(
#             ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         for obj in ar.selected_rows:
#             obj.standby = False
#             obj.closed = False
#             obj.save()
#             ar.set_response(refresh=True)


class SpawnTicket(dd.Action):
    label = _("Spawn child ticket")
    sort_index = 12  # after ShowInsert and CloneRow
    # button_text = "◎"  # 25ce bullseye
    button_text = "⧉"  # U+29C9
    # label = "\u2611" "☑"
    # label = "⚇"  # "\u2687"
    # show_in_workflow = False
    # show_in_toolbar = False
    # goto_new = True
    params_layout = """
    ticket_summary
    """

    parameters = dict(
        ticket_summary=models.CharField(
            pgettext("Ticket", "Summary"), max_length=200, blank=False
        )
    )

    def run_from_ui(self, ar, **kw):
        pv = ar.action_param_values
        parent = ar.selected_rows[0]
        user = ar.get_user()
        child = rt.models.tickets.Ticket(
            user=user, summary=pv.ticket_summary, group=parent.group, parent=parent
        )
        child.full_clean()
        child.save_new_instance(ar)
        ar.goto_instance(child)
        ar.success()


class Ticket(
    UserAuthored,
    mixins.CreatedModified,
    TimeInvestment,
    Assignable,
    Hierarchical,
    Votable,
    Starrable,
    Workable,
    Feasible,
    UploadController,
    Referrable,
    MemoReferrable,
    Publishable,
    PrivacyRelevant
):
    quick_search_fields = "summary description ref"
    workflow_state_field = "state"
    create_session_on_create = True
    disable_author_assign = False
    memo_command = "ticket"
    manager_roles_required = dd.login_required(TicketsStaff)

    class Meta:
        app_label = "tickets"
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        abstract = dd.is_abstract_model(__name__, "Ticket")

    urgent = models.BooleanField(_("Urgent"), default=False)
    priority = models.IntegerField(
        _("Priority"), default=dd.plugins.tickets.default_priority)
    summary = models.CharField(
        pgettext("Ticket", "Summary"),
        max_length=200,
        blank=False,
        help_text=_("Short summary of the problem."),
    )
    description = dd.RichTextField(_("Description"), blank=True)
    upgrade_notes = dd.RichTextField(
        _("Resolution"), blank=True, format="plain")
    ticket_type = dd.ForeignKey("tickets.TicketType", blank=True, null=True)
    duplicate_of = dd.ForeignKey(
        "self",
        blank=True,
        null=True,
        verbose_name=_("Duplicate of"),
        related_name="duplicated_tickets",
    )
    end_user = dd.ForeignKey(
        end_user_model,
        verbose_name=_("End user"),
        blank=True,
        null=True,
        related_name="reported_tickets",
    )
    state = TicketStates.field(default="new")
    # rating = Ratings.field(blank=True)
    deadline = models.DateField(verbose_name=_(
        "Deadline"), blank=True, null=True)

    # deprecated fields:
    reported_for = dd.ForeignKey(
        milestone_model,
        related_name="tickets_reported",
        verbose_name="Reported for",
        blank=True,
        null=True,
        help_text=_("Milestone for which this ticket has been reported."),
    )
    fixed_for = dd.ForeignKey(  # no longer used since 20150814
        milestone_model,
        related_name="tickets_fixed",
        verbose_name="Fixed for",
        blank=True,
        null=True,
        help_text=_("The milestone for which this ticket has been fixed."),
    )
    reporter = dd.ForeignKey(
        settings.SITE.user_model, blank=True, null=True, verbose_name=_("Reporter")
    )
    waiting_for = models.CharField(
        _("Waiting for"), max_length=200, blank=True)
    feedback = models.BooleanField(_("Feedback"), default=False)
    standby = models.BooleanField(_("Standby"), default=False)

    spawn_ticket = SpawnTicket()  # "\u2687"

    fixed_since = models.DateTimeField(
        _("Fixed since"), blank=True, null=True, editable=False
    )
    last_commenter = dd.ForeignKey(
        settings.SITE.user_model,
        related_name="tickets_last_commter",
        verbose_name=_("Commented Last"),
        blank=True,
        null=True,
        help_text=_("Last user to make a comment"),
    )

    order = dd.ForeignKey(
        order_model,
        null=True, blank=True,
        related_name="tickets_by_order")

    comments = GenericRelation(
        "comments.Comment",
        content_type_field="owner_type",
        object_id_field="owner_id",
        related_query_name="ticket",
    )
    # needed by add_comments_filter()

    quick_assign_to_action = QuickAssignTo()
    edit_description = dd.ShowEditor("description")

    # def is_public(self):
    #     return not self.private

    @dd.displayfield(
        _("Assign to"),
        help_text=_(
            "Assign this ticket to another team member with a single click."),
    )
    def quick_assign_to(self, ar):
        if ar is None:
            return ""
        elems = []
        found_existing = False
        ba = ar.actor.get_action_by_name('quick_assign_to_action')
        if self.group:
            qs = self.group.members.all()
            qs = settings.SITE.user_model.filter_active_users(
                qs, dd.today(), prefix="user__"
            )
            for m in qs:
                kw = dict(action_param_values=dict(assign_to=m.user))
                u = m.user
                label = u.initials or u.username or str(u.pk)
                if m.user == self.assigned_to:
                    elems.append(label)
                    found_existing = True
                else:
                    elems.append(
                         ar.row_action_button(
                             self, ba, label=label, request_kwargs=kw)
                    )

        if self.assigned_to_id:
            elems.append(ar.row_action_button(self, ba, label=_("nobody"), request_kwargs={
                "action_param_values": {"assign_to": None}}))

        if self.assigned_to_id and not found_existing:
            u = self.assigned_to
            label = u.initials or u.username or str(u.pk)
            elems.append(label + "!")
            # ticket is assigned to a user who is not member of the team
        return E.span(*join_elems(elems, sep=", "))

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)
        user = ar.get_user()
        if not user.user_type.has_required_roles([TicketsReader]):
            return qs.none()
        q1 = Q(private=False, group__private=False)
        if user.is_anonymous:
            return qs.filter(q1)
        # if not user.user_type.has_required_roles([TicketsStaff]):
        #     q2 = Q(group__members__user=user)
        #     q3 = Q(user=user)
        #     qs = qs.filter(q1 | q2 | q3).distinct()
        return qs

    # @classmethod
    # def add_comments_filter(cls, qs, ar):
    #     tickets = cls.get_request_queryset(ar)
    #     return qs.filter(Q(ticket__isnull=True) | Q(ticket__in=tickets))
    #     # if tickets.exists():
    #     #     return qs.filter(Q(ticket__isnull=True) | Q(ticket__in=tickets))
    #     # return qs.filter(ticket__isnull=True)

    def on_create_comment(self, comment, ar):
        super().on_create_comment(comment, ar)
        comment.private = self.private
        if self.group:
            comment.group = self.group
            if self.group.private:
                comment.private = True

    def get_rfc_description(self, ar):
        html = ""
        _ = gettext
        if self.description:
            # html += tostring(E.b(_("Description")))
            html += ar.parse_memo(self.description)
        if self.upgrade_notes:
            html += tostring(E.b(_("Resolution"))) + ": "
            html += ar.parse_memo(self.upgrade_notes)
        if self.duplicate_of_id:
            html += tostring(_("Duplicate of")) + " "
            html += tostring(self.duplicate_of.as_summary_item(ar))
        return html

    def full_clean(self):
        if self.id and self.duplicate_of_id == self.id:
            self.duplicate_of = None
        # print "20150523b on_create", self.reporter
        # if not self.site_id:
        #     person = self.end_user or self.user.person
        #     if person is not None:
        #         qs = rt.models.tickets.Site.objects.filter(contact_person=person)
        #         qs = qs.filter(state=SiteStates.active)
        #         qs = qs.filter(Q(end_date__isnull=True) | Q(end_date__lte=dd.today()))
        #         qs = qs.order_by('-id')
        #         # qs = rt.models.tickets.Subscription.objects.filter(
        #         #     user=user, primary=True)
        #         if qs.count():
        #             # self.site = qs[0].site
        #             self.site = qs.first()
        super().full_clean()

    def on_create(self, ar):
        me = ar.get_user()
        self.order = me.current_order
        super().on_create(ar)

    def on_worked(self, session):
        """This is automatically called when a work session has been created
        or modified.

        """
        if self.fixed_since is None and session.is_fixing and session.end_time:
            self.fixed_since = session.get_datetime("end")

        self.touch()
        self.full_clean()
        self.save()

    def get_reporting_type(self):
        if self.ticket_type and self.ticket_type.reporting_type:
            return self.ticket_type.reporting_type
        # if t.order and t.order.reporting_type:
        #     return t.order.reporting_type
        # if t.project and t.project.reporting_type:
        #     return t.project.reporting_type
        return super().get_reporting_type()

    def memo2html(self, ar, text, **kwargs):
        # if txt:
        #     kwargs.update(title=txt)
        kwargs.update(title=text or self.summary)
        e = self.as_summary_item(ar, "#{}".format(self.pk), **kwargs)
        return tostring(e)
        # return ar.obj2str(self, "#{}".format(self.pk), **kwargs)

    def obj2memo(self, text=None):
        """Render the given database object as memo markup."""
        if self.memo_command is None:
            return "**{}**".format(self)
        return "[{} {}] ({})".format(self.memo_command, self.id, self.summary)

    # def get_memo_title(self):
    #     # don't show the ticket number in the title
    #     return self.summary

    def get_change_owner(self):
        # if self.site_id is not None:
        #     return self.group or self.site
        return self.group

    def get_comment_group(self):
        return self.group or super().get_comment_group()

    def on_commented(self, comment, ar, cw):
        """This is automatically called when a comment has been created"""
        self.last_commenter = comment.user
        self.touch()
        self.save()

    # def get_project_for_vote(self, vote):
    #     if self.project:
    #         return self.project
    #     qs = rt.models.tickets.Competence.objects.filter(user=vote.user)
    #     qs = qs.order_by('priority')
    #     if qs.count() > 0:
    #         return qs[0].project
    #     return rt.models.tickets.Project.objects.all()[0]

    def disabled_fields(self, ar):
        rv = super().disabled_fields(ar)
        # if self.project and not self.project.private:
        #     rv.add('private')
        if not ar.get_user().user_type.has_required_roles([Triager]):
            rv.add("user")
            # rv.add('fixed_since')
            # rv.add('fixed_date')
            # rv.add('fixed_time')
        return rv

    def __str__(self):
        # return "#" + str(self.id)
        return "#{0} ({1})".format(self.id, self.summary)

    # def get_choices_text(self, request, actor, field):
    #     return "#{0} ({1})".format(self.id, self.summary)

    def as_summary_item(self, ar, text=None, **kwargs):
        if ar is None:
            return "#{} ({})".format(self.id, self.summary)
        # if not 'title' in kwargs:
        #     kwargs.update(title=self.summary)
        kwargs.setdefault("title", self.summary)
        if text is None:
            text = "#{}".format(self.id)
        # if self.ref is not None:
        #     return ar.obj2html(self, "#{}".format(self.ref), *args, **kwargs)
        # return ar.obj2html(self, text, **kwargs)
        return super().as_summary_item(ar, text, **kwargs)

    # def as_summary_row(self, ar, **kwargs):
    #     if ar is None:
    #         return format_html("#{0} ({1})", self.id, self.summary)
    #     kwargs.update(title=self.summary)
    #     return ar.obj2htmls(self, mark_safe("#" + str(self.id)), **kwargs)

    def as_paragraph(self, ar, **kwargs):
        if ar is None:
            return str(self)
        # if self.nickname:
        #     return "#{0} ({1})".format(self.id, self.nickname)
        # return "#{0} ({1}) {2}".format(
        #     self.id, self.summary, self.state.button_text)
        # return "#{0} ({1})".format(self.id, self.summary)
        # num = str(self.id)
        lnk = ar.obj2htmls(self)
        more = []
        if self.priority > dd.plugins.tickets.default_priority \
                and not ar.is_obvious_field("priority"):
            more.append(format_html(
                ' <span class="l-text-prioritaire">{}</span>', self.priority))
        if self.user and not ar.is_obvious_field("user"):
            more.append(format_html(_("by {}"), ar.obj2htmls(self.user)))
        if self.group and not ar.is_obvious_field("group"):
            more.append(format_html(_("in {}"), ar.obj2htmls(self.group)))
        if self.assigned_to and not ar.is_obvious_field("assigned_to"):
            more.append(
                format_html(_("assigned to {}"),
                            ar.obj2htmls(self.assigned_to))
            )
        if len(more):
            # more = mark_safe(", ").join(more)
            more = mark_safe(" ".join(more))
            # assert isinstance(more, SafeString)  # temporary 20240506
            lnk = format_html("{} ({})", lnk, more)
        if ar.get_user().user_type.has_required_roles([Triager]):
            # lnk += " ⟶ " + tostring(self.get_workflow_buttons(ar))
            lnk += "<br/>" + tostring(self.get_workflow_buttons(ar))
            lnk = mark_safe(lnk)
        # assert isinstance(lnk, SafeString)  # temporary 20240506
        return lnk

    @dd.chooser()
    def reported_for_choices(cls, site):
        if not site:
            return []
        # return site.milestones_by_site.filter(reached__isnull=False)
        return site.milestones_by_site.all()

    @dd.chooser()
    def fixed_for_choices(cls, site):
        if not site:
            return []
        return site.milestones_by_site.all()

    # @profile
    def get_overview_elems(self, ar):
        """Overrides :meth:`lino.core.model.Model.get_overview_elems`."""
        if self.ref:
            txt = "{} {}".format(self.ref, self.summary)
        else:
            txt = self.summary
        ba = ar.actor.get_action_by_name('edit_description')
        if ba.get_row_permission(ar, self, None):
            yield E.h2(txt, " ", ar.row_action_button(self, ba))
        else:
            yield E.h2(txt)
        if self.description:
            for e in rich_text_to_elems(ar, self.description):
                yield e
        if self.upgrade_notes:
            yield E.b(_("Resolution") + ": ")
            for e in rich_text_to_elems(ar, self.upgrade_notes):
                yield e

        # elems = [ar.obj2html(self)]  # show full summary
        # # elems += [' ({})'.format(self.state.button_text)]
        # # elems += [' ', self.state.button_text, ' ']
        # if self.user and self.user != ar.get_user():
        #     elems += [' ', _(" by "), self.user.as_summary_item(ar)]
        # if self.end_user_id:
        #     elems += [' ', _("for"), ' ', self.end_user.as_summary_item(ar)]
        #
        # if dd.is_installed('votes'):
        #     qs = rt.models.votes.Vote.objects.filter(
        #         votable=self, state=VoteStates.assigned)
        #     if qs.count() > 0:
        #         elems += [', ', _("assigned to"), ' ']
        #         elems += join_elems(
        #             [vote.user.as_summary_item(ar) for vote in qs], sep=', ')
        # elif getattr(self, "assigned_to", None):
        #     elems += [", ", _("assigned to"), " ", self.assigned_to.as_summary_item(ar)]
        #
        # return E.p(*forcetext(elems))

    # def get_change_body(self, ar, cw):
    #     return tostring(E.p(
    #         _("{user} worked on [ticket {t}]").format(
    #             user=ar.get_user(), t=self.id)))

    def get_vote_raters(self):
        """ "Yield the
        :meth:`lino_xl.lib.votes.mixins.Votable.get_vote_raters` for
        this ticket.  This is the author and (if set) the
        :attr:`end_user`.

        """
        if self.user:
            yield self.user
        if issubclass(settings.SITE.user_model, dd.resolve_model(end_user_model)):
            if self.end_user:
                u = self.end_user.get_as_user()
                if u is not None:
                    yield u

    def is_workable_for(self, user):
        if self.standby or self.closed:
            return False
        if not self.state.active and not user.user_type.has_required_roles([Triager]):
            return False
        return True

    @classmethod
    def quick_search_filter(cls, search_text, prefix=""):
        """
        To skip mixins.Referrable quick_search_filter
        """
        return super().quick_search_filter(search_text, prefix)


Ticket.set_widget_options("priority", preferred_width=8, hide_sum=True)

# from django.contrib.contenttypes.fields import GenericRelation
# dd.inject_action('comments.Comment', ticket=GenericRelation(Ticket))

# dd.update_field(Ticket, 'user', verbose_name=_("Reporter"))


class CheckListItem(dd.Model):
    class Meta:
        app_label = "tickets"
        verbose_name = _("Check")
        verbose_name_plural = _("Checks")

    ticket = dd.ForeignKey("tickets.Ticket")
    details = dd.CharField(_("Todo details"), max_length=220)
    checked = dd.BooleanField(_("Finished"), default=False)


# dd.inject_field(
#     'users.User', 'project',
#     dd.ForeignKey(
#         'tickets.Project',
#         blank=True, null=True, related_name="users_by_project",
#         help_text=_("The project you are currently working on")))


@dd.receiver(dd.post_startup)
def setup_memo_commands(sender=None, **kwargs):
    # See :doc:`/specs/memo`

    if not sender.is_installed("memo"):
        return

    Ticket = sender.models.tickets.Ticket
    mp = sender.plugins.memo.parser

    mp.add_suggester(
        "#", Ticket.objects.order_by("id"), "id", value=lambda obj, _: str(obj)[1:]
    )


dd.inject_field(
    settings.SITE.user_model, 'current_order',
    dd.ForeignKey(
        order_model, related_name="current_users",
        verbose_name=_("Current order"),
        help_text=_("The invoicing order you have been working on recently."),
        blank=True, null=True))
