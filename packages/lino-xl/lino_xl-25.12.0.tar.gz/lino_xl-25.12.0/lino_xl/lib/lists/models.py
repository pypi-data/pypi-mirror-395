# -*- coding: UTF-8 -*-
# Copyright 2014-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from django.utils.html import format_html

from lino_xl.lib.contacts.roles import ContactsStaff, ContactsUser
from lino_xl.lib.appypod.mixins import PrintLabelsAction
from lino.modlib.printing.mixins import Printable
from lino.utils.mldbc.mixins import BabelDesignated
# from lino.core.utils import comma
from lino.utils.html import E, join_elems

from lino.api import dd, rt
from lino import mixins
from lino.core import constants

if dd.is_installed('lists'):
    partner_model = dd.plugins.lists.partner_model
else:
    partner_model = None

from lino.modlib.printing.mixins import DirectPrintAction
from lino.mixins.periods import Monthly


allow_subscription = dd.is_installed("contacts") and dd.is_installed("system")


class SubscribeToList(dd.Action):
    """Action to create membership on List"""
    label = _("Subscribe to list")
    parameters = dict(
        first_name=dd.CharField(_("First name"), max_length=300),
        last_name=dd.CharField(_("Last name"), max_length=300),
        email=models.EmailField(_("Email address")),
        list=dd.ForeignKey("lists.List"),
    )

    params_layout = """
    first_name last_name
    email list
    """

    required_roles = set([])  # type: ignore

    def action_param_defaults(self, ar, obj, **kw):
        kw = super().action_param_defaults(ar, obj, **kw)
        user = ar.get_user()
        if not user.is_anonymous:
            partner = user.partner.get_mti_child("person") if user.partner else None
            kw.update(
                first_name=partner.first_name if partner else user.first_name,
                last_name=partner.last_name if partner else user.last_name,
                email=partner.email if partner else user.email
            )
        kw.update(list=rt.models.system.SiteConfig.get_site_config().newsletter_list)
        return kw

    # pylint: disable=R0914
    def run_from_ui(self, ar, **kwargs):  # type: ignore[override]
        apv = ar.action_param_values
        if not (email := apv["email"]):
            raise Exception("Email field is required!")  # pylint: disable=W0719
        if not (list_ := apv["list"]):
            raise Exception("List field is required!")  # pylint: disable=W0719

        user = ar.get_user()

        PartnerModel = dd.plugins.lists.partner_model  # pylint: disable=C0103
        User = rt.models.users.User  # pylint: disable=C0103

        partner = None

        if not (partners := PartnerModel.objects.filter(email=email)).exists():
            attrs = {
                "first_name": apv["first_name"],
                "last_name": apv["last_name"],
                "email": email,
            }
            username = email.split("@")[0]
            while True:
                if not User.objects.filter(username=username).exists():
                    break
                username = str(uuid4())
            person = rt.models.contacts.Person(**attrs)
            # partner.name must not be blank,
            # populate at least one of the name when both are not found
            if not person.first_name and not person.last_name:
                person.first_name = username.capitalize()
            person.full_clean()
            person.save_new_instance(ar)
            partner = person.partner_ptr
            if user.is_anonymous:
                new_user = User(**attrs)
                new_user.username = username
                new_user.partner = partner
                new_user.full_clean()
                new_user.save_new_instance(
                    User.get_default_table().create_request(parent=ar, user=new_user))
                user = new_user

        Member = rt.models.lists.Member  # pylint: disable=W0621,C0103

        if Member.objects.filter(list=list_, partner__email=email).exists():
            ar.set_response(message=_("Membership already exists."))
        else:
            if partner is None:
                partner = partners.first()
            membership = Member(list=list_, partner=partner)
            membership.full_clean()
            membership.save_new_instance(
                membership.get_default_table().create_request(parent=ar, user=user))

        ar.success()


class PrintMembers(DirectPrintAction):
    # combo_group = "creacert"
    label = _("Members")
    tplname = "list_members"
    build_method = "weasy2pdf"
    icon_name = None
    show_in_toolbar = False
    # parameters = Monthly(
    #     show_remarks=models.BooleanField(
    #         _("Show remarks"), default=False),
    #     show_states=models.BooleanField(
    #         _("Show states"), default=True))
    # params_layout = """
    # start_date
    # end_date
    # show_remarks
    # show_states
    # """
    # keep_user_values = True


#class ListType(mixins.BabelNamed):
class ListType(BabelDesignated):
    """Represents a possible choice for the `list_type` field of a
    :class:`List`.

    """

    class Meta:
        app_label = 'lists'
        abstract = dd.is_abstract_model(__name__, 'ListType')
        verbose_name = _("List Type")
        verbose_name_plural = _("List Types")


class ListTypes(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'lists.ListType'
    column_names = 'designation *'


#class List(mixins.BabelNamed, mixins.Referrable):
class List(BabelDesignated, mixins.Referrable, Printable):

    class Meta:
        app_label = 'lists'
        abstract = dd.is_abstract_model(__name__, 'List')
        verbose_name = _("Partner List")
        verbose_name_plural = _("Partner Lists")

    list_type = dd.ForeignKey('lists.ListType', blank=True, null=True)
    remarks = models.TextField(_("Remarks"), blank=True)
    default_for_new_users = dd.BooleanField(_("Default for new users"), default=False)

    print_labels = PrintLabelsAction()
    print_members = PrintMembers()
    print_members_html = PrintMembers(build_method='weasy2html',
                                      label=format_lazy(
                                          u"{}{}", _("Members"), _(" (HTML)")))
    
    if allow_subscription:
        subscribe = SubscribeToList()

    @dd.displayfield(_("Print"))
    def print_actions(self, ar):
        if ar is None:
            return ''
        elems = []
        elems.append(ar.instance_action_button(self.print_labels))
        elems.append(ar.instance_action_button(self.print_members))
        elems.append(ar.instance_action_button(self.print_members_html))
        return E.p(*join_elems(elems, sep=", "))

    def get_overview_elems(self, ar):
        return [self.as_summary_item(ar)]


class Lists(dd.Table):
    required_roles = dd.login_required(ContactsUser)
    # required_roles = set([])
    model = 'lists.List'
    # column_names = 'ref designation list_type *'
    column_names = 'ref overview list_type *'
    order_by = ['ref']

    insert_layout = dd.InsertLayout("""
    ref list_type
    designation
    remarks
    """,
                                    window_size=(60, 12))

    detail_layout = dd.DetailLayout("""
    id ref list_type print_actions
    designation
    remarks
    MembersByList
    """)


if allow_subscription:
    class NewsletterList(Lists):
        """Makes the SiteConfig.newsletter_list publicly available."""
        required_roles = set([])
        default_record_id = "row"

        @classmethod
        def get_row_by_pk(cls, ar, pk):
            return rt.models.system.SiteConfig.get_site_config().newsletter_list


class Member(mixins.Sequenced):

    class Meta:
        app_label = 'lists'
        abstract = dd.is_abstract_model(__name__, 'Member')
        verbose_name = _("List membership")
        verbose_name_plural = _("List memberships")

    quick_search_fields = "partner__name remark"
    show_in_site_search = False
    allow_cascaded_delete = "list partner"

    list = dd.ForeignKey('lists.List', related_name="members")
    partner = dd.ForeignKey(partner_model, related_name="list_memberships")
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    def __str__(self):
        return _("{} is member of {}").format(self.partner, self.list)

    def as_summary_item(self, ar, text=None, **kwargs):
        if ar is None:
            obj = super()
        elif ar.is_obvious_field("list"):
            obj = self.partner
        elif ar.is_obvious_field("partner"):
            obj = self.list
        else:
            obj = super()
        return obj.as_summary_item(ar, text, **kwargs)


class Members(dd.Table):
    required_roles = dd.login_required(ContactsUser)
    model = 'lists.Member'
    detail_layout = dd.DetailLayout("""
    list
    partner
    remark
    """,
                                    window_size=(60, 'auto'))


class MembersByList(Members):
    label = _("Members")
    master_key = 'list'
    order_by = ['seqno']
    if dd.is_installed("phones"):
        column_names = "seqno partner remark workflow_buttons partner__address_column partner__contact_details *"
    else:
        column_names = "seqno partner remark workflow_buttons partner__address_column partner__email partner__gsm *"


class MembersByPartner(Members):
    master_key = 'partner'
    column_names = "list remark *"
    order_by = ['list__ref']
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    # summary_sep = ", "
    insert_layout = """
    list
    remark
    """


class AllMembers(Members):
    required_roles = dd.login_required(ContactsStaff)


if allow_subscription:
    dd.inject_field(
        "system.SiteConfig",
        "newsletter_list",
        dd.ForeignKey("lists.List", verbose_name=_("Newsletter list"), null=True, blank=True)
    )

    if False:
        
        @dd.receiver(dd.post_save, sender="users.User")
        def update_list_membership(sender, instance, **kwargs):
            """Update list membership for user when modified."""
            if not instance.partner:
                person = rt.models.contacts.Person(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    email=instance.email
                )
                # partner.name must not be blank, populate at least one of the name when both are not found
                if not person.first_name and not person.last_name:
                    person.first_name = instance.username.capitalize()
                person.full_clean()
                person.save_new_instance(
                    person.get_default_table().create_request(user=instance))
                instance.partner = person.partner_ptr
                instance.save()
                return
            Member = rt.models.lists.Member  # pylint: disable=W0621,C0103
            for l in rt.models.lists.List.objects.filter(default_for_new_users=True):
                if not Member.objects.filter(partner=instance.partner, list=l).exists():
                    membership = Member(list=l, partner=instance.partner)
                    membership.full_clean()
                    membership.save_new_instance(
                        membership.get_default_table().create_request(user=instance))
