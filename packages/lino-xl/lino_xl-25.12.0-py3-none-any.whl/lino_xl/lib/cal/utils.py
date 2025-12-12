# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Some calendar utilities.

See :ref:`book.specs.cal`.

"""

import datetime
from dateutil.tz import tzlocal
from dateutil.parser import parse
from typing import Union, Any

from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_str

from lino.utils.format_date import format_date
from lino.utils.format_date import fds
from lino.utils.format_date import day_and_month, day_and_weekday

from lino.api import rt


def aware(d):
    "Convert the given datetime into a timezone-aware datetime."
    return datetime.datetime(d.year, d.month, d.day, tzinfo=tzlocal())


def dt2kw(dt, name, **d):
    """Store given timestamp `dt` in a field dict.  `name` is the base
    name of the fields.

    """
    if dt:
        if isinstance(dt, datetime.datetime):
            d[name + '_date'] = dt.date()
            if dt.time():
                d[name + '_time'] = dt.time()
            else:
                d[name + '_time'] = None
        elif isinstance(dt, datetime.date):
            d[name + '_date'] = dt
            d[name + '_time'] = None
        else:
            raise Exception("Invalid datetime value %r" % dt)
    else:
        d[name + '_date'] = None
        d[name + '_time'] = None
    return d


def setkw(obj, **kw):
    for k, v in kw.items():
        setattr(obj, k, v)


def when_text(d, t=None):
    """Return a string with a concise representation of the given date
    and time combination.

    """
    if d is None:
        return ''
    # fmt = 'yyyy MMM dd (EE)'
    # txt = d.strftime(settings.SITE.date_format_strftime)
    txt = format_date(d, 'EE ')
    txt += fds(d)
    if t is not None:
        txt += ' (%s)' % t.strftime(settings.SITE.time_format_strftime)
    return txt


def update_auto_event(autotype, user, date, summary, owner, **defaults):
    return update_auto_component(rt.models.cal.Event, autotype, user, date,
                                 summary, owner, **defaults)


def update_auto_task(autotype, user, date, summary, owner, **defaults):
    Task = rt.models.cal.Task
    return update_auto_component(Task, autotype, user, date, summary, owner,
                                 **defaults)


def update_auto_component(model, autotype, user, date, summary, owner,
                          **defaults):
    """
    Creates, updates or deletes the
    automatic :class:`calendar component <Component>`
    of the specified `auto_type` and `owner`.

    Specifying `None` for `date` means that
    the automatic component should be deleted.
    """
    #~ print "20120729 update_auto_component", model,autotype,user, date, settings.SITE.loading_from_dump
    #~ if SKIP_AUTO_TASKS: return
    if settings.SITE.loading_from_dump:
        #~ print "20111014 loading_from_dump"
        return None
    ContentType = rt.models.contenttypes.ContentType
    ot = ContentType.objects.get_for_model(owner.__class__)
    if date and date >= settings.SITE.today() + datetime.timedelta(days=-7):
        #~ defaults = owner.get_auto_task_defaults(**defaults)
        #~ print "20120729 b"
        defaults.setdefault('user', user)
        obj, created = model.objects.get_or_create(defaults=defaults,
                                                   owner_id=owner.pk,
                                                   owner_type=ot,
                                                   auto_type=autotype)
        if not obj.is_user_modified():
            original_state = dict(obj.__dict__)
            if obj.user != user:
                obj.user = user
            summary = force_str(summary)
            if obj.summary != summary:
                obj.summary = summary
            if obj.start_date != date:
                obj.start_date = date
            if created or obj.__dict__ != original_state:
                #~ obj.full_clean()
                obj.save()
        return obj
    else:
        #~ print "20120729 c"
        # delete task if it exists
        try:
            obj = model.objects.get(owner_id=owner.pk,
                                    owner_type=ot,
                                    auto_type=autotype)
        except model.DoesNotExist:
            pass
        else:
            if not obj.is_user_modified():
                obj.delete()


def update_reminder(type, owner, user, orig, msg, num, unit):
    """
    Shortcut for calling :func:`update_auto_task`
    for automatic "reminder tasks".
    A reminder task is a message about something that will
    happen in the future.
    """
    update_auto_task(type, user, unit.add_duration(orig, -num), msg, owner)


def resolve_datetime(s: str) -> Union[datetime.datetime, datetime.date]:
    dt = parse(s)
    try:
        dt = timezone.make_naive(dt)
    except:
        pass
    try:
        dt = timezone.make_aware(dt)
    except:
        pass
    return dt


RRULE_RESOLVE = dict(
    FREQ=lambda x: rt.models.system.Recurrences.get_by_name(x.lower()),
    UNTIL=lambda x: resolve_datetime(x),
    COUNT=lambda x: int(x),
    INTERVAL=lambda x: int(x),
    BYSECOND=lambda x: [int(i) for i in x.split(',')],
    BYMINUTE=lambda x: [int(i) for i in x.split(',')],
    BYHOUR=lambda x: [int(i) for i in x.split(',')],
    # week num (allows negative indexing) weekday ; weekday = "SU" / "MO" / "TU" / "WE" / "TH" / "FR" / "SA"
    BYDAY=lambda x: [(int(i[:-2]) if i[:-2] != "" else None, i[-2:])
                     for i in x.split(',')],
    BYMONTHDAY=lambda x: [int(i) for i in x.split(',')],
    BYYEARDAY=lambda x: [int(i) for i in x.split(',')],
    BYWEEKNO=lambda x: [int(i) for i in x.split(',')],
    BYMONTH=lambda x: [int(i) for i in x.split(',')],
    BYSETPOS=lambda x: [int(i) for i in x.split(',')],
    WKST=lambda x: x.split(','))


def parse_rrule(
    rr: str
) -> tuple[Any, int, Union[int, datetime.datetime, datetime.date], dict]:
    """

    Parse the given :term:`recurrence rule` and returns a tuple of `(every_unit,
    every, max_events, keywords)` where keywords is ...

    """

    # The standards from below specification has been followed while writing this parser
    #
    assert rr.startswith('RRULE:')
    rule = rr.split(':')[1]
    every_unit = None
    every = 1
    limit = None
    kw = dict()
    for item in rule.split(';'):
        key, value = item.split('=')
        if key == 'FREQ':
            every_unit = RRULE_RESOLVE[key](value)
        elif key == 'INTERVAL':
            every = RRULE_RESOLVE[key](value)
        elif key == 'UNTIL':
            limit = RRULE_RESOLVE[key](value)
        elif key == 'COUNT':
            limit = RRULE_RESOLVE[key](value)
        else:
            kw[key] = RRULE_RESOLVE[key](value)
    return every_unit, every, limit, kw
