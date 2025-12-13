# -*- coding: UTF-8 -*-
# Copyright 2008-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""See :doc:`/plugins/google`.

"""

import json
from pathlib import Path

from django.db.models import ObjectDoesNotExist
from lino.api import ad, _
from lino.core.roles import SiteAdmin, SiteStaff


class Plugin(ad.Plugin):

    verbose_name = _("Google API")
    menu_group = 'contacts'
    # partner_model = 'google.Person'
    # extends_models = ['Person']

    needs_plugins = [
        'lino.modlib.users', 'lino_xl.lib.addresses', 'lino_xl.lib.phones'
    ]

    contacts_model = "contacts.Person"
    num_retries = 3

    sync_immediately = False
    """
    Syncs a database entry to Google on `save`.

    Not used yet.
    """

    # settings

    backend = 'lino_xl.lib.google.backend.LinoGoogleOAuth2'

    # default is set on on_init method.
    client_secret_file = None

    scopes = [
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/contacts',
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.events'
    ]
    application_name = "LinoOAuthClient"

    entry_state_translation = (
        ('confirmed', ('confirmed', )),
        ('tentative', ('tentative', )),
        ('cancelled', ('cancelled', )),
    )

    guest_state_translation = (
        ('needsAction', ('needsAction', )),
        ('declined', ('declined', )),
        ('tentative', ('tentative', )),
        ('accepted', ('accepted', )),
    )

    sync_logging_frequency = 20

    def install_django_settings(self, site):
        super().install_django_settings(site)
        if not site.get_plugin_setting('users', 'third_party_authentication'):
            return
        # self.needs_plugins.append('social_django')
        if self.client_secret_file is None:
            self.client_secret_file = site.site_dir / "google_creds.json"
        elif isinstance(self.client_secret_file, str):
            self.client_secret_file = Path(self.client_secret_file)
        if not self.client_secret_file.exists():
            raise Exception(
                "Please make sure to provide OAuth client credentials\n"
                "accessable from Google. Look at the following link for help:\n"
                "https://support.google.com/cloud/answer/6158849?hl=en")
        with self.client_secret_file.open() as f:
            client_secret = json.load(f)
        site.update_settings(
            SOCIAL_AUTH_GOOGLE_KEY=client_secret['web']['client_id'],
            SOCIAL_AUTH_GOOGLE_SECRET=client_secret['web']['client_secret'],
            SOCIAL_AUTH_GOOGLE_SCOPE=self.scopes,
            SOCIAL_AUTH_GOOGLE_USE_UNIQUE_USER_ID=True,
            SOCIAL_AUTH_GOOGLE_AUTH_EXTRA_ARGUMENTS={
                'access_type': 'offline',
                'include_granted_scopes': 'true',
                'approval_prompt': 'auto'
            },
            SOCIAL_AUTH_GOOGLE_PIPELINE=(
                'social_core.pipeline.social_auth.social_details',
                'social_core.pipeline.social_auth.social_uid',
                'social_core.pipeline.social_auth.auth_allowed',
                'social_core.pipeline.social_auth.social_user',
                'lino_xl.lib.google.pipeline.redirect_ifn_refresh_token',
                'social_core.pipeline.user.get_username',
                # 'social_core.pipeline.mail.mail_validation',
                # 'social_core.pipeline.social_auth.associate_by_email',
                'social_core.pipeline.user.create_user',
                'social_core.pipeline.social_auth.associate_user',
                'lino_xl.lib.google.pipeline.intercept_extra_data',
                'social_core.pipeline.social_auth.load_extra_data',
                'social_core.pipeline.user.user_details',
            ))
        if not site.social_auth_backends:
            site.social_auth_backends = []
        site.social_auth_backends.append(self.backend)

    def pre_site_startup(self, site):
        from lino.core.utils import resolve_model
        self.contacts_model = resolve_model(self.contacts_model)
        return super().pre_site_startup(site)

    def get_migration_steps(self, other_sources):
        from lino_xl import __version__ as xlcv
        from pkg_resources import parse_version
        if 'lino_xl' in other_sources and other_sources[
                'lino_xl'] == '23.9.1' and parse_version(xlcv) > parse_version(
                    '23.9.1'):
            return ['lino_xl_23_9_1']
        return super().get_migration_steps(other_sources)

    def migrate_from_lino_xl_23_9_1(self, migrator, globals_dict):
        tokens = []
        users_User = globals_dict['users_User']
        google_CalendarSubscription = globals_dict[
            'google_CalendarSubscription']
        google_CalendarSyncToken = globals_dict['resolve_model'](
            "google.CalendarSyncToken")
        google_EventSyncToken = globals_dict['resolve_model'](
            "google.EventSyncToken")

        def create_users_user(id, email, language, modified, created,
                              start_date, end_date, password, last_login,
                              username, user_type, initials, first_name,
                              last_name, remarks, partner_id, time_zone,
                              date_format, event_type_id,
                              calendar_sync_token, calendar_page_token):
            kw = dict()
            kw.update(id=id)
            kw.update(email=email)
            kw.update(language=language)
            kw.update(modified=modified)
            kw.update(created=created)
            kw.update(start_date=start_date)
            kw.update(end_date=end_date)
            kw.update(password=password)
            kw.update(last_login=last_login)
            kw.update(username=username)
            kw.update(user_type=user_type)
            kw.update(initials=initials)
            kw.update(first_name=first_name)
            kw.update(last_name=last_name)
            kw.update(remarks=remarks)
            kw.update(partner_id=partner_id)
            kw.update(time_zone=time_zone)
            kw.update(date_format=date_format)
            kw.update(event_type_id=event_type_id)
            tokens.append(
                (id, calendar_sync_token, calendar_page_token, modified))
            return users_User(**kw)

        globals_dict['create_users_user'] = create_users_user

        e_tokens = []

        def create_google_calendarsubscription(id, modified, user_id,
                                               calendar_id, is_hidden, primary,
                                               access_role, sync_token,
                                               page_token):
            kw = dict()
            kw.update(id=id)
            kw.update(user_id=user_id)
            kw.update(calendar_id=calendar_id)
            kw.update(is_hidden=is_hidden)
            kw.update(primary=primary)
            kw.update(access_role=access_role)
            e_tokens.append((user_id, id, sync_token, page_token, modified))
            return google_CalendarSubscription(**kw)

        globals_dict[
            'create_google_calendarsubscription'] = create_google_calendarsubscription

        def after_load(loader):
            for token in tokens:
                loader.save(
                    google_CalendarSyncToken(user_id=token[0],
                                             sync_token=token[1],
                                             page_token=token[2],
                                             modified=token[3]))
            for token in e_tokens:
                loader.save(
                    google_EventSyncToken(user_id=token[0],
                                          subscription_id=token[1],
                                          sync_token=token[2],
                                          page_token=token[3],
                                          modified=token[4]))

        migrator.after_load(after_load)

    @staticmethod
    def has_scope(scope_type, user):
        assert scope_type in ['calendar', 'contact']
        try:
            suser = user.social_auth.get(provider='google')
        except ObjectDoesNotExist:
            return False

        scopes_list = suser.extra_data["scopes"].split()

        if scope_type == "calendar":
            return ('https://www.googleapis.com/auth/calendar.events'
                    in scopes_list and
                    'https://www.googleapis.com/auth/calendar' in scopes_list)
        if scope_type == "contact":
            return 'https://www.googleapis.com/auth/contacts' in scopes_list

    def setup_main_menu(self, site, user_type, m, ar=None):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('google.MyContacts')

    def setup_explorer_menu(self, site, user_type, m, ar=None):
        # mg = self.get_menu_group()
        mg = self
        m = m.add_menu(mg.app_label, mg.verbose_name)
        if user_type.has_required_roles([SiteStaff, SiteAdmin]):
            m.add_action('google.SyncableContacts')
            m.add_action('google.SyncableEvents')
            m.add_action('google.DeletedContacts')
            m.add_action('google.DeletedEntries')
            m.add_action('google.SyncSummaries')
        else:
            m.add_action('google.MySyncableContacts')
            m.add_action('google.MySyncableEvents')
            m.add_action('google.MyDeletedContacts')
            m.add_action('google.MyDeletedEntries')
            m.add_action('google.MySyncSummaries')

    def get_requirements(self, site):
        yield "social-auth-app-django"
        yield "google-api-python-client"
        yield "google-auth"
        yield "google-auth-httplib2"
        yield "google-auth-oauthlib"
