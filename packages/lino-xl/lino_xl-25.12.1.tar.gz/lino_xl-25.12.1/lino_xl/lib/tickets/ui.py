# -*- coding: UTF-8 -*-
# Copyright 2011-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.db.models import Q
from django.utils.text import format_lazy
from lino.utils.html import E, tostring
from lino import mixins
from lino.api import dd, rt, _, gettext
from lino.modlib.users.mixins import My
from lino.utils import join_elems

from lino.core.gfks import gfk2lookup

from lino_xl.lib.cal.mixins import daterange_text
from .choicelists import TicketEvents, TicketStates
# from .choicelists import LinkTypes
from .roles import TicketsReader, Reporter, Searcher, Triager, TicketsStaff
from lino.core import constants

# site_model = dd.plugins.tickets.site_model
milestone_model = dd.plugins.tickets.milestone_model
end_user_model = dd.plugins.tickets.end_user_model

# class ProjectTypes(dd.Table):
#     required_roles = dd.login_required(TicketsStaff)
#     model = 'tickets.ProjectType'
#     column_names = 'name *'
#     detail_layout = """id name
#     ProjectsByType
#     """


class TicketTypes(dd.Table):
    required_roles = dd.login_required(TicketsStaff)
    model = 'tickets.TicketType'
    column_names = 'name reporting_type *'
    detail_layout = """id name reporting_type
    TicketsByType
    """


# class ProjectDetail(dd.DetailLayout):
#     main = "general #deploy.DeploymentsByProject more"

#     general = dd.Panel("""
#     ref name
#     description #CompetencesByProject
#     """, label=_("General"))

#     more = dd.Panel("""
#     parent type reporting_type
#     company assign_to #contact_person #contact_role private closed
#     start_date end_date srcref_url_template changeset_url_template
#     ProjectsByParent #deploy.MilestonesByProject
#     # cal.EntriesByProject
#     """, label=_("More"))

# class Projects(dd.Table):
#     required_roles = dd.login_required(Reporter)
#     model = 'tickets.Project'
#     detail_layout = ProjectDetail()
#     column_names = "ref name parent company private *"
#     order_by = ["ref"]
#     parameters = mixins.ObservedDateRange(
#         observed_event=ProjectEvents.field(blank=True),
#         interesting_for=dd.ForeignKey(
#             'contacts.Partner',
#             verbose_name=_("Interesting for"),
#             blank=True, null=True,
#             help_text=_("Only projects interesting for this partner.")))
#     params_layout = """interesting_for start_date end_date observed_event"""

#     @classmethod
#     def get_request_queryset(self, ar):
#         qs = super(Projects, self).get_request_queryset(ar)
#         pv = ar.param_values

#         if pv.observed_event:
#             qs = pv.observed_event.add_filter(qs, pv)

#         if pv.interesting_for:
#             qs = qs.filter(
#                 Q(company=pv.interesting_for))

#         if False:  # pv.interesting_for:
#             qs = qs.filter(
#                 Q(tickets_by_project__site__partner=pv.interesting_for) |
#                 Q(tickets_by_project__site__partner__isnull=True))
#             interests = pv.interesting_for.interests_by_partner.values(
#                 'topic')
#             if len(interests) > 0:
#                 qs = qs.filter(
#                     tickets_by_project__topic__in=interests,
#                     tickets_by_project__private=False)
#         return qs

# class AllProjects(Projects):
#     required_roles = dd.login_required(TicketsStaff)

# class ActiveProjects(Projects):
#     """Show a list of active projects.

#     For an example, see :ref:`noi.specs.projects`.

#     """
#     label = _("Active projects")
#     column_names = 'ref name start_date activity_overview *'
#     required_roles = dd.login_required(Triager)

#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super(ActiveProjects, self).param_defaults(ar, **kw)
#         kw.update(start_date=dd.demo_date())
#         kw.update(end_date=dd.demo_date())
#         kw.update(observed_event=ProjectEvents.active)
#         return kw

# class ProjectsByParent(Projects):
#     master_key = 'parent'
#     label = _("Subprojects")
#     column_names = "ref name children_summary *"

# class TopLevelProjects(Projects):
#     label = _("Projects (tree)")
#     required_roles = dd.login_required(TicketsStaff)
#     column_names = 'ref name parent children_summary *'
#     filter = Q(parent__isnull=True)
#     variable_row_height = True

# class ProjectsByType(Projects):
#     master_key = 'type'
#     column_names = "ref name *"

# class Links(dd.Table):
#     model = 'tickets.Link'
#     required_roles = dd.login_required(TicketsStaff)
#     stay_in_grid = True
#     detail_layout = dd.DetailLayout("""
#     parent
#     type
#     child
#     """, window_size=(40, 'auto'))
#
#     insert_layout = """
#     parent
#     type
#     child
#     """
#

# class LinksByTicket(Links):
#     label = _("Dependencies")
#     required_roles = dd.login_required(Triager)
#     master = 'tickets.Ticket'
#     column_names = 'parent type_as_parent:10 child'
#     display_mode = ((None, constants.DISPLAY_MODE_SUMMARY),)
#
#     @classmethod
#     def get_request_queryset(self, ar):
#         mi = ar.master_instance  # a Person
#         if mi is None:
#             return
#         Link = rt.models.tickets.Link
#         flt = Q(parent=mi) | Q(child=mi)
#         return Link.objects.filter(flt).order_by(
#             'child__modified', 'parent__modified')
#
#     @classmethod
#     def get_table_summary(self, obj, ar):
#         """The :meth:`summary view <lino.core.actors.Actor.get_table_summary>`
#         for :class:`LinksByTicket`.
#
#         """
#         # if obj.pk is None:
#         #     return ''
#         #     raise Exception("20150218")
#         sar = self.request_from(ar, master_instance=obj)
#         links = []
#         for lnk in sar:
#             if lnk.parent is None or lnk.child is None:
#                 pass
#             else:
#                 if lnk.child_id == obj.id:
#                     i = (lnk.type.as_child(), lnk.parent)
#                 else:
#                     i = (lnk.type.as_parent(), lnk.child)
#                 links.append(i)
#
#         def by_age(a):
#             return a[1].modified
#
#         try:
#             links.sort(key=by_age)
#         # except AttributeError:
#         except (AttributeError, ValueError):
#             # AttributeError: 'str' object has no attribute 'as_date'
#             # possible when empty birth_date
#             # ValueError: day is out of range for month
#             pass
#
#         tbt = dict()  # tickets by lnktype
#         for lnktype, other in links:
#             lst = tbt.setdefault(lnktype, [])
#             # txt = "#%d" % other.id
#             lst.append(other.as_summary_item(ar))
#
#         items = []
#         for lnktype, lst in tbt.items():
#             items.append(E.li(str(lnktype), ": ", *join_elems(lst, ', ')))
#         elems = []
#         if len(items) > 0:
#             # elems += join_elems(items)
#             # elems.append(l(*items))
#             elems.append(E.ul(*items))
#         # else:
#         #     elems.append(_("No dependencies."))
#
#         # Buttons for creating relationships:
#
#         sar = obj.spawn_ticket.request_from(ar)
#         if ar.renderer.is_interactive and sar.get_permission():
#             btn = sar.ar2button(obj)
#             elems += [E.br(), btn]
#
#         if self.insert_action is not None and ar.renderer.is_interactive:
#             sar = self.insert_action.request_from(ar)
#             if sar.get_permission():
#                 actions = []
#                 for lt in LinkTypes.objects():
#                     actions.append(E.br())
#                     sar.known_values.update(type=lt, parent=obj)
#                     sar.known_values.pop('child', None)
#                     sar.clear_cached_status()
#                     btn = sar.ar2button(None, lt.as_parent(), icon_name=None)
#                     if not lt.symmetric:
#                         # actions.append('/')
#                         sar.known_values.update(type=lt, child=obj)
#                         sar.known_values.pop('parent', None)
#                         sar.clear_cached_status()
#                         btn2 = sar.ar2button(None, lt.as_child(), icon_name=None)
#                         # actions.append(btn)
#                         btn = E.span(btn, '/', btn2)
#                     actions.append(btn)
#                     # actions.append(' ')
#                 # actions = join_elems(actions, E.br)
#
#                 if len(actions) > 0:
#                     elems += [E.br(), gettext("Create dependency as ")] + actions
#         return E.div(*elems)


class TicketDetail(dd.DetailLayout):
    main = "general more #history_tab"

    general = dd.Panel("""
    general1 #WishesByTicket
    comments.CommentsByRFC:60 #working.SessionsByTicket:20
    """,
                       label=_("General"))

    # history_tab = dd.Panel("""
    # changes.ChangesByMaster:50 #stars.StarsByController:20
    # """, label=_("History"), required_roles=dd.login_required(Triager))

    general1 = """
    summary:40 id:6 user:12 end_user:12
    order #topic #project private
    workflow_buttons #assigned_to waiting_for
    """

    more = dd.Panel("""
    more1 DuplicatesByTicket:20
    description:40 upgrade_notes:20 #LinksByTicket:20
    """,
                    label=_("More"))

    more1 = """
    #nickname:10     created modified reported_for #fixed_for ticket_type:10
    state ref duplicate_of planned_time priority
    # standby feedback closed
    """


class Tickets(dd.Table):
    required_roles = dd.login_required(Searcher)
    # label = _("All tickets")
    # required_roles = set()  # also for anonymous
    model = 'tickets.Ticket'
    order_by = ["-id"]
    focus_on_quick_search = True
    default_display_modes = {
        70: constants.DISPLAY_MODE_SUMMARY,
        None: constants.DISPLAY_MODE_LIST
    }
    column_names = 'id summary:50 user:10 #topic #faculty ' \
                   'workflow_buttons:30 #site:10 #project:10 *'  # Site commented to not disturbe care
    detail_layout = 'tickets.TicketDetail'
    insert_layout = """
    summary
    end_user
    """
    # card_layout = dd.Panel(
    #     """summary user
    #     workflow_buttons
    #     comments.CommentsByRFC""", label=_("Cards"))
    card_layout = """summary user
        order priority
        workflow_buttons
        """
    # list_layout = """summary user workflow_buttons"""

    # insert_layout = dd.InsertLayout("""
    # # reporter #product
    # summary
    # description
    # """, window_size=(70, 20))

    detail_html_template = "tickets/Ticket/detail.html"

    parameters = mixins.ObservedDateRange(
        observed_event=TicketEvents.field(blank=True),
        # topic=dd.ForeignKey('topics.Topic', blank=True, ),
        end_user=dd.ForeignKey(
            end_user_model,
            verbose_name=_("End user"),
            blank=True,
            null=True,
            help_text=_("Only rows concerning this end user.")),
        assigned_to=dd.ForeignKey(
            # end_user_model,
            settings.SITE.user_model,
            verbose_name=_("Assigned to"),
            blank=True,
            null=True,
            help_text=_("Only tickets with this user assigned.")),
        not_assigned_to=dd.ForeignKey(
            # end_user_model,
            settings.SITE.user_model,
            verbose_name=_("Not assigned to"),
            blank=True,
            null=True,
            help_text=_("Only that this user is not assigned to.")),
        interesting_for=dd.ForeignKey(
            'contacts.Company',
            verbose_name=_("Interesting for"),
            blank=True,
            null=True,
            help_text=_("Only tickets interesting for this partner.")),
        deployed_to=dd.ForeignKey(milestone_model, blank=True, null=True),
        # project=dd.ForeignKey(
        #     'tickets.Project',
        #     blank=True, null=True),
        state=TicketStates.field(blank=True,
                                 help_text=_("Only rows having this state.")),
        # priority=Priorities.field(_("Priority"),
        #                           blank=True,
        #                           help_text=_("Only rows having this priority.")),
        show_assigned=dd.YesNo.field(_("Assigned"), blank=True),
        show_deployed=dd.YesNo.field(_("Deployed"),
                                     blank=True,
                                     help_text=_(
                                         "Whether to show tickets with at "
                                         "least one deployment")),
        show_active=dd.YesNo.field(_("Active"), blank=True),
        show_todo=dd.YesNo.field(_("To do"), blank=True),
        show_private=dd.YesNo.field(_("Private"), blank=True),
        has_ref=dd.YesNo.field(_("Has reference"), blank=True),
        last_commenter=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Commented Last"),
            blank=True,
            null=True,
            help_text=_("Only tickets that have this use commenting last.")),
        not_last_commenter=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Not Commented Last"),
            blank=True,
            null=True,
            help_text=_(
                "Only tickets where this use is not the last commenter.")))

    params_layout = """
    user end_user assigned_to not_assigned_to interesting_for order state #priority deployed_to
    show_assigned show_active show_deployed show_todo show_private
    start_date end_date observed_event #topic has_ref"""

    # simple_parameters = ('reporter', 'assigned_to', 'state', 'project')

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        yield 'end_user'
        yield 'state'
        # yield 'project'
        # yield 'topic'
        yield 'order'
        # yield 'priority'
        yield 'last_commenter'
        # if not dd.is_installed('votes'):
        #     yield 'assigned_to'

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)

        if (pv := ar.param_values) is None:
            return qs

        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)

        if pv.interesting_for:
            qs = qs.filter(Q(order__partner=pv.interesting_for))

        if dd.get_plugin_setting('votes', "with_candidatures", False):
            if pv.assigned_to:
                # qs = qs.filter(
                #     Q(votes_by_ticket__user=pv.assigned_to) |
                #     Q(votes_by_ticket__end_user=pv.assigned_to)).distinct()
                qs = qs.filter(votes_by_ticket__user=pv.assigned_to).distinct()

            if pv.not_assigned_to:
                # print(20170318, self, qs.model, pv.not_assigned_to)
                # qs = qs.exclude(
                #     Q(votes_by_ticket__user_id=pv.not_assigned_to.id) |
                #     Q(votes_by_ticket__end_user_id=pv.not_assigned_to.id))
                qs = qs.exclude(votes_by_ticket__user=pv.not_assigned_to)
            if pv.show_assigned == dd.YesNo.no:
                qs = qs.filter(vote__isnull=False).distinct()
            elif pv.show_assigned == dd.YesNo.yes:
                qs = qs.filter(vote__isnull=True).distinct()

        else:
            # NB: assigned_to gets handled by super because it is a simple
            # parameter field
            if pv.not_assigned_to:
                qs = qs.exclude(assigned_to=pv.not_assigned_to)

            if pv.show_assigned == dd.YesNo.no:
                qs = qs.filter(assigned_to__isnull=True)
            elif pv.show_assigned == dd.YesNo.yes:
                qs = qs.filter(assigned_to__isnull=False)

        if pv.deployed_to:
            # qs = qs.filter(
            #     Q(votes_by_ticket__user=pv.assigned_to) |
            #     Q(votes_by_ticket__end_user=pv.assigned_to)).distinct()
            qs = qs.filter(
                deployments_by_ticket__milestone=pv.deployed_to).distinct()
        if pv.show_deployed == dd.YesNo.no:
            qs = qs.exclude(deployments_by_ticket__isnull=False)
        elif pv.show_deployed == dd.YesNo.yes:
            qs = qs.filter(deployments_by_ticket__isnull=False)

        active_states = TicketStates.filter(active=True)
        if pv.show_active == dd.YesNo.no:
            qs = qs.exclude(state__in=active_states)
        elif pv.show_active == dd.YesNo.yes:
            qs = qs.filter(state__in=active_states)

        todo_states = TicketStates.filter(show_in_todo=True)
        if pv.show_todo == dd.YesNo.no:
            qs = qs.exclude(state__in=todo_states)
        elif pv.show_todo == dd.YesNo.yes:
            qs = qs.filter(state__in=todo_states)

        # if pv.has_site == dd.YesNo.no:
        #     qs = qs.filter(site__isnull=True)
        # elif pv.has_site == dd.YesNo.yes:
        #     qs = qs.filter(site__isnull=False)

        # if pv.show_standby == dd.YesNo.no:
        #     qs = qs.filter(standby=False)
        # elif pv.show_standby == dd.YesNo.yes:
        #     qs = qs.filter(standby=True)

        if pv.show_private == dd.YesNo.no:
            qs = qs.filter(private=False)
        elif pv.show_private == dd.YesNo.yes:
            qs = qs.filter(private=True)

        if pv.has_ref == dd.YesNo.yes:
            qs = qs.filter(ref__isnull=False)
        elif pv.has_ref == dd.YesNo.no:
            qs = qs.filter(ref__isnull=True)
        # print 20150512, qs.query
        # 1253

        # the following caused a RuntimeWarning and was useless since
        # the same filter is applied by
        # pv.observed_event.add_filter(qs, pv) above: if
        # pv.start_date: qs = qs.filter(created__gte=pv.start_date) if
        # pv.end_date: qs = qs.filter(created__lte=pv.end_date)

        if pv.not_last_commenter:
            qs = qs.exclude(last_commenter=pv.not_last_commenter)

        qs = qs.select_related(
            'user',
            'assigned_to',  # 'project',
            'duplicate_of',
            'end_user')

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super().get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.start_date or pv.end_date:
            yield daterange_text(pv.start_date, pv.end_date)


class AllTickets(Tickets):
    label = _("All tickets")
    use_paging = True


class DuplicatesByTicket(Tickets):
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    label = _("Duplicates")
    master_key = 'duplicate_of'
    column_names = "detail_link state *"
    editable = False
    required_roles = set([])


class RefTickets(Tickets):
    label = _("Reference Tickets")
    required_roles = dd.login_required(Triager)

    column_names = 'ref:20 summary:50 workflow_buttons:30 id user:10 *'
    order_by = ["ref"]

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(has_ref=dd.YesNo.yes)
        return kw


class UnassignedTickets(Tickets):
    if dd.is_installed('votes'):
        column_names = "summary order user votes_by_ticket *"
    else:
        column_names = "detail_link order quick_assign_to *"

    label = _("Unassigned Tickets")
    required_roles = dd.login_required(Triager)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(show_assigned=dd.YesNo.no)
        # kw.update(show_private=dd.YesNo.no)
        # kw.update(show_active=dd.YesNo.yes)
        # kw.update(show_closed=dd.YesNo.no)
        kw.update(state=TicketStates.opened)
        return kw


class TicketsByEndUser(Tickets):
    master_key = 'end_user'
    column_names = ("id summary:50 group workflow_buttons * ")
    # display_mode = ((None, constants.DISPLAY_MODE_SUMMARY),)
    required_roles = dd.login_required((TicketsReader, Triager))
    details_of_master_template = _("%(details)s of end user %(master)s")
    params_layout = """
    user assigned_to not_assigned_to interesting_for order state deployed_to
    show_assigned show_active show_deployed show_todo show_private
    start_date end_date observed_event has_ref"""

    @classmethod
    def table_as_summary(self, ar):
        """The :meth:`summary view <lino.core.actors.Actor.get_table_summary>`
        for this table.

        """
        chunks = []
        items = [o.as_summary_item(ar) for o in ar]
        if len(items) > 0:
            chunks += join_elems(items, ", ")

        sar = self.insert_action.create_request(parent=ar)
        if sar.get_permission():
            chunks.append(sar.ar2button())

        return tostring(chunks)


class TicketsByType(Tickets):
    master_key = 'ticket_type'
    column_names = "summary state  *"


class PublicTickets(Tickets):
    label = _("Public tickets")
    order_by = ["-id"]
    column_names = 'detail_link:50 ticket_type:10 *'

    # filter = Q(assigned_to=None)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        # kw.update(show_assigned=dd.YesNo.no)
        kw.update(show_private=dd.YesNo.no)
        # kw.update(show_active=dd.YesNo.yes)
        # kw.update(show_closed=dd.YesNo.no)
        kw.update(state=TicketStates.opened)
        return kw


class TicketsToTriage(Tickets):
    label = _("Tickets to triage")
    required_roles = dd.login_required(Triager)
    button_label = _("Triage")
    order_by = ("-priority", "-id")
    column_names = 'detail_link:50 priority ' \
                   'quick_assign_to:20 ticket_type:10 *'
    params_panel_hidden = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(state=TicketStates.new)
        return kw

    welcome_message_when_count = 0


class TicketsToTalk(Tickets):
    label = _("Tickets to talk")
    required_roles = dd.login_required(Triager)
    order_by = ["-priority", "-deadline", "-id"]
    # order_by = ["-id"]
    column_names = "detail_link:50 priority #deadline waiting_for " \
                   "workflow_buttons:40 *"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(state=TicketStates.talk)
        return kw


# class TicketsNeedingMyFeedback(TicketsToTalk):
#     label = _("Tickets needing my feedback")
#     column_names = "detail_link:50 priority #deadline last_commenter " \
#                    "workflow_buttons:40 *"
#
#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super().param_defaults(ar, **kw)
#         kw.update(not_last_commenter=ar.get_user())
#         return kw
#

# class MyTicketsNeedingFeedback(TicketsNeedingMyFeedback):
#     label = _("My tickets needing feedback")
#     column_names = "detail_link:50 priority #deadline " \
#                    "workflow_buttons:40 *"
#
#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super().param_defaults(ar, **kw)
#         kw.update(last_commenter=ar.get_user(), not_last_commenter=None)
#         return kw
#

class ActiveTickets(Tickets):
    label = _("Active tickets")
    required_roles = dd.login_required(Triager)
    order_by = ["-id"]
    # order_by = ["-modified", "id"]
    column_names = 'detail_link:50 priority order ' \
                   'assigned_to:10 ticket_type:10 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(show_active=dd.YesNo.yes)
        # kw.update(show_closed=dd.YesNo.no)
        # kw.update(show_standby=dd.YesNo.no)
        return kw


class MyTickets(My, Tickets):
    # label = _("My tickets")
    required_roles = dd.login_required(Reporter)
    order_by = ["-priority", "-id"]
    column_names = "priority detail_link assigned_to #planned_time workflow_buttons *"
    params_panel_hidden = True
    # params_layout = """
    # user end_user site #project state #priority
    # start_date end_date observed_event #topic #feasable_by show_active"""
    params_layout = """
    end_user
    order
    state
    start_date
    end_date
    observed_event
    show_active
    user
    """
    params_panel_pos = "left"

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(show_active=dd.YesNo.yes)
        # kw.update(show_closed=dd.YesNo.no)
        # kw.update(show_standby=dd.YesNo.no)
        return kw


class MyTicketsToWork(Tickets):
    label = _("Tickets to work")
    order_by = ["-priority", "-modified"]
    required_roles = dd.login_required(Reporter)
    column_names = 'priority detail_link:50 workflow_buttons:30 *'
    params_layout = """
    user end_user order assigned_to #project state
    start_date end_date observed_event #topic show_active"""
    params_panel_hidden = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(show_active=dd.YesNo.yes)
        # kw.update(show_todo=dd.YesNo.yes)
        kw.update(assigned_to=ar.get_user())
        return kw


# class TicketsBySite(Tickets):
#     required_roles = dd.login_required(Reporter)
#     # label = _("Known problems")
#     master_key = 'site'
#     column_names = "priority detail_link:50 ticket_type workflow_buttons *"
#     order_by = ["-priority", "-id"]
#
#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super().param_defaults(ar, **kw)
#         kw.update(show_active=dd.YesNo.yes)
#         return kw


class TicketsByGroup(Tickets):
    abstract = not dd.is_installed('groups')
    master_key = 'group'
    order_by = ["-priority", "-id"]
    column_names = 'priority id summary:50 workflow_buttons:30 *'

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(show_active=dd.YesNo.yes)
        return kw


class TicketsByOrder(Tickets):
    required_roles = dd.login_required(Reporter)
    master_key = 'order'
    column_names = "priority detail_link:50 ticket_type workflow_buttons *"
    order_by = ["-priority", "-id"]

    @classmethod
    def param_defaults(self, ar, **kw):
        # mi = ar.master_instance
        kw = super().param_defaults(ar, **kw)
        kw.update(show_active=dd.YesNo.yes)
        # kw.update(interesting_for=mi.partner)
        # kw.update(end_date=dd.today())
        # kw.update(observed_event=TicketEvents.todo)
        return kw


# class SiteDetail(dd.DetailLayout):
#     main = """general #meetings.MeetingsBySite"""
#     general = dd.Panel("""
#     id name
#     reporting_type workflow_buttons
#     remark
#     bottom""",
#                        label=_("General"))
#     bottom = """
#     bottom_left:30 TicketsBySite
#     """
#     bottom_left = """
#     description
#     """
#
#
# class Sites(dd.Table):
#     # required_roles = set()  # also for anonymous
#     required_roles = dd.login_required(Reporter)
#     model = 'tickets.Site'
#     column_names = "ref name remark workflow_buttons id *"
#     order_by = ['ref', 'name']
#     # detail_html_template = "tickets/Site/detail.html"
#     parameters = dd.ParameterPanel(
#         watcher=dd.ForeignKey('users.User', blank=True, null=True),
#         show_exposed=dd.YesNo.field(
#             _("Exposed"),
#             blank=True,
#             help_text=_("Whether to show rows in an exposed state")),
#         state=SiteStates.field(blank=True),
#     )
#
#     insert_layout = """
#     name ref
#     remark
#     # description
#     """
#     detail_layout = 'tickets.SiteDetail'
#     params_layout = """watcher state show_exposed"""
#
#     @classmethod
#     def get_title_tags(self, ar):
#         for t in super().get_title_tags(ar):
#             yield t
#
#         pv = ar.param_values
#         if pv.show_exposed:
#             yield format_lazy(_("{}: {}"), _("Exposed"), pv.show_exposed)
#
#     @classmethod
#     def get_request_queryset(self, ar):
#         qs = super().get_request_queryset(ar)
#         if isinstance(qs, list):
#             return qs
#
#         if (pv := ar.param_values) is None: return qs
#         if pv.watcher:
#             if dd.is_installed("groups"):
#                 groups = rt.models.groups.Membership.objects.filter(
#                     user=pv.watcher).values_list('group', flat=True)
#                 qs = qs.filter(group__in=groups)
#             # sqs = rt.models.tickets.Subscription.objects.filter(user=pv.watcher)
#             # subscribed_sites = sqs.values_list('site')
#             # qs = qs.filter(pk__in=subscribed_sites)
#         qs = self.model.add_param_filter(qs, show_exposed=pv.show_exposed)
#
#         return qs
#
#
# # def get_summary_columns():
# #     for ts in TicketStates.get_list_items():
# #         if ts.active:
# #             k = ts.get_summary_field()
# #             if k is not None:
# #                 yield k
#
#
# class SitesByGroup(Sites):
#     master_key = 'group'
#     column_names = "detail_link parsed_description workflow_buttons *"
#
#
# class MySites(Sites):
#     label = _("My projects")
#     column_names = "detail_link parsed_description workflow_buttons *"
#
#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super().param_defaults(ar, **kw)
#         kw.update(watcher=ar.get_user())
#         kw.update(show_exposed=dd.YesNo.yes)
#         return kw
#
#     # @classmethod
#     # def setup_columns(cls):
#     #     cls.column_names = "overview "
#     #     cls.column_names += ' '.join(get_summary_columns())
#

# class SitesOverview(MySites):
#     label = _("Sites Overview")

# @classmethod
# def param_defaults(self, ar, **kw):
#     kw = super(MySitesDashboard, self).param_defaults(ar, **kw)
#     if ar.get_user().user_type.has_required_roles([TicketsStaff]):
#         kw['watcher'] = None
#     return kw


# class AllSites(Sites):
#     required_roles = dd.login_required(TicketsStaff)


# # List of sites that user X has stared?
# class SitesByPartner(Sites):
#     master_key = 'partner'
#     column_names = "name remark *"

# class SitesByCompany(Sites):
#     master_key = 'company'
#     column_names = "ref name workflow_buttons *"
#
#
# class SitesByPerson(Sites):
#     master_key = 'contact_person'
#     column_names = "ref name *"


class CheckListItems(dd.Table):
    model = "tickets.CheckListItem"
    column_names = "ticket details checked"


class CheckListItemsByTicket(CheckListItems):
    master_key = "ticket"
    column_names = "details checked"
