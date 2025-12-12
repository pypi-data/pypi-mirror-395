# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Create some meetings.

"""

from lino.api import dd, rt
from lino.utils import Cycler


def objects():

    if dd.get_plugin_setting('cal', 'with_demo_appointments'):

        meetings = Cycler(dd.plugins.agenda.meeting_model.objects.filter(
            event_type__is_public=True))
        if len(meetings) == 0:
            print("There are no public meetings")
            return
        topics = Cycler(dd.plugins.agenda.topic_model.objects.all())

        for i in range(12):
            m = meetings.pop()
            for j in range(3 + i % 5):
                yield rt.models.agenda.Item(meeting=m, topic=topics.pop())
