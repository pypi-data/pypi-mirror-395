# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db.models import Q
from lino.mixins import BabelDesignated, Sequenced
from lino.api import dd, rt, _
from lino.modlib.system.choicelists import DisplayColors
from .mixins import Plannable, Planners, Day
from .ui import *


class DailyPlannerRow(BabelDesignated, Sequenced, Plannable):

    # TODO: rename this to TimeSlot. A time slot is "a time when something can
    # happen or is planned to happen, especially when it is one of several
    # possible times"
    # (https://dictionary.cambridge.org/dictionary/english/time-slot) or "a time
    # assigned on a schedule or agenda"
    # (https://www.vocabulary.com/dictionary/time%20slot)

    class Meta:
        app_label = 'calview'
        abstract = dd.is_abstract_model(__name__, 'DailyPlannerRow')
        verbose_name = _("Planner row")
        verbose_name_plural = _("Planner rows")
        ordering = ['start_time', '-seqno']

    start_time = dd.TimeField(blank=True,
                              null=True,
                              verbose_name=_("Start time"))
    end_time = dd.TimeField(blank=True, null=True, verbose_name=_("End time"))

    # def get_weekly_chunks(obj, ar, qs, today):
    #     if obj.start_time:
    #         qs = qs.filter(start_time__gte=obj.start_time,
    #                        start_time__isnull=False)
    #     if obj.end_time:
    #         qs = qs.filter(start_time__lt=obj.end_time,
    #                        start_time__isnull=False)
    #     return [e.as_summary_item(ar, ar.actor.get_calview_div(e, ar)) for e in qs]
    #
    @classmethod
    def get_plannable_entries(cls, obj, qs, ar):
        # qs = rt.models.cal.Event.objects.all()
        if obj is cls.HEADER_ROW:
            return qs.filter(
                Q(start_time__isnull=True) | Q(end_date__isnull=False))
        if obj.start_time:
            qs = qs.filter(start_time__gte=obj.start_time,
                           start_time__isnull=False)
        if obj.end_time:
            qs = qs.filter(start_time__lt=obj.end_time,
                           start_time__isnull=False)
        return qs


dd.update_field(DailyPlannerRow, 'overview', verbose_name=_("Time range"))


# DailyPlannerRow.install_actors(globals())

dd.inject_field('system.SiteConfig', 'default_color',
                DisplayColors.field(_("Color"), default='blue'))
