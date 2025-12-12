# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import sys
from django.conf import settings
from django.db import models
from django.utils import timezone

try:
    from googleapiclient.errors import HttpError
except:
    HttpError = Exception
from typing import NamedTuple

from etgen.html2rst import RstTable
from lino.utils.html import E, tostring
from lino.mixins import Created, Modified
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.users.models import User
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino.api import rt, dd, _
# from lino.core.roles import SiteAdmin, SiteStaff

from .utils import make_api_call, get_credentials, build, update_creds
from .choicelists import AccessRoles, google_status
from .mixins import GoogleContactSynchronized, SyncToken
from .exceptions import AccessLocked

from lino import logger

if dd.is_installed("cal"):

    from lino_xl.lib.cal.models import BaseSubscription

    class CalendarSubscription(BaseSubscription):

        class Meta:
            app_label = "google"
            abstract = dd.is_abstract_model(__name__, "CalendarSubscription")

        primary = dd.BooleanField(default=False)
        access_role = AccessRoles.field(default='owner')

    class EventSyncToken(SyncToken):

        class Meta:
            abstract = dd.is_abstract_model(__name__, 'EventSyncToken')
            app_label = 'google'
            unique_together = ['subscription']

        subscription = dd.ForeignKey('google.CalendarSubscription')

    class CalendarSyncToken(SyncToken):

        class Meta:
            abstract = dd.is_abstract_model(__name__, 'CalendarSyncToken')
            app_label = 'google'
            unique_together = ['user']

    class DeletedEntry(dd.Model):

        class Meta:
            app_label = "google"
            abstract = dd.is_abstract_model(__name__, "DeletedEntry")

        calendar = dd.BooleanField(default=False)
        user = dd.ForeignKey('users.User', null=False, blank=False)
        event_id = dd.CharField(max_length=200, blank=True, null=True)
        calendar_id = dd.CharField(max_length=200)


class Contact(UserAuthored, GoogleContactSynchronized, Modified):
    allow_cascaded_delete = ["contact"]
    quick_search_fields = "contact__name"

    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "Contact")

    contact = dd.ForeignKey(dd.plugins.google.contacts_model)


class DeletedContact(UserAuthored):

    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "DeletedContact")

    contact_id = dd.CharField(max_length=200)


class ContactSyncToken(SyncToken):

    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "ContactSyncToken")
        unique_together = ['user']


def get_user_country(self):
    if self.partner is None or self.partner.country is None:
        return None
    return self.partner.country


User.get_country = get_user_country


class SyncSummary(UserAuthored, Created):

    class Meta:
        app_label = 'google'
        abstract = dd.is_abstract_model(__name__, 'SyncSummary')
        verbose_name = _("Sync Summary")
        verbose_name_plural = _("Sync Summaries")

    show_in_site_search = False

    halted = dd.BooleanField(_("Failed"), default=False, editable=False)
    stats = dd.RichTextField(editable=False)


class FailedForeignItem(dd.Model):

    class Meta:
        app_label = 'google'
        abstract = dd.is_abstract_model(__name__, 'FailedForeignItem')
        verbose_name = _("Failed Foreign Item")
        verbose_name_plural = _("Failed Foreign Items")

    job = dd.ForeignKey("google.SyncSummary")
    value = models.JSONField()
    item_class = dd.ForeignKey("contenttypes.ContentType")


class FailedEntries(NamedTuple):
    calendars = []
    events = []
    contacts = []
    foreign_items = []  # list[tuple[dd.Model, dict]]


class Stats(object):
    calendars__in_insert = 0
    calendars__in_update = 0
    events__in_insert = 0
    events__in_update = 0
    contacts__in_insert = 0
    contacts__in_update = 0
    calendars_deleted__in = 0
    events_deleted__in = 0
    contacts_deleted__in = 0
    calendars__out_insert = 0
    calendars__out_update = 0
    events__out_insert = 0
    events__out_update = 0
    contacts__out_insert = 0
    contacts__out_update = 0
    calendars_deleted__out = 0
    events_deleted__out = 0
    contacts_deleted__out = 0

    @property
    def calendars(self):
        return (self.calendars_deleted__out + self.calendars_deleted__in +
                self.calendars__out_update + self.calendars__out_insert +
                self.calendars__in_insert + self.calendars__in_update)

    @property
    def events(self):
        return (self.events_deleted__out + self.events_deleted__in +
                self.events__out_update + self.events__out_insert +
                self.events__in_insert + self.events__in_update)

    @property
    def contacts(self):
        return (self.contacts_deleted__out + self.contacts_deleted__in +
                self.contacts__out_update + self.contacts__out_insert +
                self.contacts__in_insert + self.contacts__in_update)

    def to_rst(self):
        return RstTable(["", "Calendars", "Events", "Contacts"]).to_rst(
            [[
                "Inserted (inward)", self.calendars__in_insert,
                self.events__in_insert, self.contacts__in_insert
            ],
             [
                 "Inserted (outward)", self.calendars__out_insert,
                 self.events__out_insert, self.contacts__out_insert
             ],
             [
                 "Updated (inward)", self.calendars__in_update,
                 self.events__in_update, self.contacts__in_update
             ],
             [
                 "Updated (outward)", self.calendars__out_update,
                 self.events__out_update, self.contacts__out_update
             ],
             [
                 "Deleted (inward)", self.calendars_deleted__in,
                 self.events_deleted__in, self.contacts_deleted__in
             ],
             [
                 "Deleted (outward)", self.calendars_deleted__out,
                 self.events_deleted__out, self.contacts_deleted__out
             ], ["", "", "", ""],
             ["Total modified", self.calendars, self.events, self.contacts]])

    def to_html(self):
        return E.table(
            E.thead(
                E.tr(E.th(), E.th("Calendars"), E.th("Events"),
                     E.th("Contacts"))),
            E.tbody(
                E.tr(E.td("Inserted (inward)"),
                     E.td(str(self.calendars__in_insert)),
                     E.td(str(self.events__in_insert)),
                     E.td(str(self.contacts__in_insert))),
                E.tr(E.td("Inserted (outward)"),
                     E.td(str(self.calendars__out_insert)),
                     E.td(str(self.events__out_insert)),
                     E.td(str(self.contacts__out_insert))),
                E.tr(E.td("Updated (inward)"),
                     E.td(str(self.calendars__in_update)),
                     E.td(str(self.events__in_update)),
                     E.td(str(self.contacts__in_update))),
                E.tr(E.td("Updated (outward)"),
                     E.td(str(self.calendars__out_update)),
                     E.td(str(self.events__out_update)),
                     E.td(str(self.contacts__out_update))),
                E.tr(E.td("Deleted (inward)"),
                     E.td(str(self.calendars_deleted__in)),
                     E.td(str(self.events_deleted__in)),
                     E.td(str(self.contacts_deleted__in))),
                E.tr(E.td("Deleted (outward)"),
                     E.td(str(self.calendars_deleted__out)),
                     E.td(str(self.events_deleted__out)),
                     E.td(str(self.contacts_deleted__out))),
                E.tr(E.td(), E.td(), E.td(), E.td()),
                E.tr(E.td("Total modified"), E.td(str(self.calendars)),
                     E.td(str(self.events)), E.td(str(self.contacts)))))


class Synchronizer:

    logging_frequency = None

    _failed_entries = None
    _stats = None
    _errors = ""
    current_item_class = None
    current_item = None
    errors = ""
    failed_entries = None
    stats = None
    user = None
    credentials = None

    def __init__(self, user=None, logging_frequency=None):
        if user is not None:
            self.setup(user, logging_frequency)

    def setup(self, user, logging_frequency=None):
        self.clear()
        self.user = user
        self.stats = Stats()
        self.failed_entries = FailedEntries()
        self.credentials = get_credentials(user)
        self.logging_frequency = (logging_frequency
                                  if logging_frequency is not None else
                                  dd.plugins.google.sync_logging_frequency)

    def handle_api_error_message(self, error, *args, **kwargs):
        msg = f"Failed to do outward sync:\n{self.current_item_class}\n" \
            f"{self.current_item}\nReason: {error.reason}\n\n"
        self.errors += msg
        return msg

    def make_api_call(self, *args, **kwargs):
        kwargs.update(msg_fn=self.handle_api_error_message)
        return make_api_call(*args, **kwargs)

    def has_scope_contacts(self):
        return dd.plugins.google.has_scope('contact', self.user)

    def has_scope_calendar(self):
        return dd.plugins.google.has_scope('calendar', self.user)

    def pull_events(self, resource, sub, room):
        Event = rt.models.cal.Event
        self.current_item_class = Event
        token, created = rt.models.google.EventSyncToken.objects.get_or_create(
            user=sub.user, subscription=sub)
        if created:
            token.lock()

        def sync10():
            events = self.make_api_call(lambda: resource.events().list(
                calendarId=sub.calendar.google_id,
                maxResults=10,
                showDeleted=True,
                syncToken=token.sync_token,
                pageToken=token.page_token))
            token.sync_token = events.get('nextSyncToken') or token.sync_token

            if items := events['items']:
                for item in items:
                    self.current_item = item
                    try:
                        Event.insert_or_update_google_event(item,
                                                            room,
                                                            synchronizer=self)
                        if (evs := self.stats.events
                            ) % self.logging_frequency == 0:
                            logger.info(
                                "google.Synchronizer (%s): synchronized %s events so far.",
                                self.user, evs)
                    except Exception as e:
                        self.failed_entries.foreign_items.append((Event, item))
                        logger.exception(e)
                        logger.error(f"failed cal.Event item: {item}")
                        raise e

            if next_page_token := events.get('nextPageToken'):
                token.page_token = next_page_token
                sync10()
            else:
                token.page_token = None

        try:
            sync10()
        finally:
            token.save()

    def sync_calendar(self):
        logger.info(f"Synchronizing google calendar for user: {self.user}")
        gcal = build("calendar", "v3", credentials=self.credentials)

        Calendar = rt.models.cal.Calendar
        CalendarSubscription = rt.models.google.CalendarSubscription
        Event = rt.models.cal.Event
        token, created = rt.models.google.CalendarSyncToken.objects.get_or_create(
            user=self.user)
        if created:
            token.lock()

        # Outward sync

        if not settings.SITE.is_demo_site:
            cal_res = gcal.calendars()
            ers = gcal.events()

            calendar_qs = Calendar.get_outward_insert_update_queryset(
                self.user)
            event_qs = Event.get_outward_insert_update_queryset(self.user)
            synched_cals = []
            synched_events = []

            try:
                Event.sync_deleted_records(ers, self)
                Calendar.sync_deleted_records(cal_res, self)

                self.current_item_class = Calendar
                for c in calendar_qs:
                    self.current_item = c
                    c.insert_or_update_into_google(cal_res, synchronizer=self)
                    synched_cals.append(c.pk)
                    if (cs := self.stats.calendars
                        ) % self.logging_frequency == 0:
                        logger.info(
                            "google.Synchronizer (%s): synchronized %s calendars so far.",
                            self.user, cs)

                self.current_item_class = Event
                for e in event_qs:
                    self.current_item = e
                    e.insert_or_update_into_google(ers, synchronizer=self)
                    synched_events.append(e.pk)
                    if (evs :=
                            self.stats.events) % self.logging_frequency == 0:
                        logger.info(
                            "google.Synchronizer (%s): synchronized %s events so far.",
                            self.user, evs)

            except Exception as e:
                if (calendar_qs :=
                        calendar_qs.exclude(pk__in=synched_cals)).count():
                    self.failed_entries.calendars.append(calendar_qs)

                if (event_qs :=
                        event_qs.exclude(pk__in=synched_events)).count():
                    self.failed_entries.events.append(event_qs)

                token.save()
                raise e

        # Inward sync

        def sync10():
            self.current_item_class = Calendar
            self.current_item = None
            try:
                cals = self.make_api_call(lambda: gcal.calendarList().list(
                    maxResults=10,
                    syncToken=token.sync_token,
                    showDeleted=True,
                    showHidden=True,
                    pageToken=token.page_token))
            except HttpError:
                return

            for cal in cals.get("items", []):
                if cal.get("deleted", False):
                    Calendar.delete_google_calendar(cal, self)
                    self.stats.calendars_deleted__in += 1
                    if (cs := self.stats.calendars
                        ) % self.logging_frequency == 0:
                        logger.info(
                            "google.Synchronizer (%s): synchronized %s calendars so far.",
                            self.user, cs)
                    continue
                self.current_item = cal
                try:
                    calendar, _ = Calendar.insert_or_update_google_calendar(
                        cal, synchronizer=self)
                except Exception as e:
                    logger.exception(e)
                    logger.error(f"failed calendar item: {cal}")
                    return

                if (cs := self.stats.calendars) % self.logging_frequency == 0:
                    logger.info(
                        "google.Synchronizer (%s): synchronized %s calendars so far.",
                        self.user, cs)

                try:
                    subscription = CalendarSubscription.objects.get(
                        user=self.user, calendar=calendar)
                except CalendarSubscription.DoesNotExist:
                    subscription = CalendarSubscription(user=self.user,
                                                        calendar=calendar)
                    ar = CalendarSubscription.get_default_table().create_request(
                        user=self.user)
                    subscription.full_clean()
                    subscription.save_new_instance(ar)
                subscription.primary = cal.get("primary", False)
                subscription.access_role = cal.get("accessRole", "reader")
                subscription.full_clean()
                subscription.save()

            if next_page_token := cals.get('nextPageToken'):
                token.page_token = next_page_token
                sync10()
            else:
                token.page_token = None
                token.sync_token = cals.get('nextSyncToken')

        try:
            sync10()
        finally:
            token.save()

        for sub in CalendarSubscription.objects.select_related(
                'calendar').filter(user=self.user):
            self.pull_events(
                gcal, sub,
                sub.calendar.room_calendars.filter(
                    name=sub.calendar.name).order_by('pk').first())

        gcal.close()

    def sync_contacts(self):
        logger.info(f"Synchronizing google contacts for user: {self.user}")
        Contact = rt.models.google.Contact
        self.current_item_class = Contact

        token, created = rt.models.google.ContactSyncToken.objects.get_or_create(
            user=self.user)
        if created:
            token.lock()
        people = build("people", "v1", credentials=self.credentials).people()

        if not settings.SITE.is_demo_site:
            qs = Contact.get_outward_insert_update_queryset(self.user)
            synched = []

            try:
                Contact.sync_deleted_records(people, self)

                for c in qs:
                    self.current_item = c
                    c.insert_or_update_into_google(people, synchronizer=self)
                    synched.append(c.pk)
                    if (cns :=
                            self.stats.contacts) % self.logging_frequency == 0:
                        logger.info(
                            "google.Synchronizer (%s): synchronized %s contacts so far.",
                            self.user, cns)
            except Exception as e:
                if (qs := qs.exclude(pk__in=synched)).count():
                    self.failed_entries.contacts.append(qs)

                token.save()
                raise e

        def sync10():
            try:
                resp = self.make_api_call(lambda: people.connections().list(
                    resourceName="people/me",
                    personFields=Contact.person_fields,
                    pageToken=token.page_token,
                    syncToken=token.sync_token,
                    pageSize=10,
                    requestSyncToken=True))
            except HttpError:
                return

            if "connections" not in resp:
                token.page_token = None
                token.sync_token = resp["nextSyncToken"]
                return resp

            for item in resp["connections"]:
                self.current_item = item
                if (ks := len(item.keys())) == 2:
                    Contact.delete_google_contact(item, synchronizer=self)
                    if (cns :=
                            self.stats.contacts) % self.logging_frequency == 0:
                        logger.info(
                            "google.Synchronizer (%s): synchronized %s contacts so far.",
                            cns, self.user)
                    continue
                assert ks > 2  # probably not needed, keep just to see in case something breaks
                try:
                    Contact.insert_or_update_google_contact(item,
                                                            synchronizer=self)
                except Exception as e:
                    logger.exception(e)
                    logger.error(f"failed contact item: {item}")
                    return

                if (cns := self.stats.contacts) % self.logging_frequency == 0:
                    logger.info(
                        "google.Synchronizer (%s): synchronized %s contacts so far.",
                        self.user, cns)

            if pageToken := resp.get("nextPageToken"):
                token.page_token = pageToken
                sync10()
            else:
                token.page_token = None
                token.sync_token = resp["nextSyncToken"]

        try:
            sync10()
        finally:
            token.save()
            people.close()

    def __call__(self, cal_only=False, contacts_only=False):
        if self.user is None:
            raise Exception(
                "Invalid google.Synchronizer instance, does not have a user scope, please call setup"
            )
        ss = rt.models.google.SyncSummary(user=self.user)
        try:
            if not contacts_only:
                if self.has_scope_calendar():
                    try:
                        self.sync_calendar()
                    except Exception as e:
                        rt.models.google.CalendarSyncToken.objects.filter(
                            user=self.user).update(modified=timezone.now())
                        rt.models.google.EventSyncToken.objects.filter(
                            user=self.user).update(modified=timezone.now())
                        for qs in (self.failed_entries.calendars +
                                   self.failed_entries.events):
                            qs.update(modified=timezone.now())
                        raise e
                else:
                    logger.info(
                        "google.Synchronizer(%s): does not have the "
                        "necessary scopes to sync Google calendar", self.user)

            if not cal_only:
                if self.has_scope_contacts():
                    try:
                        self.sync_contacts()
                    except Exception as e:
                        rt.models.google.ContactSyncToken.objects.filter(
                            user=self.user).update(modified=timezone.now())
                        for qs in self.failed_entries.contacts:
                            qs.update(modified=timezone.now())
                        raise e
                else:
                    logger.info(
                        "google.Synchronizer(%s): does not have the "
                        "necessary scopes to sync Google contacts", self.user
                    )

        except Exception as e:
            logger.exception(e)
            ss.halted = True
            self.errors += dd.read_exception(sys.exc_info())
            # if not isinstance(e, AccessLocked):
            #     raise e
        finally:
            update_creds(self.user, self.credentials)
            ss.stats = tostring(
                E.div(self.stats.to_html(), E.br(),
                      E.div(*[E.p(ln) for ln in self.errors.split('\n')])))
            ss.full_clean()
            ss.save_new_instance(ss.get_default_table().create_request())
            for kls, item in self.failed_entries.foreign_items:
                ffi = rt.models.google.FailedForeignItem(
                    job=ss,
                    value=item,
                    item_class=rt.models.contenttypes.ContentType.objects.
                    get_for_model(kls))
                ffi.full_clean()
                ffi.save_new_instance(ffi.get_default_table().create_request())
            logger.info(
                "google.Synchronizer(): Sync summary ->\n%s",
                self.user, self.stats.to_rst())

        self._failed_entries = self.failed_entries
        self._stats = self.stats
        self._errors = self.errors
        self.failed_entries = None
        self.stats = None
        self.errors = ""
        return self

    def clear(self):
        self._failed_entries = self.failed_entries = self.user = self.stats = self._stats = self.credentials = None
        self.errors = self._errors = ""

    def sync(self, cal_only=False, contacts_only=False):
        self(cal_only, contacts_only)
        self.failed_entries = FailedEntries()
        self.stats = Stats()
        return self


class SynchronizeGoogle(dd.Action):
    help_text = _("Synchronize this database row with Google.")
    label = _("Sync Google")
    select_rows = True
    required_roles = dd.login_required()

    def run_from_ui(self, ar, **kwargs):
        for user in ar.selected_rows:
            Synchronizer(user)()
        ar.success()


dd.inject_action('users.User', synchronize_google=SynchronizeGoogle())


class FailedForeignItemsByJob(dd.Table):
    allow_create = False
    column_names = "job value item_class"
    label = _("Failed foreign items")
    master_key = 'job'
    model = "google.FailedForeignItem"
    required_roles = dd.login_required()


class SyncSummaries(dd.Table):
    allow_create = False
    column_names = "created halted stats"
    detail_layout = """
    created halted
    stats
    FailedForeignItemsByJob
    """
    label = _("Sync summaries")
    model = "google.SyncSummary"
    # required_roles = dd.login_required((SiteAdmin, SiteStaff))
    required_roles = dd.login_required(ContactsStaff)

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super().param_defaults(ar, **kw)
        kw.update(user=ar.get_user())
        return kw


class MySyncSummaries(SyncSummaries):
    required_roles = dd.login_required()

    @classmethod
    def get_request_queryset(self, ar, **filter):
        return super().get_request_queryset(
            ar, **filter).filter(user=ar.get_user())


class Contacts(dd.Table):
    label = _("Google contacts")
    model = 'google.Contact'
    # required_roles = dd.login_required((SiteAdmin, SiteStaff))
    required_roles = dd.login_required(ContactsStaff)


class SyncableContacts(Contacts):
    allow_create = False
    label = _("Syncable contacts")

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return rt.models.google.Contact.get_outward_insert_update_queryset()


class MyContacts(Contacts):
    required_roles = dd.login_required(ContactsUser)
    insert_layout = """contact"""

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return super().get_request_queryset(
            ar, **filter).filter(user=ar.get_user())


class MySyncableContacts(SyncableContacts):
    required_roles = dd.login_required()

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return rt.models.google.Contact.get_outward_insert_update_queryset(
            ar.get_user())


class DeletedContacts(dd.Table):
    allow_create = False
    label = _("Deleted contacts")
    model = "google.DeletedContact"
    # required_roles = dd.login_required((SiteAdmin, SiteStaff))
    required_roles = dd.login_required(ContactsStaff)


class MyDeletedContacts(DeletedContacts):
    required_roles = dd.login_required()

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        return super().get_request_queryset(
            ar, **filter).filter(user=ar.get_user())


if dd.is_installed("cal"):

    class DeletedEntries(dd.Table):
        allow_create = False
        label = _("Deleted calendar entries")
        model = "google.DeletedEntry"
        # required_roles = dd.login_required((SiteAdmin, SiteStaff))
        required_roles = dd.login_required(ContactsStaff)

    class MyDeletedEntries(DeletedEntries):
        required_roles = dd.login_required()

        @classmethod
        def get_request_queryset(cls, ar, **filter):
            return super().get_request_queryset(
                ar, **filter).filter(user=ar.get_user())

    class SyncableEvents(dd.Table):
        allow_create = False
        label = _("Syncable calendar entries")
        model = "cal.Event"
        required_roles = dd.login_required()

        @classmethod
        def get_request_queryset(cls, ar, **filter):
            qs = None
            Event = rt.models.cal.Event
            for user, *_ in rt.models.google.CalendarSubscription.objects.values_list(
                    "user").distinct():
                if qs is None:
                    qs = Event.get_outward_insert_update_queryset(user)
                else:
                    qs = qs.union(Event.get_outward_insert_update_queryset(user))
            if qs is None:
                return Event.objects.none()
            return qs

    class MySyncableEvents(SyncableEvents):

        @classmethod
        def get_request_queryset(cls, ar, **filter):
            return rt.models.cal.Event.get_outward_insert_update_queryset(
                ar.get_user())


DELETED_EVENTS_META = {}
DELETED_CALENDARS_META = {}


@dd.receiver(dd.post_analyze)
def set_delete_signal_receivers(*args, **kwargs):

    if dd.is_installed("cal"):
        @dd.receiver(dd.pre_delete, sender=rt.models.cal.Event)
        def event_will_get_deleted(sender, instance, **kw):
            if instance.google_id:
                sub = rt.models.google.CalendarSubscription.objects.filter(
                    models.Q(access_role='writer') | models.Q(access_role='owner'),
                    calendar=instance._get_calendar()).first()
                if sub is not None and (user := sub.user) is not None:
                    DELETED_EVENTS_META[instance.google_id] = user

        @dd.receiver(dd.post_delete, sender=rt.models.cal.Event)
        def event_deleted(sender, instance, **kw):
            if user := DELETED_EVENTS_META.get(instance.google_id):
                entry = rt.models.google.DeletedEntry(
                    event_id=instance.google_id,
                    user=user,
                    calendar=False,
                    calendar_id=instance._get_calendar().google_id)
                entry.full_clean()
                entry.save()
                del DELETED_EVENTS_META[instance.google_id]

        @dd.receiver(dd.pre_delete, sender=rt.models.cal.Calendar)
        def calendar_will_get_deleted(sender, instance, **kw):
            if instance.google_id:
                sub = rt.models.google.CalendarSubscription.objects.filter(
                    models.Q(access_role='writer') | models.Q(access_role='owner'),
                    calendar=instance).first()
                if sub is not None and (user := sub.user):
                    DELETED_CALENDARS_META[instance.google_id] = user

        @dd.receiver(dd.post_delete, sender=rt.models.cal.Calendar)
        def calendar_deleted(sender, instance, **kw):
            if user := DELETED_CALENDARS_META.get(instance.google_id):
                entry = rt.models.google.DeletedEntry(
                    calendar_id=instance.google_id, calendar=True, user=user)
                entry.full_clean()
                entry.save()
                del DELETED_CALENDARS_META[instance.google_id]

    @dd.receiver(dd.post_save,
                 sender=dd.resolve_model(dd.plugins.google.contacts_model))
    def contact_modified(sender, instance, **kw):
        for obj in rt.models.google.Contact.objects.filter(contact=instance):
            obj.full_clean()
            obj.save()

    @dd.receiver(dd.post_delete, sender=rt.models.google.Contact)
    def contact_deleted(sender, instance, **kw):
        inst = rt.models.google.DeletedContact(user=instance.user,
                                               contact_id=instance.google_id)
        inst.save_new_instance(ar=inst.get_default_table().create_request(
            user=instance.user))
