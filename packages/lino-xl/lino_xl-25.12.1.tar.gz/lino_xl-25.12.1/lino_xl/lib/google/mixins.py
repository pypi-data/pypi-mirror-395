# -*- coding: UTF-8 -*-
# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime
import re
from dateutil.parser import parse
from urllib.parse import urlparse
from django.conf import settings
from django.db import models
from django.utils import timezone
from lino.api import dd, rt, _
from lino.mixins import Modified
from lino.modlib.users.mixins import UserAuthored
from lino.utils.format_date import IncompleteDate

from .choicelists import EntryStates, GuestStates, google_status
from .exceptions import AccessLocked

from lino import logger

if dd.is_installed('google'):
    try:
        from googleapiclient.errors import HttpError
    except ImportError:
        HttpError = None


class AccessLockable(Modified):

    class Meta:
        abstract = True

    locked = dd.BooleanField(default=False)

    # TODO: add another dd.DateTimeField `locked_at` for statistical purposes?
    # We can assume the released_at from the `modified` field.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This might be dangerous in case a locked instance is lost from a python session, and could be hard to get
        # this object back from the database.
        # Workarounds:
        # Use the `unlock_all` or `unlock_objects` to modify them at the database level.
        # Or get a list of pk(s) using `get_locked_objects_pk` and use `_force_get` instead.
        if self.pk is not None:
            if self.locked:
                raise AccessLocked(
                    f"Access to {self} as been locked by another transaction.")
            self.lock()

    def lock(self):
        auto_touch = self.auto_touch
        self.auto_touch = False
        self.save(lock=True)
        self.auto_touch = auto_touch

    def save(self, *args, **kwargs):
        self.locked = kwargs.pop("lock", False)  # otherwise, unlock
        super().save(*args, **kwargs)

    # Use the following methods for troubleshooting, never use them in any production code.
    @classmethod
    def unlock_all(cls):
        cls.objects.filter(locked=True).update(locked=False,
                                               modified=timezone.now())

    @classmethod
    def unlock_objects(cls, pk_list):
        cls.objects.filter(pk__in=pk_list).update(locked=False,
                                                  modified=timezone.now())

    @classmethod
    def get_locked_objects_pk(cls):
        return list(
            cls.objects.filter(locked=True).values_list('pk', flat=True))

    @classmethod
    def _force_get(cls, pk):
        foreign_keys = {}
        normal_fields = []
        for fld in cls._meta.concrete_fields:
            if fld.name in ['id', 'pk']:
                continue
            if isinstance(fld, models.ForeignKey):
                foreign_keys[fld.name] = fld
            else:
                normal_fields.append(fld.name)
        stuff = cls.objects.filter(pk=pk).values(*normal_fields,
                                                 *foreign_keys.keys())[0]
        self = cls(**{
            key: value
            for key, value in stuff.items() if key in normal_fields
        })
        for name, fld in foreign_keys.items():
            if isinstance(fld.related_model, AccessLockable):
                setattr(self, name, fld.related_model._force_get(stuff[name]))
            else:
                setattr(self, name,
                        fld.related_model.objects.get(id=stuff[name]))
        self.id = self.pk = pk
        return self


class SyncToken(UserAuthored, AccessLockable):

    class Meta:
        abstract = True

    sync_token = dd.CharField(max_length=300, blank=True, null=True)
    page_token = dd.CharField(max_length=300, blank=True, null=True)


class GoogleSynchronized(dd.Model):

    class Meta:
        abstract = True

    if dd.is_installed('google'):
        google_id = dd.CharField(max_length=200,
                                 verbose_name=_('Google resource ID/name'),
                                 blank=True)

        def synchronize_with_google(self, user=None) -> bool:
            return True


class GoogleCalendarSynchronized(GoogleSynchronized):

    class Meta:
        abstract = True

    if dd.is_installed('google'):

        modified = models.DateTimeField(_("Modified"),
                                        editable=False,
                                        null=True)

        def insert_or_update_into_google(self, resource, synchronizer):
            body = {
                'summary': self.name,
                'description': self.description,
                'timeZone': synchronizer.user.time_zone.text
            }

            if self.google_id:
                c = synchronizer.make_api_call(
                    lambda: resource.get(calendarId=self.google_id))
                if c.get('timeZone') is not None:
                    body.pop('timeZone')
                synchronizer.make_api_call(lambda: resource.update(
                    calendarId=self.google_id, body=body))
                synchronizer.stats.calendars__out_update += 1
            else:
                c = synchronizer.make_api_call(
                    lambda: resource.insert(body=body))
                self.google_id = c.get('id')
                synchronizer.stats.calendars__out_insert += 1

            self.full_clean()
            self.save()

        @classmethod
        def get_outward_insert_update_queryset(cls, user):
            return cls.objects.annotate(
                subscribed=models.Case(models.When(models.Exists(
                    rt.models.google.CalendarSubscription.objects.filter(
                        calendar__pk=models.OuterRef("pk"), user=user), ),
                                                   then=models.Value(True)),
                                       output_field=models.BooleanField(),
                                       default=models.Value(False))).filter(
                                           models.Q(google_id='') | models.Q(
                                               modified__gte=user.modified),
                                           subscribed=True)

        @classmethod
        def delete_google_calendar(cls, cal, synchronizer):
            try:
                gid = cal["id"]
                calendar = cls.objects.get(google_id=gid)
                calendar.delete()
                rt.models.google.DeletedEntry.objects.filter(
                    calendar=True, calendar_id=gid).delete()
                synchronizer.stats.calendars_deleted__in += 1
            except cls.DoesNotExist:
                pass

        @classmethod
        def sync_deleted_records(cls, resource, synchronizer):
            synchronizer.current_item_class = cls
            for obj in rt.models.google.DeletedEntry.objects.select_related(
                    'user').filter(calendar=True, user=synchronizer.user):
                try:
                    synchronizer.current_item = obj
                    synchronizer.make_api_call(
                        lambda: resource.delete(calendarId=obj.calendar_id))
                except HttpError:
                    continue
                obj.delete()
                synchronizer.stats.calendars_deleted__out += 1
                if (cs := synchronizer.stats.calendars
                        ) % synchronizer.logging_frequency == 0:
                    logger.info(
                        "google.Synchronizer (%s): synchronized %s calendars so far.",
                        synchronizer.user, cs)

        @classmethod
        def insert_or_update_google_calendar(cls, cal: dict, synchronizer):
            user = synchronizer.user
            try:
                calendar = cls.objects.get(google_id=cal["id"])
                if name := cal.get('summary'):
                    calendar.name = name
                if description := cal.get('description'):
                    calendar.description = description
            except cls.DoesNotExist:
                calendar = cls(google_id=cal["id"],
                               name=cal.get("summary", ""),
                               description=cal.get("description", ""))

            if color := cal.get('colorId'):
                calendar.color = color
            calendar.full_clean()
            if calendar.pk is None:
                ar = cls.get_default_table().create_request(user=user)
                calendar.save_new_instance(ar)
                synchronizer.stats.calendars__in_insert += 1
            else:
                calendar.save()
                synchronizer.stats.calendars__in_update += 1

            Room = rt.models.cal.Room
            room_desc = cal.get("location") or cal.get("description", "")
            room = calendar.room_calendars.filter(
                name=calendar.name).order_by('pk').first()
            if room is None:
                room = Room(name=cal.get("summary", ""),
                            description=room_desc,
                            calendar=calendar)
                room.full_clean()
                ar = Room.get_default_table().create_request(user=user)
                room.save_new_instance(ar)
            else:
                room.description = room_desc
                room.full_clean()
                room.save()

            return calendar, room


class GoogleCalendarEventSynchronized(GoogleSynchronized):

    class Meta:
        abstract = True

    if dd.is_installed('google'):

        @classmethod
        def delete_google_event(cls, event: dict, synchronizer):
            try:
                eid = event["id"]
                e = cls.objects.get(google_id=eid)
                e.delete()
                rt.models.google.DeletedEntry.objects.filter(
                    calendar=False,
                    event_id=eid,
                    calendar_id=e._get_calendar().google_id).delete()
                synchronizer.stats.events_deleted__in += 1
            except cls.DoesNotExist:
                pass

        @classmethod
        def sync_deleted_records(cls, resource, synchronizer):
            synchronizer.current_item_class = cls
            for obj in rt.models.google.DeletedEntry.objects.select_related(
                    'user').filter(calendar=False, user=synchronizer.user):
                synchronizer.current_item = obj
                try:
                    synchronizer.make_api_call(lambda: resource.delete(
                        calendarId=obj.calendar_id, eventId=obj.event_id))
                except HttpError:
                    continue
                obj.delete()
                synchronizer.stats.events_deleted__out += 1
                if (evs := synchronizer.stats.events
                        ) % synchronizer.logging_frequency == 0:
                    logger.info(
                            "google.Synchronizer (%s): synchronized %s events so far.",
                            synchronizer.user, evs)

        @classmethod
        def get_outward_insert_update_queryset(cls, user):
            cal_cases = []
            for fieldname in dd.plugins.cal.calendar_fieldnames:
                parts = fieldname.split("__")
                query = None
                for i in range(len(parts)):
                    if query is None:
                        query = models.Q(**{f"{parts[i]}__isnull": False})
                    else:
                        part = "__".join(parts[:i + 1])
                        query = query & models.Q(**{f"{part}__isnull": False})
                cal_cases.append(models.When(query, then=models.F(fieldname)))

            qs = cls.objects
            site_calendar = settings.SITE.get_config_value('site_calendar')
            if not cal_cases:
                qs = qs.annotate(cal=models.Value(
                    site_calendar.pk if site_calendar else None,
                    output_field=dd.ForeignKey(rt.models.cal.Calendar)))
            else:
                qs = qs.annotate(cal=models.Case(
                    *cal_cases,
                    default=site_calendar.pk if site_calendar else models.
                    Value(None),
                    output_field=dd.ForeignKey(rt.models.cal.Calendar)))
            return qs.filter(
                cal__isnull=False).annotate(
                    sub=models.Case(models.When(
                        models.Exists(
                            rt.models.google.CalendarSubscription.
                            objects.filter(models.Q(access_role='writer')
                                           | models.Q(access_role='owner'),
                                           calendar__pk=models.OuterRef("cal"),
                                           user=user)),
                        then=rt.models.google.CalendarSubscription.objects.
                        filter(models.Q(access_role='writer')
                               | models.Q(access_role='owner'),
                               calendar__pk=models.OuterRef("cal"),
                               user=user).values('pk')[:1]),
                                    default=models.Value(None),
                                    output_field=dd.ForeignKey(
                                        rt.models.google.CalendarSubscription,
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True))
                ).filter(sub__isnull=False).annotate(
                    edit=models.Case(models.When(models.Q(
                        modified__gte=rt.models.google.CalendarSubscription.
                        objects.filter(pk=models.OuterRef("sub")).values(
                            "eventsynctoken__modified")[:1]),
                                                 then=models.Value(True)),
                                     default=models.Value(False),
                                     output_field=models.BooleanField())
                ).filter(models.Q(google_id="") | models.Q(edit=True))

        def insert_or_update_into_google(self, resource, synchronizer):
            body = {
                'summary': self.summary,
                'description': self.description,
            }
            if hasattr(self, "sequence"):
                body["sequence"] = self.sequence
            elif hasattr(self, "seqno"):
                body["sequence"] = self.seqno

            if self.start_time:
                body['start'] = {
                    'dateTime': self.get_datetime('start').isoformat()
                }
            elif self.start_date:
                body['start'] = {'date': self.start_date.isoformat()}
            # TODO: what's originalStart

            if self.end_time:
                body['end'] = {
                    'dateTime': self.get_datetime('end').isoformat()
                }
            elif self.end_date:
                body['end'] = {'date': self.end_date.isoformat()}

            attendees = []
            for guest in self.guest_set.all():
                if email := guest.partner.email:
                    attendee = {'email': email}
                    if status := google_status(guest.state):
                        attendee['responseStatus'] = status
                    attendees.append(attendee)
            if attendees:
                body['attendees'] = attendees
            cal = self._get_calendar()

            if self.google_id:
                synchronizer.make_api_call(
                    lambda: resource.update(calendarId=cal.google_id,
                                            eventId=self.google_id,
                                            body=body))
                synchronizer.stats.events__out_update += 1
            else:
                e = synchronizer.make_api_call(lambda: resource.insert(
                    calendarId=cal.google_id, body=body))
                synchronizer.stats.events__out_insert += 1
                self.google_id = e['id']

            self.full_clean()
            self.save()

        @classmethod
        def insert_or_update_google_event(cls, event: dict, room,
                                          synchronizer):
            user = synchronizer.user
            try:
                e = cls.objects.get(google_id=event['id'])
            except cls.DoesNotExist:
                e = cls(google_id=event['id'])
            if state := EntryStates.get_by_name(event.get('status', ''), None):
                if e.state is not None and google_status(e.state) != state:
                    e.state = state

            e.summary = event.get('summary', "")  # The title of the event
            e.description = event.get('description', "")
            if hasattr(e, "sequence"):
                e.sequence = event.get('sequence', 0)
            elif hasattr(e, "seqno"):
                e.seqno = event.get('sequence', 0)

            if e.room is None:
                e.room = room

            # if location := event.get('location'):
            #     if location != e.room.description:
            #         Room = room.__class__
            #         try:
            #             room = Room.objects.get(description=location, calendar=room.calendar)
            #         except Room.DoesNotExist:
            #             room = e.room
            #             room.pk = None
            #             room.description = location
            #             ar = Room.get_default_table().create_request(user=user)
            #             room.full_clean()
            #             room.save_new_instance(ar)
            #         e.room = room
            #         # TODO: clear up unused rooms

            def resolve_datetime(stamp, tz=None):
                dt = parse(stamp)
                if timezone.is_aware(dt):
                    return dt
                if tz is not None:
                    with timezone.override(tz):
                        return timezone.make_aware(dt)
                return timezone.make_aware(dt)

            def resolve_date_time(stamp, tz=None):
                dt = resolve_datetime(stamp, tz)
                return dt.date(), dt.time()

            if start := event.get('start'):
                if dateTime := start.get('dateTime'):
                    e.start_date, e.start_time = resolve_date_time(dateTime)
                else:
                    e.start_date = datetime.date(
                        *map(int, start['date'].split('-')))
            elif originalStart := event.get('originalStartTime'):
                if dateTime := originalStart.get('dateTime'):
                    e.start_date, e.start_time = resolve_date_time(dateTime)
                else:
                    e.start_date = datetime.date(
                        *map(int, originalStart['date'].split('-')))

            if end := event.get('end'):
                if dateTime := end.get('dateTime'):
                    e.end_date, e.end_time = resolve_date_time(dateTime)
                else:
                    e.end_date = datetime.date(
                        *map(int, end['date'].split('-')))

            author = None
            if creator := event.get('creator'):
                author = rt.models.users.User.objects.filter(
                    email=creator['email']).first()
            if author is not None:
                e.user = author
            if e.user is None:
                e.user = user
            e.full_clean()
            if e.pk is None:
                ar = cls.get_default_table().create_request(user=user)
                e.save_new_instance(ar)
                synchronizer.stats.events__in_insert += 1
            else:
                e.save()
                synchronizer.stats.events__in_update += 1

            if attendees := event.get('attendees'):
                # TODO: how about the removed attendees? There should be a definitive method to figure out
                #     which are Guest from google and which are lino native
                for attendee in attendees:
                    if attendee.get("organizer", False):
                        continue
                    if guest_email := attendee.get("email") is not None:
                        Partner = dd.resolve_model(
                            dd.plugins.cal.partner_model)
                        partners = Partner.objects.filter(email=guest_email)
                        partner = None
                        if partners.count() >= 1:
                            partner = partners.filter(
                                user__isnull=False).first()
                            if partner is None:
                                partner = partners[0]
                        if partner is not None:
                            Guest = rt.models.cal.Guest
                            try:
                                guest = Guest.objects.get(event=e,
                                                          partner=partner)
                            except Guest.DoesNotExist:
                                guest = Guest(event=e, partner=partner)
                            if state := GuestStates.get_by_name(
                                    attendee.get("responseStatus", ''), None):
                                if guest.state is not None and google_status(
                                        guest.state) != state:
                                    guest.state = state
                            guest.full_clean()
                            if guest.pk is None:
                                ar = Guest.get_default_table().create_request(
                                    user=user)
                                guest.save_new_instance(ar)
                            else:
                                guest.save()

            return e


class GoogleContactSynchronized(GoogleSynchronized):
    contacts_model = None
    """
    May be set as a class attribute when contacts_model was first resolved by the plugin.
    """

    type_map = {"mobile": "gsm", "homeFax": "fax", "workFax": "fax"}

    person_fields = "addresses" \
                    ",birthdays" \
                    ",emailAddresses" \
                    ",genders" \
                    ",locales" \
                    ",names" \
                    ",nicknames" \
                    ",phoneNumbers" \
                    ",urls"

    class Meta:
        abstract = True

    if dd.is_installed('google'):

        @classmethod
        def delete_google_contact(cls, contact, synchronizer):
            user = synchronizer.user
            try:
                item = cls.objects.get(google_id=contact["resourceName"],
                                       user=user)
                item.delete()
                rt.models.google.DeletedContact.objects.filter(
                    contact_id=contact["resourceName"], user=user).delete()
                synchronizer.stats.contacts_deleted__in += 1
            except cls.DoesNotExist:
                pass

        @classmethod
        def sync_deleted_records(cls, resource, synchronizer):
            synchronizer.current_item_class = cls
            for obj in rt.models.google.DeletedContact.objects.select_related(
                    'user').filter(user=synchronizer.user):
                synchronizer.current_item = obj
                try:
                    synchronizer.make_api_call(lambda: resource.deleteContact(
                        resourceName=obj.contact_id))
                except HttpError:
                    continue
                obj.delete()
                synchronizer.stats.contacts_deleted__out += 1
                if (cns := synchronizer.stats.contacts
                        ) % synchronizer.logging_frequency == 0:
                    logger.info(
                        "google.Synchronizer (%s): synchronized %s contacts so far.", synchronizer.user, cns)

        @classmethod
        def get_outward_insert_update_queryset(cls, user=None):
            if user is not None:
                return cls.objects.filter(
                    modified__gte=rt.models.google.ContactSyncToken.objects.
                    get(user=user).modified,
                    user=user)
            return cls.objects.annotate(syncable=models.Case(
                models.When(~models.Exists(
                    rt.models.google.ContactSyncToken.objects.filter(
                        user=models.OuterRef("user"))),
                            then=models.Value(True)),
                models.When(models.Exists(
                    rt.models.google.ContactSyncToken.objects.filter(
                        modified__lte=models.OuterRef("modified"),
                        user=models.OuterRef("user"))),
                            then=models.Value(True)),
                output_field=models.BooleanField(),
                default=models.Value(False))).filter(syncable=True)

        @classmethod
        def street_address(cls, address):
            return f"{address.addr1 or ''}, {address.street_prefix or ''} {address.street or ''}".strip(
                " ,")

        @classmethod
        def parse_street(cls, street_line, address):
            pattern = "^"
            if address.addr1:
                pattern += f"((?P<addr1>{address.addr1})(, ))?"
            if address.street_prefix:
                pattern += "(" + (p_street_prefix :=
                                  "(?P<street_prefix>{address.street_prefix})"
                                  ) + ("( ))?" if address.street else ")?")
            if address.street:
                pattern += (p_street := f"(?P<street>{address.street})") + "?"
            pattern += ".*$"

            m = re.match(pattern, street_line).groupdict()

            if m["addr1"] is None or m["street_prefix"] is None or m[
                    "street"] is None:
                parts = [p.strip() for p in street_line.split(",")]

                if len(parts) > 2:
                    return m["addr1"], m["street_prefix"], street_line

                p_index = 0
                match = None
                for i, part in parts:
                    p_index = i
                    if match := re.match(
                            r"^(?P<street_prefix>.*)?( )?" + p_street + "$",
                            part):
                        if m["street_prefix"] is None:
                            m["street_prefix"] = match.groupdict(
                            )["street_prefix"]
                        break
                    elif match := re.match(
                            "^" + p_street_prefix + "?( )?" +
                            "(P?<street>.*)?$", part):
                        if m["street"] is None:
                            m["street"] = match.groupdict()["street"]
                        break
                if match is not None:
                    if m["addr1"] is None and p_index == 1:
                        m["addr1"] = parts[0]

            return m["addr1"], m["street_prefix"], m["street"] or street_line

        def insert_or_update_into_google(self, resource, synchronizer):
            if self.google_id:
                person = synchronizer.make_api_call(lambda: resource.get(
                    resourceName=self.google_id,
                    personFields=rt.models.google.Contact.person_fields))
            else:
                person = {}
            contact = self.contact
            name = [
                n for n in person.get("names", [{
                    "metadata": {
                        "primary": True
                    }
                }]) if n.get("metadata", {}).get("primary")
            ][0]

            name["displayName"] = contact.name
            if contact.first_name:
                name["givenName"] = contact.first_name
            if contact.last_name:
                name["familyName"] = contact.last_name
            if contact.middle_name:
                name["middleName"] = contact.middle_name
            if contact.title:
                name["honorificPrefix"] = contact.title
            person["names"] = [name]

            if bdate := contact.birth_date:
                birthdays = person.get("birthdays", [{
                    "metadata": {
                        "primary": True
                    }
                }])
                birthday = [
                    b for b in birthdays
                    if b.get("metadata", {}).get("primary")
                ][0]
                if 'date' not in birthday:
                    birthday['date'] = {}
                birthday['date']["day"] = bdate.day
                birthday['date']["month"] = bdate.month
                birthday['date']["year"] = bdate.year
                birthday['text'] = f"{bdate.month}/{bdate.day}/{bdate.year}"
                person["birthdays"] = [birthday]

            addresses = person.get("addresses", [{
                "metadata": {
                    "primary": True,
                }
            }])

            def dump_address(cont, addr={"metadata": {"primary": False}}):
                if cont.country is not None:
                    addr["country"] = cont.country.name
                    addr[
                        "countryCode"] = cont.country.isocode or cont.country.iso3 or cont.country.short_code
                addr["postalCode"] = cont.zip_code
                if cont.city is not None:
                    addr["city"] = cont.city.name
                if cont.region is not None:
                    addr["region"] = cont.region.name
                if cont.addr2:
                    addr["extendedAddress"] = cont.addr2
                if cont.street_box:
                    addr["poBox"] = cont.street_box
                addr["streetAddress"] = self.street_address(cont)
                return addr

            address = [
                a for a in addresses if a.get("metadata", {}).get("primary")
            ][0]
            addresses.clear()

            if contact.country is not None or contact.city is not None or contact.region is not None or contact.addr1 or contact.street:
                addresses.append(dump_address(contact, address))

            for a in rt.models.addresses.Address.objects.filter(
                    partner=contact, primary=False):
                addresses.append(dump_address(a))

            person["addresses"] = addresses

            phones = person.get("phoneNumbers", [{
                "metadata": {
                    "primary": True
                }
            }])
            phone = [
                p for p in phones if p.get("metadata", {}).get("primary")
            ][0]
            phones_dup = phones.copy()
            phones.clear()
            if "type" in phone:
                phone["value"] = getattr(
                    contact, self.type_map.get(phone["type"], "phone"))
            else:
                if contact.phone:
                    phone["value"] = contact.phone
                    # phone["type"] = "main"
                elif contact.gsm:
                    phone["value"] = contact.gsm
                    phone["type"] = "mobile"
                elif contact.fax:
                    phone["value"] = contact.fax
                    # phone["type"] = "homeFax"
                else:
                    phone.clear()
            if phone:
                phones.append(phone)
            for phone in rt.models.phones.ContactDetail.objects.filter(
                    primary=False,
                    partner=contact,
                    detail_type__in=[
                        (phone_type := lambda t: rt.models.phones.
                         ContactDetailTypes.get_by_name(t).value)("phone"),
                        phone_type("gsm"),
                        phone_type("fax")
                    ]):
                phn = [
                    p for p in phones_dup
                    if p.get("canonicalForm", p["value"]) == phone.value
                ]
                if phn:
                    phn = phn[0]
                else:
                    phn = {"metadata": {"primary": False}}

                if "canonicalForm" in phn:
                    phn["canonicalForm"] = phone.value
                    if "value" in phn:
                        del phn["value"]
                else:
                    phn["value"] = phone.value

                if phone.detail_type == rt.models.phones.ContactDetailTypes.gsm:
                    phn["type"] = "mobile"

                phones.append(phn)

            person["phoneNumbers"] = phones

            emails = person.get("emailAddresses", [{
                "metadata": {
                    "primary": True
                }
            }])
            email = [
                e for e in emails if e.get("metadata", {}).get("primary")
            ][0]
            emails_dup = emails.copy()
            emails.clear()

            if contact.email:
                email["value"] = contact.email
                emails.append(email)

            for email in rt.models.phones.ContactDetail.objects.filter(
                    primary=False,
                    partner=contact,
                    detail_type=rt.models.phones.ContactDetailTypes.email):
                eml = [e for e in emails_dup if e["value"] == email.value]
                if eml:
                    eml = eml[0]
                else:
                    eml = {"metadata": {"primary": False}}

                eml["value"] = email.value

                emails.append(eml)

            person["emailAddresses"] = emails

            urls = person.get("urls", [{"metadata": {"primary": True}}])
            url = [u for u in urls if u.get("metadata", {}).get("primary")][0]
            urls_dup = urls.copy()
            urls.clear()

            if contact.url:
                url["value"] = contact.url
                urls.append(url)

            for url in rt.models.phones.ContactDetail.objects.filter(
                    primary=False,
                    partner=contact,
                    detail_type=rt.models.phones.ContactDetailTypes.url):
                u = [u for u in urls_dup if u["value"] == url.value]
                if u:
                    u = u[0]
                else:
                    u = {"metadata": {"primary": False}}

                u["value"] = url.value

                urls.append(u)

            person["urls"] = urls

            if self.google_id:
                synchronizer.make_api_call(lambda: resource.updateContact(
                    resourceName=self.google_id, body=person))
                synchronizer.stats.contacts__out_update += 1
            else:
                resp = synchronizer.make_api_call(
                    lambda: resource.createContact(body=person))
                synchronizer.stats.contacts__out_insert += 1
                self.google_id = resp["resourceName"]

            self.full_clean()
            self.save()

        @classmethod
        def insert_or_update_google_contact(cls, contact, synchronizer):
            user = synchronizer.user
            try:
                self = cls.objects.get(google_id=contact["resourceName"])
            except cls.DoesNotExist:
                self = cls(google_id=contact["resourceName"], user=user)

            if cls.contacts_model is None:
                cls.contacts_model = dd.resolve_model(
                    dd.plugins.google.contacts_model)

            try:
                person = self.contact
            except cls.contacts_model.DoesNotExist:
                person = cls.contacts_model()

            for name in contact.get("names", []):
                if name.get("metadata", {}).get("primary"):
                    person.name = name.get("displayName", "")
                    person.title = name.get("honorificPrefix", "")
                    person.first_name = name.get("givenName", "")
                    person.middle_name = name.get("middleName", "")
                    person.last_name = name.get("familyName", "")
                    break

            if not person.first_name and not person.last_name:
                person.first_name = "Unknown"

            phones = []
            for phone in contact.get("phoneNumbers", []):
                t = cls.type_map.get(phone.get("type", "dummy"), "phone")
                v = phone.get("canonicalForm", phone["value"])
                if phone.get("metadata", {}).get("primary"):
                    setattr(person, t, v)
                    continue

                phones.append({
                    "primary":
                    False,
                    "value":
                    v,
                    "detail_type":
                    rt.models.phones.ContactDetailTypes.get_by_name(t)
                })

            for url in contact.get("urls", []):
                if url.get("metadata", {}).get("primary"):
                    if not urlparse((v := url["value"])).scheme:
                        v = f"http://{v}"
                    person.url = v
                    continue

                if not urlparse((v := url["value"])).scheme:
                    v = f"http://{v}"

                phones.append({
                    "primary":
                    False,
                    "value":
                    v,
                    "detail_type":
                    rt.models.phones.ContactDetailTypes.url
                })

            for email in contact.get("emailAddresses", []):
                if email.get("metadata", {}).get("primary"):
                    person.email = email["value"]
                    continue

                phones.append({
                    "primary":
                    False,
                    "value":
                    email["value"],
                    "detail_type":
                    rt.models.phones.ContactDetailTypes.email
                })

            for bday in contact.get("birthdays", []):
                if bday.get("metadata", {}).get("primary"):
                    person.birth_date = IncompleteDate(
                        (bdate := bday["date"]).get("year", 0),
                        bdate.get("month", 0), bdate.get("day", 0)).strftime(
                            settings.SITE.date_format_strftime)
                    break

            addresses = []
            for address in contact.get("addresses", []):
                a_obj = {
                    "zip_code": address.get("postalCode", ""),
                    "street": address.get("streetAddress", ""),
                    "street_box": address.get("poBox", ""),
                    "addr2": address.get("extendedAddress", "")
                }

                if (cc := address.get("countryCode")) is not None:
                    # There should be a database entry for each country in "all_countries" fixture. Which we assume so.
                    # If the database is not filled with all countries,
                    # then put the below statement into try ... except block
                    country = rt.models.countries.Country.objects.filter(
                        models.Q(short_code=cc) | models.Q(isocode=cc)
                        | models.Q(iso3=cc)).first()

                    if country is None:
                        msg = f"{address['country']} ({address['countryCode']})"
                        msg += ": No such country in the database"
                        raise Exception(msg)

                    a_obj['country'] = country
                else:
                    country = user.get_country()

                if country is not None:
                    if city := address.get("city"):
                        city, __ = rt.models.countries.Place.objects.get_or_create(
                            name=city,
                            country=country,
                            type=rt.models.countries.PlaceTypes.city)
                        a_obj['city'] = city

                    if region := address.get("region"):
                        region, __ = rt.models.countries.Place.objects.get_or_create(
                            name=region,
                            country=country,
                            type=rt.models.countries.PlaceTypes.region)
                        a_obj['region'] = region

                if address.get("metadata", {}).get("primary"):
                    for key, value in a_obj.items():
                        setattr(person, key, value)
                    continue

                a_obj.update(primary=False)

                addresses.append(a_obj)

            person.full_clean()
            if person.pk is None:
                person.save_new_instance(
                    person.get_default_table().create_request(user=user))
            else:
                person.save()

            self.contact = person

            for i, phone in enumerate(phones):
                p, __ = rt.models.phones.ContactDetail.objects.get_or_create(
                    partner=person, **phone)
                phones[i] = p

            if phones:
                rt.models.phones.ContactDetail.objects.filter(
                    partner=person,
                    primary=False).exclude(pk__in=[p.pk
                                                   for p in phones]).delete()

            for i, address in enumerate(addresses):
                a, __ = rt.models.addresses.Address.objects.get_or_create(
                    partner=person, **address)
                addresses[i] = a

            if addresses:
                rt.models.addresses.Address.objects.filter(
                    partner=self.contact, primary=False).exclude(
                        pk__in=[a.pk for a in addresses]).delete()

            self.full_clean()
            if self.pk is None:
                self.save_new_instance(ar=self.get_default_table().create_request(
                    user=user))
                synchronizer.stats.contacts__in_insert += 1
            else:
                self.save()
                synchronizer.stats.contacts__in_update += 1

            return self
