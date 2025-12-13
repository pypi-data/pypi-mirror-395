# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, dd, _
from lino_xl.lib.accounting.roles import LedgerUser
from django.db import models


class SubscribeToLedger(dd.Action):
    label = _("Subscribe to ledger")
    select_rows = True
    required_roles = dd.login_required(LedgerUser)

    parameters = {
        "company": dd.ForeignKey("contacts.Company", blank=True),
        "ledger": dd.ForeignKey("ledgers.Ledger", blank=True),
        "role": dd.ForeignKey("contacts.RoleType"),
        "user": dd.ForeignKey("users.User", blank=True)
    }

    def action_param_defaults(self, ar, obj, **kw):
        kw = super().action_param_defaults(ar, obj, **kw)
        if obj is not None:
            if isinstance(obj, rt.models.ledgers.Ledger):
                kw['company'] = obj.company
                kw['ledger'] = obj
            elif isinstance(obj, rt.models.users.User):
                kw['user'] = obj
            else:
                raise Exception(
                    _("Invalid selected_row: must be a ledgers.Ledger or users.User instance"))
        return kw

    @staticmethod
    def is_parameters_valid(ar, apv):
        if len(ar.selected_rows) > 1:
            ar.error(_(
                "Invalid parameter %s: only one row is required"
            ) % ar.actor.model.__name__.lower(), alert=True)
            return False
        if apv['role'] is None:
            ar.error(_("Missing required parameter: role"), alert=True)
            return False
        if (user := apv['user']) is None:
            ar.error(_("Missing required parameter: user"), alert=True)
            return False
        ledger = apv['ledger']
        if (company := apv['company']) is None and ledger is None:
            ar.error(
                _("Missing complementary required parameter: company or ledger"), alert=True)
            return False

        if user.ledger is None:
            return True

        ledger = ledger or company.ledger
        if user.ledger == ledger:
            ar.error(_(
                "Invalid operation: User (%s) already assigned to the selected ledger"
            ) % str(user), alert=True)
            return False
        if (qs := rt.models.users.User.objects.filter(ledger=ledger).annotate(authorized=models.Case(
                    models.When(models.Exists(rt.models.users.Authority.objects.filter(
                        user=models.OuterRef('pk'), authorized=user)), then=models.Value(True)),
                default=models.Value(False),
                output_field=models.BooleanField()
                )).filter(authorized=True)).exists():
            ar.error(_(
                "Invalid operation: Authorized user (%s) already assigned to the selected ledger"
            ) % str(qs.first()), alert=True)
            return False

        return True

    @staticmethod
    def make_subscription(apv, ar):
        ledger = apv['ledger']
        if (company := apv['company']) is None:
            company = ledger.company
        elif ledger is None:
            ledger = company.ledger

        if (user := apv['user']).ledger is not None:
            user = rt.models.users.User(
                username=f"{company.as_ref_prefix()}{user.username}")
            for attr_name in ['initials', 'first_name', 'last_name', 'nickname', 'email', 'language', 'user_type',
                              'remarks', 'partner', 'time_zone', 'date_format', 'sales_journal']:
                setattr(user, attr_name, getattr(
                    apv['user'], attr_name) if hasattr(user, attr_name) else None)
            user.save_new_instance(user.get_default_table().create_request(parent=ar))
            authority = rt.models.users.Authority(authorized=apv['user'], user=user)
            authority.save_new_instance(
                authority.get_default_table().create_request(parent=ar))

        user.ledger = ledger
        user.save()

        if user.partner is not None:
            Role = rt.models.contacts.Role
            role_attr = dict(type=apv['role'], company=company, person=user.person)
            if not Role.objects.filter(**role_attr).exists():
                role = Role(**role_attr)
                role.save_new_instance(role.get_default_table().create_request(parent=ar))

    def run_from_ui(self, ar, **kwargs):
        apv = ar.action_param_values
        if not self.is_parameters_valid(ar, apv):
            return

        self.make_subscription(apv, ar)

        ar.goto_instance(apv['company'] or apv['ledger'].company)
        ar.success()
