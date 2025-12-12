# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.conf import settings
from django.utils.translation import pgettext_lazy as pgettext

from lino.api import dd, _

from lino.modlib.system.choicelists import DurationUnits, DisplayColors


class YearMonths(dd.ChoiceList):
    verbose_name = _("YearMonths")


add = YearMonths.add_item
add('1', _('January'), 'january')
add('2', _('February'), 'february')
add('3', _('March'), 'march')
add('4', _('April'), 'april')
add('5', _('May'), 'may')
add('6', _('June'), 'june')
add('7', _('July'), 'july')
add('8', _('August'), 'august')
add('9', _('September'), 'september')
add('10', _('October'), 'october')
add('11', _('November'), 'november')
add('12', _('December'), 'december')

# class PositioningType(dd.Choice):
#     available_for = ['secondly', 'minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly']
#
#
# class PositioningTypes(dd.ChoiceList):
#     verbose_name = _("Positioning types")
#
#
# add = PositioningTypes.add_item
# add('BYSECOND', _("By second"))
# add('BYMINUTE', _("By minute"))
# add('BYHOUR', _("By hour"))
# add('BYDAY', _("By day"))
# add('BYMONTHDAY', _("By day of month"), available_for=['secondly', 'minutely', 'hourly', 'daily', 'monthly', 'yearly'])
# add('BYYEARDAY', _("By day of year"), available_for=['secondly', 'minutely', 'hourly', 'yearly'])
# add('BYWEEKNO', _("By week number"), available_for=['yearly'])
# add('BYMONTH', _("By month"))
# add('BYSETPOS', _("By setpos"))
# add('WKST', _("wkst"), 'wkst')


def amonthago():
    return DurationUnits.months.add_duration(dd.today(), -1)


# class AccessClasses(dd.ChoiceList):
#     verbose_name = _("Access class")
#     verbose_name_plural = _("Access classes")
#     required_roles = dd.login_required(dd.SiteStaff)
# add = AccessClasses.add_item
# add('10', _('Private'), 'private')
# add('20', _('Show busy'), 'show_busy')
# add('30', _('Public'), 'public')


class PlannerColumns(dd.ChoiceList):
    verbose_name = _("Planner column")
    verbose_name_plural = _("Planner columns")
    required_roles = dd.login_required(dd.SiteStaff)


add = PlannerColumns.add_item
add('10', _('External'), 'external')
add('20', _('Internal'), 'internal')


class TaskStates(dd.Workflow):
    verbose_name_plural = _("Task states")
    required_roles = dd.login_required(dd.SiteStaff)
    app_label = 'cal'


add = TaskStates.add_item

add('10', _("To do"), 'todo')
add('15', _("Important"), 'important')
add('20', pgettext(u"cal", u"Started"), 'started')
add('30', _("Done"), 'done')
# add('40', _("Sleeping"),'sleeping')
add('50', _("Cancelled"), 'cancelled')

if not settings.SITE.use_silk_icons:
    TaskStates.todo.button_text = "☐"  # BALLOT BOX \u2610
    TaskStates.started.button_text = "☉"  # SUN (U+2609)
    TaskStates.done.button_text = "☑"  # BALLOT BOX WITH CHECK \u2611
    TaskStates.cancelled.button_text = "☒"  # BALLOT BOX WITH X (U+2612)
    TaskStates.important.button_text = "⚠"  # U+26A0


class GuestState(dd.State):
    afterwards = False


class GuestStates(dd.Workflow):
    verbose_name_plural = _("Presence states")
    required_roles = dd.login_required(dd.SiteStaff)
    app_label = 'cal'
    item_class = GuestState
    afterwards = models.BooleanField(_("Afterwards"), default=False)

    @classmethod
    def get_column_names(self, ar):
        return 'value name afterwards text button_text'


add = GuestStates.add_item
add('10', _("Invited"), 'invited')

# GuestStates will be reset by importing either feedback or
# voga. But the calendar module itself requires a state named
# `invited`


class EntryState(dd.State):
    fixed = False
    fill_guests = False
    transparent = False
    noauto = False
    guest_state = None


class EventEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")


add = EventEvents.add_item
add('10', _("Stable"), 'stable')
add('20', _("Unstable"), 'pending')


class EntryStates(dd.Workflow):
    verbose_name_plural = _("Entry states")
    required_roles = dd.login_required(dd.SiteStaff)
    app_label = 'cal'
    item_class = EntryState
    fill_guests = models.BooleanField(_("Fill guests"), default=False)
    fixed = models.BooleanField(_("Stable"), default=False)
    transparent = models.BooleanField(_("Transparent"), default=False)
    noauto = models.BooleanField(_("No auto"), default=False)
    guest_state = GuestStates.field(_("Guest state"), blank=True)
    # editable_states = set()
    # column_names = "value name text fill_guests"

    # @dd.virtualfield(models.BooleanField("fill_guests"))
    # def fill_guests(cls,obj,ar):
    # return obj.fill_guests

    @classmethod
    def get_column_names(self, ar):
        return 'value name text button_text fill_guests fixed transparent noauto'


# 20250620 Should suggested events be transparent? Currently they aren't because
# if they were transparent, Lino wouldn't try to find the next slot when a
# wanted event is in conflict with another suggestion. But is this such a
# problem? Wouldn't it be interesting to allow conflicting suggested events, or
# at least in some workflows?

add = EntryStates.add_item
add('10', _("Suggested"), 'suggested', fill_guests=True, button_text="?")

add('20', _("Draft"), 'draft', fill_guests=True,
    button_text="☐")  # BALLOT BOX (2610)
if False:
    add('40', _("Published"), 'published')
    # add('30', _("Notified"),'notified')
    add('30', _("Visit"), 'visit')
    add('60', _("Rescheduled"), 'rescheduled', fixed=True)
add('50',
    _("Took place"),
    'took_place',
    fixed=True,
    fill_guests=False,
    button_text="☑")  # BALLOT BOX WITH CHECK (2611)

# lino_tera add a state "Missed"
# add('60', _("Missed"), 'missed', transparent=True,
#     help_text=_("Guest missed the appointment."),
#     button_text="☉", noauto=True)  # \u2609 SUN

add('70',
    _("Cancelled"),
    'cancelled',
    fixed=True,
    transparent=True,
    help_text=_("Cancelled with valid reason."),
    button_text="☒",
    noauto=True)

if False:
    add('75',
        _("Omitted"),
        'omitted',
        fixed=True,
        transparent=True,
        button_text="☒")  # BALLOT BOX WITH X (\u2612)
    # button_text="☹")  # 2639


class NotifyBeforeUnits(dd.ChoiceList):
    verbose_name = _("Unit")
    verbose_name_plural = _("Notify Units")


add = NotifyBeforeUnits.add_item
add('10', _('minutes'), 'minutes')
add('20', _('hours'), 'hours')
add('30', _('days'), 'days')
add('40', _('weeks'), 'weeks')

# class SchedulingArea(dd.Choice):
#     all_rooms = False
#
#     def get_target_type(self):
#         qs = rt.models.cal.EventType.objects.filter(scheduling_area=self)
#         if qs.count() > 1:
#             tpl = "Multiple types for scheduling area {} : {}"
#             raise Exception(tpl.format(self, [j.ref for j in qs]))
#         return qs.first()
#
#
# class SchedulingAreas(dd.ChoiceList):
#     verbose_name = _("Scheduling area")
#     verbose_name_plural = _("Scheduling areas")
#     item_class = SchedulingArea
#     column_names = 'value name text target_type'
#     required_roles = dd.login_required(dd.SiteStaff)
#     max_length = 20
#
#     @dd.displayfield(_("Calendar entry type"))
#     def target_type(cls, choice, ar):
#         et = choice.get_target_type()
#         if et is None:
#             return None
#         return et.ref
#
# SchedulingAreas.add_item('holidays', _("Holidays"), 'holidays', all_rooms=True)
# SchedulingAreas.add_item('birthdays', _("Birthdays"), 'birthdays', all_rooms=False)
