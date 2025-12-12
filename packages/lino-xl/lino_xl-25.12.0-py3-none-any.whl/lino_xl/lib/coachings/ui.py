# -*- coding: UTF-8 -*-
# Copyright 2008-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino import mixins

from lino.modlib.users.mixins import My
from .roles import CoachingsUser, CoachingsStaff
from .choicelists import *


class CoachingTypes(dd.Table):
    model = 'coachings.CoachingType'
    column_names = 'name does_integ does_gss eval_guestrole *'
    required_roles = dd.login_required(CoachingsStaff)


class CoachingEndings(dd.Table):
    required_roles = dd.login_required(CoachingsStaff)
    model = 'coachings.CoachingEnding'
    column_names = 'seqno name type *'
    order_by = ['seqno']
    detail_layout = """
    id name seqno
    CoachingsByEnding
    """


class Coachings(dd.Table):
    required_roles = dd.login_required(CoachingsStaff)
    model = 'coachings.Coaching'
    no_phantom_row = True

    parameters = mixins.ObservedDateRange(
        coached_by=dd.ForeignKey(
            'users.User',
            blank=True,
            null=True,
            verbose_name=_("Coached by"),
            help_text="""Nur Begleitungen dieses Benutzers."""),
        and_coached_by=dd.ForeignKey(
            'users.User',
            blank=True,
            null=True,
            verbose_name=_("and by"),
            help_text="""... und auch Begleitungen dieses Benutzers."""),
        observed_event=dd.PeriodEvents.field(blank=True, default='active'),
        primary_coachings=dd.YesNo.field(
            _("Primary coachings"),
            blank=True,
            help_text="""Accompagnements primaires."""),
        coaching_type=dd.ForeignKey(
            'coachings.CoachingType',
            blank=True,
            null=True,
            help_text="""Nur Begleitungen dieses Dienstes."""),
        ending=dd.ForeignKey(
            'coachings.CoachingEnding',
            blank=True,
            null=True,
            help_text="""Nur Begleitungen mit diesem Beendigungsgrund."""),
    )
    params_layout = """
    start_date end_date observed_event coached_by and_coached_by
    primary_coachings coaching_type ending
    """
    params_panel_hidden = True

    #~ @classmethod
    #~ def param_defaults(self,ar,**kw):
    #~ kw = super(Coachings,self).param_defaults(ar,**kw)
    #~ D = datetime.date
    #~ kw.update(start_date = D.today())
    #~ kw.update(end_date = D.today())
    #~ return kw

    @classmethod
    def get_request_queryset(self, ar, **filter):
        qs = super().get_request_queryset(ar, **filter)
        if (pv := ar.param_values) is None: return qs
        coaches = []
        for u in (pv.coached_by, pv.and_coached_by):
            if u is not None:
                coaches.append(u)
        if len(coaches):
            qs = qs.filter(user__in=coaches)

        ce = pv.observed_event
        if ce is not None:
            qs = ce.add_filter(qs, pv)

        if pv.primary_coachings == dd.YesNo.yes:
            qs = qs.filter(primary=True)
        elif pv.primary_coachings == dd.YesNo.no:
            qs = qs.filter(primary=False)
        if pv.coaching_type is not None:
            qs = qs.filter(type=pv.coaching_type)
        if pv.ending is not None:
            qs = qs.filter(ending=pv.ending)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super().get_title_tags(ar):
            yield t

        pv = ar.param_values

        if pv.observed_event:
            yield str(pv.observed_event)

        if pv.coached_by:
            s = str(self.parameters['coached_by'].verbose_name) + \
                ' ' + str(pv.coached_by)
            if pv.and_coached_by:
                s += " %s %s" % (_('and'), pv.and_coached_by)
            yield s

        if pv.primary_coachings:
            yield str(self.parameters['primary_coachings'].verbose_name) \
                + ' ' + str(pv.primary_coachings)

    @classmethod
    def get_create_permission(self, ar):
        """Reception clerks can see coachings, but cannot modify them nor add
        new ones.

        """

        if not ar.get_user().user_type.has_required_roles([CoachingsUser]):
            #if not ar.get_user().user_type.coaching_level:
            return False
        return super().get_create_permission(ar)


class CoachingsByClient(Coachings):
    required_roles = dd.login_required()
    #~ debug_permissions = 20121016
    master_key = 'client'
    order_by = ['start_date']
    column_names = 'start_date end_date user:12 primary type:12 ending id'
    hidden_columns = 'id'
    auto_fit_column_widths = True


class CoachingsByEnding(Coachings):
    master_key = 'ending'


class CoachingsByUser(Coachings):
    required_roles = dd.login_required(CoachingsUser)
    master_key = 'user'
    column_names = 'start_date end_date client type primary id'

    @classmethod
    def setup_request(self, ar):  # 20230221
        if ar.master_instance is None:
            ar.master_instance = ar.get_user()
        #~ print "20120519 MyOutbox.setup_request()", ar.master_instance
        super().setup_request(ar)


class MyCoachings(My, CoachingsByUser):
    column_names = 'client start_date end_date type primary id'
    order_by = ['client__name']

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(start_date=dd.today())
        kw.update(end_date=dd.today())
        return kw
