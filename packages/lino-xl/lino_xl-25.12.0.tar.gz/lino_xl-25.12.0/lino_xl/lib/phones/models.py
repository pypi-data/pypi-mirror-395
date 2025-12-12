# -*- coding: UTF-8 -*-
# Copyright 2017-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models

from lino.api import dd, rt, gettext, _
from lino.core import constants
from lino.core.diff import ChangeWatcher
from lino.core.roles import SiteStaff
from lino.mixins.periods import DateRange
from lino.modlib.checkdata.choicelists import Checker
from lino.modlib.system.choicelists import PeriodEvents
from lino.utils.html import E, tostring, join_elems

from .choicelists import ContactDetailTypes
from .mixins import ContactDetailsOwner


class ContactDetail(DateRange):

    class Meta:
        app_label = 'phones'
        verbose_name = _("Contact detail")
        verbose_name_plural = _("Contact details")

    detail_type = ContactDetailTypes.field(default='email')
    partner = dd.ForeignKey(dd.plugins.phones.partner_model,
                            related_name='phones_by_partner')
    value = dd.CharField(_("Value"), max_length=200, blank=True)
    remark = dd.CharField(_("Remark"), max_length=200, blank=True)
    primary = models.BooleanField(_("Primary"), default=False)
    # end_date = models.DateField(_("Until"), blank=True, null=True)

    allow_cascaded_delete = ['partner']

    def __str__(self):
        return self.detail_type.format(self.value)

    def full_clean(self):
        super(ContactDetail, self).full_clean()
        self.detail_type.validate(self.value)

    def after_ui_save(self, ar, cw):
        super(ContactDetail, self).after_ui_save(ar, cw)
        mi = self.partner
        if mi is None:
            return
        if self.primary and self.detail_type:
            for o in mi.phones_by_partner.exclude(id=self.id).filter(
                    detail_type=self.detail_type):
                if o.primary:
                    o.primary = False
                    o.save()
                    ar.set_response(refresh_all=True)
        k = self.detail_type.field_name
        if k:
            watcher = ChangeWatcher(mi)
            setattr(mi, k, self.value)
            watcher.send_update(ar)
            mi.save()

    @classmethod
    def get_simple_parameters(cls):
        for p in super(ContactDetail, cls).get_simple_parameters():
            yield p
        yield 'partner'
        yield 'detail_type'

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(observed_event=PeriodEvents.field(blank=True))
        super(ContactDetail, cls).setup_parameters(fields)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super(ContactDetail, cls).get_request_queryset(ar, **filter)
        if (pv := ar.param_values) is None:
            return qs
        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)
        return qs


@dd.receiver(dd.pre_ui_delete, sender=ContactDetail)
def clear_partner_on_delete(sender=None, request=None, **kw):
    self = sender
    mi = self.partner
    if mi:
        mi.propagate_contact_detail(self.detail_type)


class ContactDetails(dd.Table):
    model = 'phones.ContactDetail'
    required_roles = dd.login_required(SiteStaff)
    column_names = "value:30 detail_type:10 remark:10 partner id primary *"
    insert_layout = """
    detail_type
    value
    remark
    """
    detail_layout = dd.DetailLayout("""
    partner
    detail_type
    value
    remark
    start_date end_date
    """,
                                    window_size=(60, 'auto'))
    params_layout = "observed_event start_date end_date partner detail_type"


class ContactDetailsByPartner(ContactDetails):
    required_roles = dd.login_required()
    master_key = 'partner'
    column_names = 'detail_type:10 value:30 primary:5 end_date remark:10 *'
    label = _("Contact details")
    auto_fit_column_widths = True
    stay_in_grid = True
    window_size = (80, 20)

    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}

    @classmethod
    def table_as_summary(self, ar):
        items = [o.detail_type.as_html(o, ar) for o in ar if not o.end_date]

        html = []
        if len(items) == 0:
            html.append(gettext("No contact details"))
        else:
            html += join_elems(items, sep=', ')

        ins = self.insert_action.request_from(ar)
        if ins.get_permission():
            btn = ins.ar2button()
            html.append(' ')
            html.append(btn)

        html.append(' ')
        html.append(ar.as_button(icon_name="wrench",
                                 title=_("Manage contact details")))  # GEAR
        return tostring(html)


FIX_D2O = True  # Fix differences by synchronizing details to owner


class ContactDetailsOwnerChecker(Checker):
    verbose_name = _("Check for mismatches between contact details and owner")
    model = ContactDetailsOwner
    # msg_mismatch = _("Field differs from primary item")
    msg_mismatch = _("{} is {} on owner but {} on primary item")
    # msg_empty = _("{} is empty on owner but primary item exists")
    msg_missing = _("Missing primary item")
    msg_multiple = _("Multiple primary items for {}")

    def get_checkdata_problems(self, ar, obj, fix=False):
        # dd.logger.info("20171013 Checking {}", obj)
        ContactDetailTypes = rt.models.phones.ContactDetailTypes
        ContactDetail = rt.models.phones.ContactDetail
        for cdt in ContactDetailTypes.get_list_items():
            k = cdt.field_name
            if k:
                value = getattr(obj, k)
                kw = dict(partner=obj, primary=True, detail_type=cdt)
                try:
                    cd = ContactDetail.objects.get(**kw)
                    # if value:
                    if cd.value != value:
                        yield (FIX_D2O,
                               self.msg_mismatch.format(cdt, value, cd.value))
                        if FIX_D2O and fix:
                            setattr(obj, k, cd.value)
                            obj.full_clean()
                            obj.save()
                    # else:
                    #     yield (FIX_D2O, self.msg_empty)
                    #     if FIX_D2O and fix:
                    #         setattr(obj, k, cd.value)
                    #         obj.full_clean()
                    #         obj.save()
                except ContactDetail.DoesNotExist:
                    if value:
                        yield (True, self.msg_missing)
                        if fix:
                            kw.update(value=value)
                            cd = ContactDetail(**kw)
                            cd.save()
                except ContactDetail.MultipleObjectsReturned:
                    yield (False, self.msg_multiple.format(cdt))


ContactDetailsOwnerChecker.activate()
