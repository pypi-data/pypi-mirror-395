# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime as dt
from copy import copy
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.html import format_html

from lino import mixins
from lino.api import dd, rt, _, gettext
from lino.modlib.checkdata.choicelists import Checker
from lino.utils.html import E, tostring
from lino.utils.format_date import fds, fts
from lino.utils.quantities import Duration, ZERO_DURATION
from lino.mixins.periods import DateRange, Started, Ended
from lino.mixins.sequenced import Sequenced
from lino.modlib.system.choicelists import YesNo
from lino.modlib.linod.choicelists import background_task
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.summaries.mixins import DateSummarized, SlaveSummarized
from lino.modlib.about.choicelists import TimeZones

# from lino_xl.lib.excerpts.mixins import Certifiable
# from lino_xl.lib.contacts.mixins import ContactRelated
# from lino_xl.lib.tickets.choicelists import TicketStates
from lino_xl.lib.tickets.roles import Triager
from lino_xl.lib.invoicing.mixins import InvoiceGenerator
from lino_xl.lib.calview.mixins import CalendarViewable

from .actions import EndThisSession, EndTicketSession
from .mixins import SummarizedFromSession
from .choicelists import ReportingTypes
from .ui import *


class SessionType(mixins.BabelNamed):

    class Meta:
        app_label = 'working'
        verbose_name = _("Session Type")
        verbose_name_plural = _('Session Types')


# class Location(mixins.BabelDesignated):

#     class Meta:
#         app_label = 'working'
#         verbose_name = _("Location")
#         verbose_name_plural = _('Locations')

#     time_zone = dd.ForeignKey(
#         dd.plugins.working.ticket_model,
#         related_name="sessions_by_ticket")


class Session(UserAuthored, Started, Ended, InvoiceGenerator, CalendarViewable):

    class Meta:
        app_label = 'working'
        verbose_name = _("Working session")
        verbose_name_plural = _('Working sessions')
        abstract = dd.is_abstract_model(__name__, 'Session')

    # target_invoicing_area = 'reporting'
    target_voucher_model = "storage.DeliveryNote"

    ticket = dd.ForeignKey(
        dd.plugins.working.ticket_model,
        # blank=True, null=True,
        related_name="sessions_by_ticket")

    session_type = dd.ForeignKey('working.SessionType', null=True, blank=True)
    summary = models.CharField(_("Summary"),
                               max_length=200,
                               blank=True,
                               help_text=_("Summary of the session."))
    description = dd.RichTextField(_("Description"), blank=True)
    # break_time = models.TimeField(
    #     blank=True, null=True,
    #     verbose_name=_("Break Time"))
    break_time = dd.DurationField(_("Break Time"), blank=True, null=True)
    computed_duration = dd.DurationField(_("Computed duration"),
                                         blank=True,
                                         null=True,
                                         editable=False)
    faculty = dd.ForeignKey('skills.Skill',
                            related_name="sessions_by_faculty",
                            blank=True,
                            null=True)

    reporting_type = ReportingTypes.field(blank=True)

    is_fixing = models.BooleanField(_("Fixing"), default=False)
    if settings.USE_TZ:
        time_zone = TimeZones.field()
    else:
        time_zone = dd.DummyField()

    end_session = EndThisSession()
    # show_today = ShowMySessionsByDay('start_date')
    # print_activity_report = PrintActivityReport()

    def when_text(self):
        if self.start_time and self.end_time:
            if self.end_date is None or self.start_date == self.end_date:
                return "%s %s-%s" % (fds(self.start_date),
                                     fts(self.start_time),
                                     fts(self.end_time))
            else:
                return "%s %s-%s %s" % (
                    fds(self.start_date), fts(self.start_time),
                    fds(self.end_date), fts(self.end_time))
        elif self.start_time:
            return "%s %s" % (
                fds(self.start_date),
                fts(self.start_time))
        elif self.start_date:
            return fds(self.start_date)

    def __str__(self):
        if (when := self.when_text()) is None:
            # return "%s # %s" % (self._meta.verbose_name, self.pk)
            return super().__str__()
        kw = dict(user=self.user.initials or self.user, when=when)
        if self.ticket is None:
            tpl = "{user} {when}"
        else:
            tpl = "{when} {user} {what}"
            kw.update(what="#" + str(self.ticket.id))
        # tpl = _("{user} working {when} on {what}")
        return tpl.format(**kw)
        # return "%s # %s" % (self._meta.verbose_name, self.pk)

    # def as_str(self, ar):
    #     return tostring(self.as_summary_item(ar))

    def get_event_summary(self, ar):
        # yield "barbaz"
        # yield str(ar.param_values)
        # yield self.as_summary_item(ar)
        if (u := self.user) is not None:
            yield " " + (u.initials or str(u))
        if (t := self.ticket) is not None:
            yield " " + str(t)

    def as_summary_item(self, ar, text=None, **kwargs):

        # In MySessionsByDay, start_date isn't strictly speaking an obvious
        # field, it is "obvious" only when it's a same-day session and when
        # start_date  is the same as the start_date set in param_values.

        if text is None:
            text = fts(self.start_time)
            if self.end_time is not None:
                text += "-" + fts(self.end_time)
            if ar is not None:
                pv = ar.param_values
                if pv is None or pv.start_date != self.start_date \
                        or pv.end_date != self.start_date:
                    # if not ar.is_obvious_field('start_date'):
                    text = fds(self.start_date) + " " + text
                u = self.user
                if pv is None or pv.user != u:
                    # if not ar.is_obvious_field('user'):
                    text += " " + u.nickname or u.initials or str(u)
                if not ar.is_obvious_field('ticket'):
                    text += " #" + str(self.ticket.id)
        return super().as_summary_item(ar, text, **kwargs)

    def as_paragraph(self, ar):
        txt = super().as_paragraph(ar)
        # txt = ar.add_detail_link(self, str(self))
        if ar and not ar.is_obvious_field('ticket'):
            if self.end_time is None:
                tpl = _("{} working on {}")
            else:
                tpl = _("{} worked on {}")
            txt = format_html(tpl, txt,
                              ar.obj2htmls(self.get_ticket()))
        return txt

    def get_ticket(self):
        if self.ticket_id is not None:
            return self.ticket

    def on_create(self, ar):
        super().on_create(ar)
        if settings.USE_TZ:
            self.time_zone = self.user.time_zone or \
                             rt.models.about.TimeZones.default

    def get_time_zone(self):
        return self.time_zone

    def full_clean(self, *args, **kwargs):
        if self.user_id and not self.time_zone:
            # can be removed when all production sites have migrated:
            self.time_zone = self.user.time_zone or \
                             rt.models.about.TimeZones.default

        if not settings.SITE.loading_from_dump:
            if self.start_time is None:
                self.set_datetime('start', dd.now())
                # value = timezone.now()
                # if pytz:
                #     tz = pytz.timezone(self.get_timezone())
                #     value = value.astimezone(tz)
                # self.start_time = value.time()
            if self.start_date is None:
                self.start_date = dd.today()
            # if self.ticket_id is not None and self.faculty_id is None:
            #     self.faculty = self.ticket.faculty
            if self.end_time is not None:
                if self.end_date is None:
                    self.end_date = self.start_date
            if self.ticket_id:
                self.ticket.on_worked(self)

            self.computed_duration = self.compute_duration()
            # print("20231231 set computed_duration", self.computed_duration)

        super().full_clean(*args, **kwargs)

    def get_duration(self):
        """
        Overrides :meth:`Ended.get_duration
        <lino.mixins.periods.Ended.get_duration>`
        """
        return self.computed_duration

    def compute_duration(self):
        duration = Ended.get_duration(self)
        # duration = self.get_duration()
        if duration is not None:
            if self.break_time:
                duration -= self.break_time
            # print("20231231 a", list(self.get_sub_sessions()))
            for obj in self.get_sub_sessions():
                if obj.computed_duration:
                    duration -= obj.computed_duration
            # assert type(duration) is Duration
        return duration

    def get_sub_sessions(self):
        if self.end_date is None or self.end_date == self.start_date:
            qs = self.__class__.objects.filter(user=self.user,
                                               start_date=self.start_date,
                                               end_date=self.start_date,
                                               start_time__gte=self.start_time,
                                               end_time__lte=self.end_time)
            qs = qs.exclude(id=self.id)
            # print("20231231 single-day", qs.count(), qs.query)
            return qs
        assert self.end_date > self.start_date  # has been working overnight
        # print("20231231 multi-day")
        qs = self.__class__.objects.filter(user=self.user,
                                           start_date__gte=self.start_date,
                                           end_date__lte=self.end_date)
        qs = qs.exclude(id=self.id)
        st = self.get_datetime('start')
        et = self.get_datetime('end')
        lst = []
        for obj in qs.order_by('start_date', 'start_time'):
            # print("20230117", obj)
            if obj.get_datetime('start') >= st:
                if obj.get_datetime('end') <= et:
                    lst.append(obj)
        return lst

    def get_reporting_type(self):
        if self.reporting_type:
            return self.reporting_type
        return self.get_ticket().get_reporting_type()

    # def after_ui_save(self, ar, cw):
    #     super().after_ui_save(ar, cw)
    #     if self.ticket_id:
    #         self.ticket.on_worked(self, ar, cw)

    def get_root_project(self):
        """Return the root project for this session (or None if session has no
        ticket).

        """
        if self.ticket and self.ticket.project:
            return self.ticket.project.get_parental_line()[0]

    @dd.displayfield(_("Ticket #"))
    def ticket_no(self, ar):
        if ar is None:
            return self.ticket_id
        return self.ticket.as_summary_item(ar)  # self.ticket_id)

    # @dd.displayfield(_("Site"))
    # def site_ref(self, ar):
    #     if not self.ticket:
    #         return ''
    #     site = self.ticket.site
    #     if site is None:
    #         return ''
    #     if ar is None:
    #         return str(site)
    #     return site.as_summary_item(ar)

    @dd.virtualfield(dd.DecimalField(verbose_name=_('Duration (decimal)'), max_digits=32, decimal_places=2, null=True, blank=True))
    def duration_decimal(self, ar):
        if self.computed_duration is None:
            return None
        return Decimal(self.computed_duration)

    def get_invoiceable_partner(self):
        if self.ticket_id and self.ticket.order_id:
            return self.ticket.order.get_invoiceable_partner()

    def get_invoiceable_start_date(self, max_date):
        return self.start_date

    def get_invoiceable_end_date(self):
        return self.end_date

    def get_invoiceable_product(self, max_date=None):
        rt = self.get_reporting_type()
        qs = ReportingRule.objects.filter(
            Q(reporting_type='') | Q(reporting_type=rt))
        if self.ticket.urgent:
            qs = qs.exclude(urgent=YesNo.no)
        else:
            qs = qs.exclude(urgent=YesNo.yes)
        if (rule := qs.first()) is None:
            raise Exception(
                "20240802 No reporting rule for {} {}".format(self, rt))
        return rule.product

    def get_invoiceable_qty(self):
        qty = self.get_duration()
        if qty is not None:
            # print("20221220", qty, "-->", Duration(qty))
            return Duration(qty)

    def get_invoiceable_title(self, number=None):
        # return "{} {}".format(self, self.user)
        return str(self)

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        # pre-select all objects that potentially will generate an invoice.

        qs = super().get_generators_for_plan(plan, partner)

        max_date = plan.get_max_date()
        if max_date:
            qs = qs.filter(start_date__lte=max_date)
        if plan.min_date:
            qs = qs.filter(start_date__gte=plan.min_date)

        # qs = cls.objects.all()
        # qs = qs.filter(state=EntryStates.took_place)
        # if plan.area_id:
        #     qs = qs.filter(room__invoicing_area=plan.area)

        if partner is None:
            partner = plan.partner

        if plan.order is not None:
            # raise Exception("20210731 {}".format(dd.plugins.invoicing.order_model))
            # qs = qs.filter(**gfk2lookup(cls.owner, plan.order))
            qs = qs.filter(ticket__order=plan.order)
            # if dd.plugins.invoicing.order_model is rt.models.orders.Order:
            #     qs = qs.filter(ticket__order=plan.order)
            # else:
            #     # sessions on a ticket without an order will never get invoiced
            #     return []
        else:
            qs = qs.filter(ticket__order__isnull=False)
            if partner is not None:
                # fldname = rt.models.tickets.Site.get_partner_filter_field(partner)
                # fldname = rt.models.orders.Order.get_partner_filter_field(partner)
                fldname = dd.plugins.invoicing.order_model.get_partner_filter_field(
                    partner)
                qs = cls.filter_by_invoice_recipient(
                    qs, partner, 'ticket__order__' + fldname)
                # print("20221219", qs.query)
                # q1 = models.Q(
                #     ticket__site__company__salesrule__invoice_recipient__isnull=True,
                #     ticket__site__company=partner)
                # q2 = models.Q(
                #     ticket__site__company__salesrule__invoice_recipient=partner)
                # qs = qs.filter(models.Q(q1 | q2))

        # logger.debug("20240120 %s (%d rows)", qs.query, qs.count())
        return qs.order_by('id')


dd.update_field(Session,
                'user',
                blank=False,
                null=False,
                verbose_name=_("Worker"))
dd.update_field(Session, 'end_time', db_index=True)

Session.set_widget_options('ticket__id', label=_("Ticket #"))
Session.set_widget_options('ticket_no', width=8)
Session.set_widget_options('break_time', hide_sum=True)

# from lino_xl.lib.invoicing.mixins import Periodicities


class Contract(UserAuthored, DateRange):

    class Meta:
        app_label = 'working'
        verbose_name = _("Working contract")
        verbose_name_plural = _('Working contracts')
        abstract = dd.is_abstract_model(__name__, 'Contract')

    start_date = models.DateField(_("Start date"), blank=True, null=True)
    end_date = models.DateField(_("End date"), blank=True, null=True)
    hours_per_week = dd.DurationField(_("Hours/week"))
    # periodicity = Periodicities.field()


dd.update_field(Contract, 'user', verbose_name=_("Worker"))


class ReportingRule(Sequenced):
    # Used to decide which product to use when invoicing a session
    class Meta:
        app_label = 'working'
        verbose_name = _("Reporting rule")
        verbose_name_plural = _("Reporting rules")

    reporting_type = ReportingTypes.field(blank=True, null=True)
    urgent = YesNo.field(blank=True, null=True)
    product = dd.ForeignKey('products.Product', null=True, blank=True)


# class ServiceReport(UserAuthored, ContactRelated, Certifiable, DateRange):
#
#     class Meta:
#         app_label = 'working'
#         verbose_name = _("Service Report")
#         verbose_name_plural = _("Service Reports")
#
#     interesting_for = dd.ForeignKey(
#         'contacts.Partner',
#         verbose_name=_("Interesting for"),
#         blank=True,
#         null=True,
#         help_text=_("Only tickets interesting for this partner."))
#
#     ticket_state = TicketStates.field(
#         null=True, blank=True, help_text=_("Only tickets in this state."))
#
#     def __str__(self):
#         return "{} {}".format(self._meta.verbose_name, self.pk)
#
#     def get_tickets_parameters(self, **pv):
#         """Return a dict with parameter values for `tickets.Tickets` based on
#         the options of this report.
#
#         """
#         pv.update(start_date=self.start_date, end_date=self.end_date)
#         pv.update(interesting_for=self.interesting_for)
#         if self.ticket_state:
#             pv.update(state=self.ticket_state)
#         return pv
#
#
# dd.update_field(ServiceReport, 'user', verbose_name=_("Worker"))
#

class SummaryBySession(DateSummarized, SlaveSummarized, SummarizedFromSession):
    # common base for UserSummary and OrderSummary

    class Meta:
        abstract = True

    @classmethod
    def get_summary_columns(cls):
        for t in ReportingTypes.get_list_items():
            k = t.name + '_hours'
            yield k

    def reset_summary_data(self):
        for t in ReportingTypes.get_list_items():
            k = t.name + '_hours'
            setattr(self, k, None)  # ZERO_DURATION

    def __str__(self):
        s = " / ".join([
            str(getattr(self, name) or "-")
            for name in self.get_summary_columns()
        ])
        return "{}: {}".format(self.year, s)

    # def add_from_session(self, obj):
    #     d = obj.get_duration()
    #     if d:
    #         rt = obj.get_reporting_type()
    #         k = rt.name + '_hours'
    #         value = getattr(self, k) + d
    #         setattr(self, k, value)


class UserSummary(SummaryBySession):

    class Meta:
        app_label = 'working'
        verbose_name = _("User summary")
        verbose_name_plural = _("User summaries")

    summary_period = 'weekly'
    # summary_period = 'monthly'
    delete_them_all = True
    master = dd.ForeignKey('users.User')

    def get_summary_collectors(self):
        qs = rt.models.working.Session.objects.filter(user=self.master)
        if self.year:
            qs = qs.filter(start_date__year=self.year)
        if self.month:
            # remember that summary_period is 'weekly'
            qs = qs.filter(start_date__week=self.month)
        yield (self.add_from_session, qs)


if dd.is_installed("invoicing"):

  class OrderSummary(SummaryBySession):

    class Meta:
        app_label = 'working'
        verbose_name = _("Order summary")
        verbose_name_plural = _("Order summaries")

    summary_period = 'yearly'
    delete_them_all = True
    master = dd.ForeignKey(dd.plugins.invoicing.order_model)

    active_tickets = models.IntegerField(_("Active tickets"))
    inactive_tickets = models.IntegerField(_("Inactive tickets"))

    @classmethod
    def get_summary_columns(cls):
        for k in super().get_summary_columns():
            yield k
        yield 'active_tickets'
        yield 'inactive_tickets'

    def reset_summary_data(self):
        super().reset_summary_data()
        # for ts in TicketStates.get_list_items():
        #     k = ts.get_summary_field()
        #     if k is not None:
        #         setattr(self, k, 0)
        self.active_tickets = 0
        self.inactive_tickets = 0

    def get_summary_collectors(self):
        if self.year is None:
            qs = rt.models.tickets.Ticket.objects.filter(order=self.master)
            # qs = qs.filter(
            #     sessions_by_ticket__start_date__year=self.year)
            yield (self.add_from_ticket, qs)

        qs = rt.models.working.Session.objects.filter(
            ticket__order=self.master)
        if self.year:
            qs = qs.filter(start_date__year=self.year)
        yield (self.add_from_session, qs)

    def add_from_ticket(self, obj):
        ts = obj.state
        # k = ts.get_summary_field()
        # if k is not None:
        #     value = getattr(self, k) + 1
        #     setattr(self, k, value)
        if ts.active:
            self.active_tickets += 1
        else:
            self.inactive_tickets += 1


@dd.receiver(dd.pre_analyze)
def inject_summary_fields(sender, **kw):
    UserSummary = rt.models.working.UserSummary
    Ticket = dd.plugins.working.ticket_model
    options = dict(max_length=dd.plugins.summaries.duration_max_length,
                   null=True,
                   blank=True)
    for t in ReportingTypes.get_list_items():
        k = t.name + '_hours'
        dd.inject_field(UserSummary, k, dd.DurationField(t.text, **options))
        dd.inject_field(Ticket, k, dd.DurationField(t.text, **options))

        if dd.is_installed("invoicing"):

            OrderSummary = rt.models.working.OrderSummary
            dd.inject_field(OrderSummary, k,
                            dd.DurationField(t.text, **options))

            def make_getter(t):
                k = t.name + '_hours'

                def getter(obj, ar):
                    if obj.id is None:
                        # Avoid RemovedInDjango50Warning "Passing unsaved model
                        # instances to related filters is deprecated."
                        return
                    qs = OrderSummary.objects.filter(
                        master=obj, year__isnull=True)
                    # d = qs.aggregate(**{k:models.Sum(k)})
                    start_date_time = dt.datetime.now()
                    end_date_time = copy(start_date_time)
                    for obj in qs:
                        td = getattr(obj, k).as_timedelta()
                        end_date_time += td
                    return end_date_time - start_date_time

                return getter

            dd.inject_field(
                dd.plugins.invoicing.order_model, k,
                dd.VirtualField(dd.DurationField(t.text), make_getter(t)))


def welcome_messages(ar):
    """Yield messages for the welcome page."""

    Session = rt.models.working.Session
    Group = rt.models.groups.Group
    # Ticket = rt.models.tickets.Ticket
    # TicketStates = rt.models.tickets.TicketStates
    me = ar.get_user()

    # all open sessions (i.e. those somebody is working on)
    qs = Session.objects.filter(end_time__isnull=True)
    if dd.is_installed("groups"):
        if not me.user_type.has_required_roles([Triager]):
            mygroups = Group.objects.filter(members__user=me)
            qs = qs.filter(ticket__group__in=mygroups)
    if qs.count() == 0:
        return
    working = {me: [E.b(str(_("You are working on ")))]}
    for ses in qs:
        if ses.user not in working:
            working[ses.user] = [
                ar.obj2html(ses.user),
                gettext(" is working on: ")
            ]
        txt = str(ses.ticket)
        working[ses.user].append(
            ar.obj2html(ses.ticket,
                        txt,
                        title=getattr(ses.ticket, 'summary', "")
                        or getattr(ses.ticket, 'name', "")))

        if ses.user == me:
            working[ses.user] += [
                ' (',
                ar.instance_action_button(ses.end_session,
                                          EndTicketSession.label), ')'
            ]
        working[ses.user].append(', ')

    if len(working[me]) > 1:
        working[me][-1] = working[me][-1].replace(", ", ".")
        result = E.p(*working.pop(me))
    else:
        result = E.p()
        working.pop(me)
    for u, s in working.items():
        if len(result):
            result.append(E.br())
        s[-1] = s[-1].replace(", ", ".")
        result.append(E.span(*s))
    yield result


dd.add_welcome_handler(welcome_messages)

if False:  # works, but is not useful

    def weekly_reporter(days, ar, start_date, end_date):
        Session = rt.models.working.Session
        me = ar.get_user()
        qs = Session.objects.filter(user=me,
                                    start_date__gte=start_date,
                                    end_date__lte=end_date)
        # print 20150420, start_date, end_date, qs
        d2p = dict()
        for ses in qs:
            prj = ses.ticket.project
            if prj is not None:
                while prj.parent is not None:
                    prj = prj.parent
            projects = d2p.setdefault(ses.start_date, dict())
            duration = projects.setdefault(prj, Duration())
            duration += ses.get_duration()
            projects[prj] = duration

        # print 20150420, d2p
        def fmt(delta):
            return str(Duration(delta))

        for date, projects in d2p.items():
            parts = []
            tot = Duration()
            for prj, duration in projects.items():
                if prj is None:
                    prj = "N/A"
                txt = "{0} ({1})".format(prj, fmt(duration))
                parts.append(txt)
                tot += duration
            if len(parts):
                if len(parts) == 1:
                    txt = parts[0]
                else:
                    txt = ', '.join(parts) + " = " + fmt(tot)
                txt = E.p(txt, style="text-align:right")
                days[date].append(txt)

    from lino.utils.weekly import add_reporter
    add_reporter(weekly_reporter)


class SessionChecker(Checker):
    model = Session
    verbose_name = _("Check the computed duration of sessions")

    def get_checkdata_problems(self, ar, obj, fix=False):
        computed_duration = obj.compute_duration()
        if str(obj.computed_duration) != str(computed_duration):
            yield (True, _("Duration is {0} but should be {1}").format(
                str(obj.computed_duration), str(computed_duration)))
            if fix:
                obj.computed_duration = computed_duration
                obj.full_clean()
                obj.save()


SessionChecker.activate()


class TicketSessionsChecker(Checker):
    model = dd.plugins.working.ticket_model
    verbose_name = _("Check the fixed_since field of tickets")

    def get_checkdata_problems(self, ar, obj, fix=False):
        qs = rt.models.working.Session.objects.filter(ticket=obj,
                                                      end_time__isnull=False,
                                                      is_fixing=True)
        qs = qs.order_by('end_date', 'end_time')
        ses = qs.first()
        if ses is None:
            if obj.fixed_since is not None:
                if fix:
                    obj.fixed_since = None
                    obj.full_clean()
                    obj.save()
                yield (True, _("No fixing session but marked as fixed"))
        else:
            if obj.fixed_since is None:
                if fix:
                    obj.fixed_since = ses.get_datetime('end')
                    obj.full_clean()
                    obj.save()
                yield (
                    True,
                    _("Fixing session exists but ticket not marked as fixed"))


TicketSessionsChecker.activate()


dd.inject_field(
    "users.User", 'open_session_on_new_ticket',
    models.BooleanField(_("Open session on new ticket"), default=False))


if not dd.plugins.working.hidden:

    @background_task(every_unit="weekly", every=1, saturday=True, start_time="04:00")
    def send_weekly_report(ar):
        tpl = rt.get_template("working/weekly_report.eml")
        recipients = [
            obj.user.email for obj in rt.models.working.Contract.objects.all()]
        with ar.override_attrs(
            permalink_uris=True, renderer=dd.plugins.memo.front_end.renderer
        ):
            context = ar.get_printable_context()
            body = tpl.render(**context)
            sender = settings.SERVER_EMAIL
            subject = _("Week {weekno} activity report").format(
                weekno=dd.today().strftime("%W"))
            subject = settings.EMAIL_SUBJECT_PREFIX + subject
            ar.send_email(subject, sender, body, recipients)

    def session_top_link(ar):
        if (user := ar.get_user()).is_anonymous:
            return ""
        for ses in rt.models.working.Session.objects.filter(user=user, end_time__isnull=True):
            yield ar.instance_action_button(
                ses.end_session, EndTicketSession.label,
                title=_("Stop working on {ticket}").format(ticket=ses.ticket))

    settings.SITE.add_top_link_generator(session_top_link)
