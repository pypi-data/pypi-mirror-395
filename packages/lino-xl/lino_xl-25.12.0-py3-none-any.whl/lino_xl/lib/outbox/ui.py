# -*- coding: UTF-8 -*-
# Copyright 2011-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives

from lino.api import dd, _
from lino.core import constants
from lino.utils.html import html2text
from lino.modlib.office.roles import OfficeUser, OfficeStaff

from .choicelists import RecipientTypes


class Recipients(dd.Table):
    required_roles = dd.login_required(OfficeStaff)
    model = 'outbox.Recipient'
    # ~ column_names = 'mail  type *'
    # ~ order_by = ["address"]


class RecipientsByMail(Recipients):
    required_roles = dd.login_required(OfficeUser)
    master_key = 'mail'
    column_names = 'partner:20 address:20 name:20 type:10 *'
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}
    # summary_sep = ", "
    insert_layout = """
    partner
    name address
    """
    # ~ column_names = 'type owner_type owner_id'
    # ~ column_names = 'type owner'


class SendMail(dd.Action):
    """
    Send an `outbox.Mail` as an email.
    """

    icon_name = 'email_go'
    url_action_name = 'send'
    label = _('Send email')
    callable_from = "td"

    def get_action_permission(self, ar, obj, state):
        if obj is not None and obj.sent is not None:
            if not ar.get_user().user_type.has_required_roles([dd.SiteAdmin]):
                return False
        return super().get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        elem = ar.selected_rows[0]

        def undo(ar):
            elem.sent = None
            elem.full_clean()
            elem.save()
            ar.success(_("{} has been unsent.").format(elem), refresh=True)

        def send(ar):
            # ~ subject = elem.subject
            # ~ sender = "%s <%s>" % (rr.get_user().get_full_name(),rr.get_user().email)
            sender = "%s <%s>" % (elem.user.get_full_name(), elem.user.email)
            # ~ recipients = list(elem.get_recipients_to())
            to = []
            cc = []
            bcc = []
            found = False
            missing_addresses = []
            for r in elem.recipient_set.all():
                recipients = None
                if r.type == RecipientTypes.to:
                    recipients = to
                elif r.type == RecipientTypes.cc:
                    recipients = cc
                elif r.type == RecipientTypes.bcc:
                    recipients = bcc
                if recipients is not None:
                    if not r.address:
                        missing_addresses.append(r)
                    if r.address.endswith('@example.com'):
                        ar.logger.info("Ignored recipient %s",
                                       r.name_address())
                    else:
                        recipients.append(r.name_address())
                    found = True
                # ~ else:
                # ~ logger.info("Ignoring recipient %s (type %s)",r,r.type)
            if not found:
                return ar.error(_("No recipients found."))
            if len(missing_addresses):
                msg = _("There are recipients without address: ")
                msg += ', '.join([str(r) for r in missing_addresses])
                return ar.error(msg, alert=True)
            # ~ as_attachment = elem.owner.attach_to_email(rr)
            # ~ body = elem.body
            # ~ if as_attachment:
            # ~ body = elem.body
            # ~ else:
            # ~ body = elem.owner.get_mailable_body(rr)
            text_content = html2text(elem.body)
            msg = EmailMultiAlternatives(subject=elem.subject,
                                         from_email=sender,
                                         body=text_content,
                                         to=to,
                                         bcc=bcc,
                                         cc=cc)
            msg.attach_alternative(elem.body, "text/html")
            for att in elem.attachment_set.all():
                fn = att.owner.get_target_file()
                if fn is None:
                    raise Warning(
                        _("Couldn't find target file of %s") % att.owner)
                msg.attach_file(fn)

            uploads = dd.resolve_app("uploads")
            for up in uploads.UploadsByController.create_request(elem):
                # ~ for up in uploads.Upload.objects.filter(owner=elem):
                fn = os.path.join(settings.MEDIA_ROOT, up.file.name)
                msg.attach_file(fn)

            num_sent = msg.send()

            elem.sent = dd.now()
            kw.update(refresh=True)
            # ~ msg = "Email %s from %s has been sent to %s." % (
            # ~ elem.id,elem.sender,', '.join([
            # ~ r.address for r in elem.recipient_set.all()]))
            msg = _(
                "Email %(id)s from %(sender)s has been sent to %(num)d recipients."
            ) % dict(id=elem.id, sender=sender, num=num_sent)
            kw.update(message=msg, alert=True)
            # ~ for n in """EMAIL_HOST SERVER_EMAIL EMAIL_USE_TLS EMAIL_BACKEND""".split():
            # ~ msg += "\n" + n + " = " + unicode(getattr(settings,n))
            ar.logger.info(msg)
            if elem.owner:
                elem.owner.after_send_mail(elem, ar, kw)
            elem.save()
            ar.success(**kw)

        if elem.sent:
            ar.confirm(
                undo,
                _("This message has already been sent on {}. "
                  "Are you sure you want to unsend it?").format(elem.sent))
            # ~ return rr.ui.error(message='Mail has already been sent.')
        else:
            send(ar)


# ~ class MailDetail(dd.FormLayout):
# ~ main = """
# ~ """


class Mails(dd.Table):
    # ~ read_access = dd.login_required(user_level='manager')
    required_roles = dd.login_required(OfficeStaff)
    model = 'outbox.Mail'
    column_names = "sent recipients subject * body"
    hidden_columns = 'body'
    order_by = ["sent"]
    detail_layout = dd.DetailLayout("""
    subject project date
    user sent #build_time id owner
    RecipientsByMail:50x5 AttachmentsByMail:20x5 uploads.UploadsByController:20x5
    body:90x10
    """)
    insert_layout = dd.InsertLayout("""
    project
    subject
    body
    """,
                                    window_size=(60, 20))


if not settings.SITE.project_model:
    Mails.detail_layout.remove_element('project')


class MyOutbox(Mails):
    required_roles = dd.login_required(OfficeUser)

    label = _("My Outbox")
    master_key = 'user'

    @classmethod
    def setup_request(self, ar):  # 20230321
        if ar.master_instance is None:
            ar.master_instance = ar.get_user()
        # ~ print "20120519 MyOutbox.setup_request()", ar.master_instance
        super().setup_request(ar)


class MailsByController(Mails):
    required_roles = dd.login_required()
    master_key = 'owner'
    auto_fit_column_widths = True
    # ~ label = _("Postings")
    # display_mode = ((None, constants.DISPLAY_MODE_SUMMARY),)


class MailsByUser(Mails):
    required_roles = dd.login_required()
    label = _("Outbox")
    column_names = 'sent subject recipients'
    # ~ order_by = ['sent']
    order_by = ['-date']
    master_key = 'user'


if settings.SITE.project_model is not None:

    class MailsByProject(Mails):
        required_roles = dd.login_required()
        label = _("Outbox")
        column_names = 'date subject recipients user *'
        # ~ order_by = ['sent']
        order_by = ['-date']
        master_key = 'project'


class SentByPartner(Mails):
    """Shows the Mails that have been sent to a given Partner.
    """
    required_roles = dd.login_required()
    master = 'contacts.Partner'
    label = _("Outbox")
    column_names = 'sent subject user'
    order_by = ['sent']

    @classmethod
    def get_request_queryset(self, ar, **kwargs):
        q1 = Recipient.objects.filter(
            partner=ar.master_instance).values('mail').query
        qs = Mail.objects.filter(id__in=q1)
        qs = qs.order_by('sent')
        return qs


class Attachments(dd.Table):
    required_roles = dd.login_required(OfficeStaff)
    model = 'outbox.Attachment'
    # ~ window_size = (400,500)
    # ~ detail_layout = """
    # ~ mail owner
    # ~ """


class AttachmentsByMail(Attachments):
    required_roles = dd.login_required(OfficeUser)
    master_key = 'mail'
    default_display_modes = {None: constants.DISPLAY_MODE_SUMMARY}


class AttachmentsByController(Attachments):
    master_key = 'owner'
