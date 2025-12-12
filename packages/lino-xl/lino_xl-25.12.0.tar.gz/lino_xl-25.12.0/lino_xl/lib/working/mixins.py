# -*- coding: UTF-8 -*-
# Copyright 2016-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.exceptions import ValidationError
from lino.modlib.summaries.mixins import Summarized
from lino.utils.quantities import ZERO_DURATION
from lino.api import dd, rt, _

from .actions import StartTicketSession, EndTicketSession


class Workable(dd.Model):

    class Meta:
        abstract = True

    create_session_on_create = False

    def get_ticket(self):
        return self

    def is_workable_for(self, user):
        return True

    if dd.is_installed('working'):

        start_session = StartTicketSession()
        end_session = EndTicketSession()

        def disabled_fields(self, ar):
            s = super().disabled_fields(ar)
            user = ar.get_user()
            if not (user.is_authenticated and self.is_workable_for(user)):
                s.add('start_session')
                s.add('end_session')
                return s
            ticket = self.get_ticket()
            if ticket is None or ticket.pk is None:
                return s
            Session = rt.models.working.Session
            qs = Session.objects.filter(user=user,
                                        ticket=ticket,
                                        end_time__isnull=True)
            if qs.exists():
                s.add('start_session')
            else:
                s.add('end_session')
            return s

        def save_new_instance(elem, ar):
            super().save_new_instance(ar)

            if rt.settings.SITE.loading_from_dump:
                return
            me = ar.get_user()
            # print elem.create_session_on_create
            if elem.create_session_on_create and me is not None and me.open_session_on_new_ticket:
                ses = rt.models.working.Session(ticket=elem, user=me)
                ses.full_clean()
                ses.save()

    def get_reporting_type(self):
        return dd.plugins.working.default_reporting_type
        

class SummarizedFromSession(Summarized):

    class Meta:
        abstract = True

    def add_from_session(self, obj):
        d = obj.get_duration()
        if d:
            rt = obj.get_reporting_type()
            k = rt.name + '_hours'
            value = getattr(self, k) or ZERO_DURATION
            if value == -1:
                return
            value += d
            # fld = self._meta.get_field(k)
            # try:
            #     value = fld.clean(value, self)
            #     # print("20221107 {} is okay".format(value))
            # except ValidationError as e:
            #     print(e)
            #     value = -1
            setattr(self, k, value)
