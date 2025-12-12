# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from django.conf import settings
from django.db import models

from lino.utils.html import E
from lino.utils.format_date import monthname
from lino.utils.format_date import fdf
from lino.modlib.system.choicelists import DurationUnits
from lino.core.utils import dbfield2params_field
from lino.core.fields import TableRow
from lino.api import dd, rt, _


def date2pk(date):
    delta = date - dd.today()
    return delta.days


def weekname(date):
    year, week, day = date.isocalendar()
    text = (date + datetime.timedelta(days=-day + 1)).strftime("%d %B")
    return _("Week {1} / {0} ({2})").format(year, week, text)


def button_func(ar, actor):
    if actor is None:

        def func(day, text):
            return str(text)
    else:
        sar = ar.spawn_request(actor=actor, param_values=ar.param_values)
        # if ar.actor.model is actor.model:
        #     sar = ar.spawn_request(actor=actor, param_values=ar.param_values)
        # else:
        #     print("20230501", ar.actor, "model is not", actor)
        #     sar = ar.spawn_request(actor=actor)

        # rnd = settings.SITE.kernel.default_renderer
        # rnd = ar.renderer

        def func(day, text):
            # day.navigation_mode = actor.navigation_mode
            return sar.ar2button(
                                 day,
                                 text,
                                 style="",
                                 icon_name=None,
                                 title=str(day))

    return func


class CalendarViewable(TableRow):

    def get_event_summary(self, ar):
        # yield "barbaz"
        # yield str(ar.param_values)
        # yield self.as_summary_item(ar)
        yield self.as_str(ar)
        # yield self.as_paragraph(ar)
        # yield str(self)

    @classmethod
    def add_planner_column_filter(self, qs, pc):
        return qs

    if dd.is_installed('calview'):
        def get_display_color(self):
            return settings.SITE.get_config_value('default_color')


class PlannableBase:

    plannable_header_row_label = _("All day")

    @classmethod
    def get_plannable_entries(cls, obj, qs, ar):
        """

        Modify the given queryset of cal.Event objects to be shown in this
        calendar view for the given plannable object `obj`, which is either an
        instance of cls or a HeaderRow instance.

        Date and time filter will be applied later.

        Default implementation does not modify the queryset.

        """
        return qs
        # return rt.models.cal.Event.objects.none()

    def get_my_plannable_entries(self, qs, ar):
        return self.get_plannable_entries(self, qs, ar)


class Day(TableRow):
    # subclassed in lino_xl.lib.working
    navigation_mode = None
    planner = None

    def __init__(self, offset=0, ar=None, navigation_mode="day", planner=None):
        # assert offset is not None
        self.date = dd.today(offset)
        self.pk = offset
        self.ar = ar  # Needed in lino_xl.lib.working
        self.navigation_mode = navigation_mode
        if planner is not None:
            assert isinstance(planner, Planner)
            self.planner = planner

    def __str__(self):
        if self.navigation_mode == "day":
            return fdf(self.date)
        elif self.navigation_mode == "week":
            return weekname(self.date)
        elif self.navigation_mode == "month":
            return monthname(self.date.month) + " " + str(self.date.year)
        else:
            raise Exception("Invalid navigation_mode {} ({})".format(
                self.navigation_mode, self.planner))

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.pk}={self.date})>"

    def skipmonth(self, n):
        return DurationUnits.months.add_duration(self.date, n)

    @classmethod
    def setup_parameters(cls, params):
        super().setup_parameters(params)

        clone_from = rt.models.resolve(dd.plugins.calview.clone_parameters_from)
        M = dd.resolve_model(clone_from.model)
        # M in {'cal.Event', 'working.Session'}
        # print("20250716", M)
        M.setup_parameters(params)

        # simulate for get_simple_parameters
        # event_fields = ['user', 'event_type', 'room']
        # if settings.SITE.project_model:
        #     event_fields.append('project')
        # for k in event_fields:
        # start_date and end_date are used by WorkedHours
        for k in ('user', 'event_type', 'room', 'project', 'start_date', 'end_date'):
            if (de := M.get_data_elem(k)) is not None:
                params[k] = dbfield2params_field(de)


class Planner(dd.Choice):
    daily_view = None
    weekly_view = None
    monthly_view = None
    default_view = None

    def __init__(self, value_and_name, text, dv, wv, mv, **kwargs):
        super().__init__(value_and_name, text, value_and_name, **kwargs)
        self.daily_view = dv
        self.weekly_view = wv
        self.monthly_view = mv

    def on_class_init(self):
        self.daily_view = rt.models.resolve(self.daily_view)
        self.weekly_view = rt.models.resolve(self.weekly_view)
        self.monthly_view = rt.models.resolve(self.monthly_view)
        self.default_view = self.weekly_view
        for a in (self.daily_view, self.weekly_view, self.monthly_view):
            if a is None:
                continue
            if a.planner is not None:
                raise Exception(
                    "Cannot use {} for planner {} as it is already used for {}"
                    .format(a, self, a.planner))
            a.planner = self

    def daily_button_func(self, ar):
        return button_func(ar, self.daily_view)

    def weekly_button_func(self, ar):
        return button_func(ar, self.weekly_view)

    def monthly_button_func(self, ar):
        return button_func(ar, self.monthly_view)


class Planners(dd.ChoiceList):
    item_class = Planner
    column_names = "value name text monthly_view weekly_view daily_view"

    monthly_view = models.CharField(_("Monthly view"))
    weekly_view = models.CharField(_("Weekly view"))
    daily_view = models.CharField(_("Daily view"))

    @classmethod
    def class_init(cls):
        super().class_init()
        for p in cls.get_list_items():
            p.on_class_init()


add = Planners.add_item
add("default", _("Calendar"), "calview.DailyView", "calview.WeeklyView",
    "calview.MonthlyView")


class Plannable(dd.Model, PlannableBase):

    class Meta:
        abstract = True

    @classmethod
    def on_analyze(cls, site):
        super().on_analyze(site)
        cls.HEADER_ROW = HeaderRow(cls)

    def get_header_chunks(obj, ar, entries, today):
        if not isinstance(obj, HeaderRow):
            raise Exception("{} is not a header row".format(obj))
        mdes = entries.filter(end_date__isnull=False, end_date__gt=today)
        mdes = mdes.order_by('-end_date')
        entries = entries.filter(
            models.Q(start_time__isnull=True),
            models.Q(end_date__isnull=True) | models.Q(end_date=today))

        # from .mixins import Planners
        pk = date2pk(today)
        planner = ar.actor.calendar_view.planner
        # print("20230501", ar.actor.calendar_view)
        target_day = Day(pk, ar, "day", planner)
        daily_button_func = planner.daily_button_func(ar)
        txt = daily_button_func(target_day, str(today.day))

        if today == dd.today():
            txt = E.b(txt)

        events = rt.models.resolve(dd.plugins.calview.clone_parameters_from)
        btn = ar.gen_insert_button(events, start_date=today)
        if btn is None:
            yield E.div(E.p(txt, align="center"))
        else:
            yield E.div(E.p(txt, btn, align="center"))
        # yield E.p(*obj.model.gen_insert_button(ar.actor, [txt], ar, today), align="center")

        # if today.weekday() == 0:
        #     ar.actor.mde_count = [0, 0, 0, 0, 0, 0, 0]

        for i in range(obj.mde_count[today.weekday()]):
            yield E.div("\u00A0", style="height: 1.2em;")

        uncolored_mdes = []

        for e in mdes:
            if not e.get_display_color():
                uncolored_mdes.append(e)
                continue
            days = (e.end_date - e.start_date).days
            max_count = obj.mde_count[today.weekday()] + 1
            for i in range(days + 1):
                mde_pos = today.weekday() + i
                if mde_pos >= 7:
                    days = i - 1
                    break
                obj.mde_count[mde_pos] = max_count
            style = f"margin-right: -{100 * days}%;" \
                + "position: relative;padding: 0 5px; border-radius: 5px;"
            yield e.as_summary_item(
                ar,
                ar.actor.get_calview_div(e, ar, passed_style=style, mde=True))

        for e in uncolored_mdes:
            yield e.as_summary_item(ar, ar.actor.get_calview_div(e, ar))

        for e in entries:
            yield e.as_summary_item(ar, ar.actor.get_calview_div(e, ar))

    def get_weekly_chunks(obj, ar, entries, today):
        if isinstance(obj, HeaderRow):
            raise Exception("{} is a header row".format(obj))
        entries = entries.filter(end_date__isnull=True)
        for e in entries:
            yield e.as_summary_item(ar, ar.actor.get_calview_div(e, ar))


class HeaderRow(CalendarViewable, PlannableBase):
    # class HeaderRow(CalendarViewable):

    # class Meta:
    #     abstract = True

    _lino_default_table = None
    id = None

    def __init__(self, model):
        self.model = model
        self.mde_count = [0, 0, 0, 0, 0, 0, 0]
        super().__init__()

    def __getattr__(self, name):
        return None

    def __str__(self):
        return str(self.model.plannable_header_row_label)

    def get_header_chunks(self, *args):
        return self.model.get_header_chunks(self, *args)

    def get_weekly_chunks(self, *args):
        return self.model.get_weekly_chunks(self, *args)

    def get_my_plannable_entries(self, *args):
        return self.model.get_plannable_entries(self, *args)


Plannable.django2lino(HeaderRow)
