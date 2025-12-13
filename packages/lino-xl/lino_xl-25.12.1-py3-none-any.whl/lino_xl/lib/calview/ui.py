# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
from collections import OrderedDict
from calendar import Calendar as PythonCalendar

from django.conf import settings
from django.db import models
from django.utils.html import format_html

from lino.api import dd, rt, _, gettext
from lino.mixins import ObservedDateRange, Draggable
from lino.core.tables import VentilatedColumns, AbstractTable
from lino.core import fields
from lino.utils.format_date import monthname
from lino.utils.format_date import day_and_month, day_and_weekday
from lino.modlib.users.mixins import My
from lino.modlib.office.roles import OfficeUser, OfficeStaff, OfficeOperator

from lino.utils import join_elems, ONE_DAY, ONE_WEEK
from lino.utils.html import E, forcetext, tostring

from lino_xl.lib.cal.choicelists import PlannerColumns, YearMonths
from lino.modlib.system.choicelists import DurationUnits, Weekdays

from .mixins import Planner, date2pk, Day, PlannableBase, CalendarViewable
from lino.core import constants

CALENDAR = PythonCalendar()

BOXWRAP = "<div>{}</div>"


class InsertEvent(dd.Action):
    label = _("Create new calendar event")
    icon_name = 'add'  # if action rendered as toolbar button
    help_text = _("Create a new calendar event")
    show_in_toolbar = True

    def run_from_ui(self, ar, **kw):
        t = rt.models.cal.Event.get_default_table()
        sar = t.insert_action.request_from(ar)
        sar.known_values = dict(start_date=str(ar.selected_rows[0].date))
        ar.set_response(eval_js=ar.renderer.ar2js(sar, None))


class DailyPlannerRows(dd.Table):
    # used for configuring the planner rows
    model = 'calview.DailyPlannerRow'
    column_names = "seqno designation start_time end_time"
    required_roles = dd.login_required(OfficeStaff)


class ParameterClone(dd.Actor):

    # Mixin for actors that inherit parameters and params_layout from another
    # table. The takeover must happen *after* the custom_layout_module has been
    # loaded. So we override the class_init() method.

    abstract = True
    clone_from = dd.plugins.calview.clone_parameters_from
    params_panel_pos = 'left'
    params_panel_hidden = False
    # 20250122: navigation_panel was moved from DayNavigator to ParameterClone

    @classmethod
    def class_init(cls):
        if isinstance(cls.clone_from, str):
            cls.clone_from = rt.models.resolve(cls.clone_from)
        super().class_init()
        # print(f"20250717 class_init() {cls} {cls.clone_from}")

    @classmethod
    def init_layouts(cls):
        super().init_layouts()
        # cls.params_layout = rt.models.cal.Events.params_layout
        pl = dd.plugins.calview.params_layout
        if settings.SITE.default_ui == 'lino_react.react':  # 20230501
            pl = """
            navigation_panel
            """ + pl
        cls.params_layout = pl

    @classmethod
    def setup_parameters(cls, params):
        # super().setup_parameters(params)
        if cls.abstract or cls.clone_from is None:
            return
        cls.clone_from.setup_parameters(params)
        # print(f"20250717 setup_parameters() {cls.clone_from} {sorted(params.keys())}")

    @classmethod
    def get_title(self, ar):
        if ar.master_instance:
            return str(ar.master_instance)
        return "Foo"

    @classmethod
    def get_data_elem(cls, name):
        e = super().get_data_elem(name)
        if e is None and cls.clone_from is not None:
            e = cls.clone_from.get_data_elem(name)
        return e
        # return cls.clone_from.get_data_elem(name)

    @classmethod
    def get_simple_parameters(cls):
        # for p in super().get_simple_parameters():
        #     yield p
        if cls.clone_from is not None:
            for p in cls.clone_from.get_simple_parameters():
                yield p
        yield "navigation_panel"

    @classmethod
    def param_defaults(cls, ar, **kwargs):
        # kwargs = super().param_defaults(ar, **kwargs)  # back since 20250122
        kwargs.update(navigation_panel=None)
        if cls.clone_from is not None:
            kwargs = cls.clone_from.param_defaults(ar, **kwargs)
        # print(f"20250717 {cls} param_defaults() returns {sorted(kwargs.keys())}")
        return kwargs

    @dd.delayedhtmlbox(default=None)
    def navigation_panel(cls, obj, ar):
        if ar is None:
            return None
        # if ar.actor.navigator is None:
        #     # raise Exception("Oops, {} has no navigator".format(cls))
        #     print("Oops, {} has no navigator".format(cls))
        #     return None

        cls = ar.actor
        today = obj.date
        # daily, weekly, monthly = obj.cal_view.navigator.make_link_funcs(ar)

        daily = obj.planner.daily_button_func(ar)
        weekly = obj.planner.weekly_button_func(ar)
        monthly = obj.planner.monthly_button_func(ar)

        if obj.navigation_mode == 'day':
            long_unit = DurationUnits.months
            short_unit = DurationUnits.days
            current_view = daily
        elif obj.navigation_mode == 'week':
            long_unit = DurationUnits.months
            short_unit = DurationUnits.weeks
            current_view = weekly
        elif obj.navigation_mode == 'month':
            long_unit = DurationUnits.years
            short_unit = DurationUnits.months
            current_view = monthly
        else:
            raise Exception("20200224")

        daily_mode = bool(obj.navigation_mode == 'day')
        weekly_mode = bool(obj.navigation_mode == 'week')
        month_mode = bool(obj.navigation_mode == 'month')

        # todo ensure that the end of the month is always in the view.
        # long_unit = DurationUnits.years if month_mode else DurationUnits.months
        long_prev = cls.get_row_by_pk(
            ar, date2pk(long_unit.add_duration(today, -1)))
        long_next = cls.get_row_by_pk(
            ar, date2pk(long_unit.add_duration(today, 1)))
        # next_unit = DurationUnits.weeks if weekly_mode else DurationUnits.days if day_view else DurationUnits.months
        short_prev = cls.get_row_by_pk(
            ar, date2pk(short_unit.add_duration(today, -1)))
        short_next = cls.get_row_by_pk(
            ar, date2pk(short_unit.add_duration(today, 1)))
        # current_view = weekly if weekly_mode else daily
        # current_view = daily
        # if not day_view:
        #     current_view = monthly if month_mode else weekly

        elems = []  # cls.calender_header(ar)

        # Month div
        rows, cells = [], []
        for i, month in enumerate(YearMonths.get_list_items()):
            pk = date2pk(
                DurationUnits.months.add_duration(today, i + 1 - today.month))
            if today.month == i + 1:
                if not month_mode:
                    cells.append(
                        E.td(
                            E.b(monthly(cls.get_row_by_pk(ar, pk),
                                        str(month)))))
                else:
                    cells.append(E.td(E.b(str(month))))
            else:
                cells.append(
                    E.td(monthly(cls.get_row_by_pk(ar, pk), str(month))))
            if (i + 1) % 3 == 0:
                rows.append(E.tr(*cells, align="center"))
                cells = []
        monthly_div = E.div(E.table(*rows, align="center"),
                            CLASS="cal-month-table")

        header = [
            # current_view(long_prev, "<<"), " " , current_view(short_prev, "<"),
            E.span(
                E.span("{} {}".format(monthname(today.month), today.year),
                       E.br(), monthly_div)),
            # current_view(short_next, ">"), " ", current_view(long_next, ">>")
        ]
        elems.append(E.h2(*header, align="center"))
        weekdaysFirstLetter = " " + "".join(
            [gettext(week.text)[0] for week in Weekdays.objects()])
        rows = [
            E.tr(*[
                E.td(E.b(day_of_week)) for day_of_week in weekdaysFirstLetter
            ],
                 align='center')
        ]
        for week in CALENDAR.monthdatescalendar(today.year, today.month):
            # each week is a list of seven datetime.date objects.
            cells = []
            current_week = week[0].isocalendar()[1]
            this_week = False
            for day in week:
                pk = date2pk(day)
                link = daily(cls.get_row_by_pk(ar, pk), str(day.day))
                if day == dd.today():
                    link = E.b(link, CLASS="cal-nav-today")
                if day == today and daily_mode:
                    cells.append(E.td(E.b(str(day.day))))
                else:
                    cells.append(E.td(link))
                if day.isocalendar()[1] == today.isocalendar()[1]:
                    this_week = True
            else:
                if this_week and weekly_mode:
                    txt = E.b(str(current_week))
                else:
                    pk = date2pk(week[0])
                    txt = weekly(cls.get_row_by_pk(ar, pk), str(current_week))
                cells = [E.td(txt, CLASS="cal-week center")] + cells
            rows.append(E.tr(*cells, align="center"))

        today = cls.get_row_by_pk(ar, 0)
        elems.append(E.table(*rows, align="center"))
        elems.append(E.p(daily(today, gettext("Today")), align="center"))
        # elems.append(E.p(weekly(today, gettext("This week")), align="center"))
        # elems.append(E.p(monthly(today, gettext("This month")), align="center"))

        # for o in range(-10, 10):
        #     elems.append(ar.goto_pk(o, str(o)))
        #     elems.append(" ")
        return E.div(*elems, CLASS="lino-nav-cal")


class DaysTable(dd.VirtualTable):
    abstract = True
    model = 'calview.Day'
    # navigation_mode = None  # "day" or "week" or "month"
    navigation_mode = "day"  # "day" or "week" or "month"

    @classmethod
    def get_planner(cls):
        pass

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        """
        pk is the offset from today in days
        """
        return cls.model(int(pk), ar, cls.navigation_mode, cls.get_planner())

    # @classmethod
    # def get_request_queryset(cls, ar, **filter):
    @classmethod
    def get_data_rows(cls, ar):
        # home = cls.get_row_by_pk(ar, 0)
        # ni = cls.get_navinfo(ar, home)

        pv = ar.param_values
        # date = pv.start_date or dd.today(ni['first'])
        # last = pv.end_date or dd.today(ni['last'])
        # start_date = dd.plugins.cal.beginning_of_time
        # end_date = dd.plugins.cal.ignore_dates_after

        if cls.navigation_mode == "day":
            def step(x): return x + ONE_DAY
            delta = 7
        elif cls.navigation_mode == "week":
            def step(x): return x + ONE_WEEK
            delta = 7 * 2
        elif cls.navigation_mode == "month":
            def step(x): return DurationUnits.months.add_duration(x, 1)
            delta = 40
        else:
            def step(x): return DurationUnits.years.add_duration(x, 1)
            delta = 40

        date = pv.start_date or dd.today(-delta)
        last = pv.end_date or dd.today(delta)

        while date <= last:
            yield cls.get_row_by_pk(ar, date2pk(date))
            date = step(date)


class DayNavigator(DaysTable):
    # every row is a Day instance. Note that Day can be overridden.

    abstract = True
    editable = False
    # required_roles = dd.login_required((OfficeUser, OfficeOperator))
    required_roles = dd.login_required(OfficeUser)
    parameters = ObservedDateRange(
        user=dd.ForeignKey('users.User', null=True, blank=True))
    column_names = "detail_link *"
    # 20250122 params_panel_hidden = False
    default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    # hide_top_toolbar = True
    planner = None  # must be set for concrete subclasses

    @classmethod
    def get_navinfo(cls, ar, day):
        assert isinstance(day, Day)
        # so that str() gives the right format
        day.navigation_mode = cls.navigation_mode
        ni = dict(recno=day.pk, message=str(day))

        if cls.navigation_mode == "month":
            ni.update(next=date2pk(day.skipmonth(1)))
            ni.update(prev=date2pk(day.skipmonth(-1)))
            ni.update(first=day.pk - 365)
            ni.update(last=day.pk + 365)
        elif cls.navigation_mode == "week":
            ni.update(next=day.pk + 7)
            ni.update(prev=day.pk - 7)
            ni.update(first=date2pk(day.skipmonth(-1)))
            ni.update(last=date2pk(day.skipmonth(1)))
        elif cls.navigation_mode == "day":
            ni.update(next=day.pk + 1)
            ni.update(prev=day.pk - 1)
            ni.update(first=date2pk(day.skipmonth(-1)))
            ni.update(last=date2pk(day.skipmonth(1)))
        else:
            raise Exception("Invalid navigation_mode {}".format(
                cls.navigation_mode))
        return ni

    @dd.virtualfield(models.IntegerField(_("Day number")))
    def day_number(cls, obj, ar):
        return obj.pk

    @classmethod
    def get_pk_field(cls):
        # return pk_field
        # return PK_FIELD
        # return cls.get_data_elem('day_number')
        return cls.day_number.return_type


class CalendarView(DayNavigator):
    title = _("Planner")
    abstract = True
    use_detail_param_panel = True
    # plannable_model = None  # must be set for concrete subclasses

    @classmethod
    def get_actor_label(cls):
        return cls.planner.text

    @classmethod
    def get_planner(cls):
        return cls.planner

    @classmethod
    def get_default_action(cls):
        return cls.detail_action
        # return dd.ShowDetail(cls.detail_layout)

    @classmethod
    def collect_extra_actions(cls):
        if cls.planner is None:
            return
        yield dd.WrappedAction(
            # rt.models.calview.DailyView.detail_action,
            cls.planner.daily_view.detail_action,
            help_text=_("Show daily view."),
            button_text=_("Daily"),
            icon_name=None)
        yield dd.WrappedAction(
            # rt.models.calview.WeeklyView.detail_action,
            cls.planner.weekly_view.detail_action,
            # action_name='calview_weekly_wrapper',
            help_text=_("Show weekly view."),
            button_text=_("Weekly"),
            icon_name=None)
        if cls.planner.monthly_view:
            yield dd.WrappedAction(
                # rt.models.calview.MonthlyView.detail_action,
                cls.planner.monthly_view.detail_action,
                help_text=_("Show monthly view."),
                button_text=_("Monthly"),
                icon_name=None)


class DaySlave(AbstractTable):
    abstract = True
    editable = False
    # hide_top_toolbar = True # no selections no toolbar
    hide_navigator = True  # no selections no toolbar
    preview_limit = 0  # no paginator & all rows.
    use_detail_params_value = True  # Get parameter values from detail view.
    master = 'calview.Day'
    # navigation_mode = "day"  # or "week" or "month"
    calendar_view = None
    with_header_row = True
    details_of_master_template = _("%(master)s")
    default_display_modes = {None: constants.DISPLAY_MODE_GRID}
    table_as_calendar = True

    # @classmethod
    # def get_title(cls, ar): return None

    @classmethod
    def get_actor_label(cls):
        return None

    @classmethod
    def class_init(cls):
        super().class_init()
        if isinstance(cls.calendar_view, str):
            cls.calendar_view = rt.models.resolve(cls.calendar_view)

    @classmethod
    def get_master_instance(cls, ar, model, pk):
        if not pk:
            pk = 0
        return model(int(pk), ar, cls.calendar_view.navigation_mode,
                     cls.calendar_view.planner)

    @classmethod
    def get_calendar_entries(cls, ar, obj):
        events_table = rt.models.resolve(dd.plugins.calview.clone_parameters_from)
        qs = events_table.get_request_queryset(ar)
        # print("20230430", qs.query)
        if obj is not None:
            if not isinstance(obj, PlannableBase):
                raise Exception(f"{repr(obj)} is not PlannableBase")
            qs = obj.get_my_plannable_entries(qs, ar)
        return qs

    @classmethod
    def get_dayslave_rows(cls, ar):
        # subclasses must implement this. they must not use the default
        # get_request_queryset() because we are cloning filter parameters.
        return []

    @classmethod
    def get_data_rows(cls, ar):
        if cls.with_header_row:
            yield cls.model.HEADER_ROW
        for obj in cls.get_dayslave_rows(ar):
            yield obj

    @classmethod
    def update_row_meta(cls, today, ar):
        if 'calDates' not in ar.row_meta:
            ar.row_meta['calDates'] = [None for i in range(8)]
        ar.row_meta['calDates'][today.weekday() + 1] = today.isoformat()

    @classmethod
    def unused_get_calview_chunks(cls, self, ar):
        """

        Yield a series of HTML elements or strings that represent the given
        calendar entry as a paragraph.

        """
        pv = ar.param_values
        if self.start_time:
            yield str(self.start_time)[:5]

        # elif not pv.start_date:
        # t.append(str(self.start_date))
        if not pv.user and self.user:
            yield str(self.user)
        if self.summary:
            yield self.summary
        if not pv.event_type and self.event_type:
            yield str(self.event_type)
        if not pv.room and self.room:
            yield str(self.room)
        if settings.SITE.project_model is not None and not pv.project and self.project:
            yield str(self.project)

    @classmethod
    def get_calview_div(cls,
                        obj,
                        ar,
                        today=None,
                        passed_style=None,
                        mde=False):
        """Return a <div> for this calendar entry in the view given by ar.

        """
        time_text = ""
        if obj.start_time:
            time_text = "{} ".format(obj.start_time)[:5]

        # text = E.span(*cls.get_calview_chunks(obj, ar))
        text = E.span(time_text, " ", *obj.get_event_summary(ar))
        # print(f"20250718 {tostring(text)}")
        color = obj.get_display_color()
        if color:
            style = "overflow: hidden; background-color: {}; color: {}; ".format(
                color.value, color.font_color)
            if passed_style:
                style += passed_style
            if mde:
                style += " height: 1.2em;"
                return E.div(text, style=style, pk=str(obj.pk))
            dot = E.span("\u00A0", CLASS="dot", style=style)
            # ele.attrib['style'] = "color: white;background-color: {};".format(data_color)
            # dot.attrib['style'] = "background-color: {};".format(data_color)
            return E.div(
                dot,
                text,
                style="overflow: hidden; height: 1.2em;padding: 0 5px",
                pk=str(obj.pk))
        else:
            return E.div(
                text,
                style="overflow: hidden; height: 1.2em;padding: 0 5px",
                pk=str(obj.pk))


class DailySlaveBase(DaySlave, VentilatedColumns):
    abstract = True
    label = _("Daily planner")
    column_names_template = "overview:12 {vcolumns}"
    ventilated_column_suffix = ':20'
    required_roles = dd.login_required((OfficeUser, OfficeOperator))
    calendar_view = "calview.DailyView"
    # details_of_master_template = _("%(master)s")
    # details_of_master_template = _("%(details)s on %(master)s")

    @classmethod
    def get_dayslave_rows(cls, ar):
        return rt.models.calview.DailyPlannerRow.objects.all()

    @classmethod
    def get_ventilated_columns(cls):
        for pc in PlannerColumns.objects():
            yield cls.get_daily_field(pc)

    @classmethod
    def get_daily_field(cls, pc):
        # if not dd.is_installed("cal"):
        #     return dd.DummyField()
        #
        # Event = rt.models.cal.Event

        events_table = rt.models.resolve(dd.plugins.calview.clone_parameters_from)

        def func(fld, obj, ar):
            # obj is a DailyPlannerRow instance
            mi = ar.master_instance
            if mi is None:  # e.g. when using DailySlave from dashboard.
                mi = cls.calendar_view.get_row_by_pk(ar, 0)
            qs = cls.get_calendar_entries(ar, obj)
            # print(f"20250718 {cls} {obj.__class__}")
            qs = events_table.model.add_planner_column_filter(qs, pc)
            # qs = qs.filter(event_type__planner_column=pc)
            # qs = qs.filter(start_date=mi.date)
            qs = qs.filter(
                models.Q(start_date=mi.date)
                | models.Q(end_date__gte=mi.date, start_date__lte=mi.date))

            # pv = ar.param_values
            # qs = Event.calendar_param_filter(qs, pv)
            # current_day = pv.get('date', dd.today())
            # if current_day:
            #     qs = qs.filter(start_date=current_day)
            # if obj is cls.model.HEADER_ROW:
            #     qs = qs.filter(start_time__isnull=True)
            # else:
            #     get_plannable_entries
            #     if obj.start_time:
            #         qs = qs.filter(start_time__gte=obj.start_time,
            #                        start_time__isnull=False)
            #     if obj.end_time:
            #         qs = qs.filter(start_time__lt=obj.end_time,
            #                        start_time__isnull=False)
            qs = qs.order_by('start_date', 'start_time')
            chunks = [e.as_summary_item(
                ar, cls.get_calview_div(e, ar)) for e in qs]
            # return E.table(E.tr(E.td(E.div(*join_elems(chunks),
            #     style="overflow: visible;"))), CLASS="fixed-table")
            return format_html(BOXWRAP, tostring(chunks))

        return dd.VirtualField(dd.HtmlBox(pc.text), func)


class WeeklySlaveBase(DaySlave, VentilatedColumns):

    # subclassed by WeeklySlave, but also in Presto where we define a custom
    # weekly Slave as a class WorkersByWeek(Workers, WeeklySlaveBase)

    abstract = True
    # title = _("Weekly planner")
    label = _("Weekly planner")
    column_names_template = "overview:12 {vcolumns}"
    ventilated_column_suffix = ':20'
    # navigation_mode = "week"
    calendar_view = "calview.WeeklyView"
    # details_of_master_template = _("%(details)s in %(master)s")
    # details_of_master_template = _("%(master)s")

    @classmethod
    def get_dayslave_rows(cls, ar):
        return rt.models.calview.DailyPlannerRow.objects.all()

    @classmethod
    def get_ventilated_columns(cls):
        for wd in Weekdays.objects():
            yield cls.get_weekly_field(wd)

    @classmethod
    def get_weekly_field(cls, week_day):

        def func(fld, obj, ar):
            if not isinstance(obj, PlannableBase):
                raise Exception(f"{repr(obj)} is not PlannableBase")
            qs = cls.get_calendar_entries(ar, obj)
            delta_days = int(ar.rqdata.get('mk', 0)
                             or 0) if ar.rqdata else ar.master_instance.pk
            # current_day = dd.today() + timedelta(days=delta_days)
            delta_days += int(week_day.value) - \
                dd.today(delta_days).weekday() - 1
            today = dd.today(delta_days)
            # current_week_day = current_day + \
            #     timedelta(days=int(week_day.value) - current_day.weekday() - 1)
            # qs = qs.filter(start_date=today)

            cls.update_row_meta(today, ar)

            qs = qs.filter(start_date=today)
            qs = qs.order_by('start_time')
            if obj is cls.model.HEADER_ROW:
                chunks = obj.get_header_chunks(ar, qs, today)
            else:
                chunks = obj.get_weekly_chunks(ar, qs, today)
            # return E.table(E.tr(E.td(E.div(*join_elems(chunks),
            #     style="overflow: visible;"))), CLASS="fixed-table")
            return format_html(BOXWRAP, tostring(chunks))

        return dd.VirtualField(dd.HtmlBox(week_day.text), func)


class MonthlySlaveBase(DaySlave, VentilatedColumns):
    abstract = True
    # title = "X"
    label = _("Monthly planner")
    column_names_template = "week_number:2 {vcolumns}"
    ventilated_column_suffix = ':20'
    # navigation_mode = "week"
    calendar_view = "calview.MonthlyView"
    # details_of_master_template = _("%(details)s in %(master)s")
    # details_of_master_template = _("%(master)s")

    @classmethod
    def get_ventilated_columns(cls):
        for wd in Weekdays.get_list_items():
            yield cls.get_monthly_field(wd)

    @classmethod
    def get_monthly_field(cls, wd):
        # wd is the weekday, a choice instance of cal.Weekdays
        if not dd.is_installed("cal"):
            return dd.DummyField()
        Events = rt.models.cal.Events

        def func(fld, obj, ar):
            # obj is the first day of the current week
            # ar is a table request on calview.MonthlySlave
            # ar.master_instance is a Day instance with monthly navigation
            mi = ar.master_instance
            if mi is None:
                return
            # today = dd.today()
            qs = cls.get_calendar_entries(ar, None)
            # print("20230501 master instance is", mi, mi.__class__)
            # print("20230501 ar is", ar)
            current_month = mi.date.month
            daily_button_func = mi.planner.daily_button_func(ar)
            # target_day = cls.get_row_by_pk(ar, obj.pk + int(wd.value) - 1)
            target_day = Day(obj.pk + int(wd.value) - 1, ar, "day", mi.planner)
            today = target_day.date

            cls.update_row_meta(today, ar)

            qs = qs.filter(start_date=today)
            qs = qs.order_by('start_time')
            mdes = qs.filter(end_date__isnull=False)
            mdes = mdes.order_by('-end_date')
            qs = qs.filter(end_date__isnull=True)

            if today.weekday() == 0 and (current_month > today.month
                                         or today.day == 1):
                cls.mde_pops = [[[] for i in range(7)] for i in range(5)]
                cls.week_offset = today.isocalendar()[1] % 5

            chunks = []
            uncolored_mdes = []
            week_index = (today.isocalendar()[1] - cls.week_offset) % 5
            twd = today.weekday()

            chunks += cls.mde_pops[week_index][today.weekday()]

            for e in mdes:
                color = e.get_display_color()
                if not color:
                    uncolored_mdes.append(e)
                    continue
                wi = week_index
                days = (e.end_date - e.start_date).days
                max_count = len(cls.mde_pops[wi][twd]) + 1
                for i in range(days + 1):
                    mde_pos = (twd + i) % 7
                    wi = week_index + ((twd + i) // 7)
                    if wi >= 5:
                        break
                    if mde_pos == 0 and i > 0:
                        max_count = len(cls.mde_pops[wi][mde_pos]) + 1
                        remains = days - i
                        cols = 6 if remains >= 6 else remains
                        style = (
                            f"margin-right:-{100 * cols}%;"
                            + "position: relative;padding: 0 5px;"
                            + f"background:{color.value};"
                            + f"color:{color.font_color};"
                            + "border-radius: 5px;height: 1.2em;")
                        cls.mde_pops[wi][mde_pos].append(
                            e.as_summary_item(ar, E.div("\u00A0", style=style)))
                    elif i != 0:
                        cls.mde_pops[wi][mde_pos].append(
                            E.div("\u00A0", style="height: 1.2em;"))
                        elem_count = len(cls.mde_pops[wi][mde_pos])
                        if elem_count < max_count:
                            for i in range(max_count - elem_count):
                                cls.mde_pops[wi][mde_pos].append(
                                    E.div("\u00A0", style="height: 1.2em;"))
                cols = 6 - twd if days + twd > 7 else days
                style = f"margin-right:-{100 * cols}%;position:" \
                    + "relative;padding:0 5px;border-radius:5px;"
                chunks.append(
                    e.as_summary_item(
                        ar,
                        cls.get_calview_div(e,
                                            ar,
                                            today,
                                            passed_style=style,
                                            mde=True)))

            for e in uncolored_mdes:
                chunks.append(e.as_summary_item(ar, cls.get_calview_div(e, ar,
                                                                        today)))

            chunks += [
                e.as_summary_item(ar, cls.get_calview_div(e, ar, today))
                for e in qs
            ]

            # pk = date2pk(target_day)

            daily_link = daily_button_func(target_day, str(today.day))
            if today == dd.today():
                daily_link = E.b(daily_link)

            header_items = [daily_link]
            btn = ar.gen_insert_button(Events, start_date=target_day.date)
            if btn is not None:
                header_items.append(btn)

            header = E.div(*header_items, align="center", CLASS="header")
            # return E.table(E.tr(E.td(*[header, E.div(*join_elems(chunks), style="overflow: visible;")])),
            #                CLASS="fixed-table cal-month-cell {} {} {}".format(
            #                  "current-month" if current_month == target_day.date.month else "other-month",
            #                  "current-day" if target_day.date == today else "",
            #                  "cal-in-past" if target_day.date < today else ""
            #              ))

            chunks.insert(0, header)

            return format_html(BOXWRAP, tostring(chunks))

        return dd.VirtualField(dd.HtmlBox(wd.text), func)


class DailyPlanner(ParameterClone, DailySlaveBase, DailyPlannerRows):
    # default_display_modes = {None: constants.DISPLAY_MODE_HTML}
    navigation_mode = 'day'


class DailySlave(DailyPlanner):

    @classmethod
    def get_title(self, ar):
        return None


class WeeklySlave(ParameterClone, WeeklySlaveBase, DailyPlannerRows):

    @classmethod
    def get_title(self, ar):
        return None


class MonthlySlave(ParameterClone, MonthlySlaveBase, DaysTable):
    # required_roles = dd.login_required(OfficeStaff)
    with_header_row = False
    navigation_mode = "month"

    @classmethod
    def get_title(self, ar):
        return None

    @classmethod
    def get_planner(cls):
        return cls.calendar_view.planner

    @classmethod
    def get_data_rows(cls, ar):
        mi = ar.master_instance  # a Day instance
        if mi is None:
            return

        year, month = mi.date.year, mi.date.month
        # inspired by calendar.Calendar.itermonthdates
        date = datetime.date(year, month, 1)
        # Go back to the beginning of the week
        days = (date.weekday() - CALENDAR.firstweekday) % 7
        date -= datetime.timedelta(days=days)
        # date = CALENDAR.itermonthdates(year, month).next()
        while True:
            yield cls.get_row_by_pk(ar, date2pk(date))
            try:
                date += ONE_WEEK
            except OverflowError:
                # Adding could fail after datetime.MAXYEAR
                break
            if date.month != month and date.weekday() == CALENDAR.firstweekday:
                break

    @dd.displayfield("Week")
    def week_number(cls, obj, ar):
        # obj is the first day of the week
        if not isinstance(obj, Day):
            raise Exception("{} is not a Day".format(obj))
        if ar.param_values is None:
            return None
        label = str(obj.date.isocalendar()[1])
        # label = str(week[0].isocalendar()[1])
        # pk = date2pk(week[0])
        pk = date2pk(obj.date)
        # nav = ar.master_instance.ar.actor.planner  # 20200224
        # daily, weekly, monthly = nav.make_link_funcs(ar)
        weekly = obj.planner.weekly_button_func(ar)
        # weekly = nav.weekly_button_func(ar)
        link = weekly(Day(pk, ar, navigation_mode="week"), label)
        # link = label
        return E.div(*[link], style="text-align:center; padding:6pt 0")
        # return E.div(*[link], style="text-align: center; display: flex; justify-content: center; align-items: center;")

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        u = ar.get_user()
        if u.is_anonymous:
            raise Exception("20230113")
        kw.update(user=u)
        return kw


class DayDetail(dd.DetailLayout):
    main = "body"
    body = "calview.DailySlave"


class WeekDetail(dd.DetailLayout):
    main = "body"
    # body = dd.Panel("navigation_panel:15 calview.WeeklySlave:85", label=_("Planner"))
    body = "calview.WeeklySlave"


class MonthDetail(dd.DetailLayout):
    main = "body"
    body = "calview.MonthlySlave"


class DailyView(ParameterClone, CalendarView):
    # label = _("Daily view")
    detail_layout = 'calview.DayDetail'
    navigation_mode = "day"
    insert_event = InsertEvent()


class WeeklyView(ParameterClone, CalendarView):
    # label = _("Weekly view")
    detail_layout = 'calview.WeekDetail'
    navigation_mode = "week"


class MonthlyView(ParameterClone, CalendarView):
    # label = _("Monthly view")
    detail_layout = 'calview.MonthDetail'
    navigation_mode = "month"
