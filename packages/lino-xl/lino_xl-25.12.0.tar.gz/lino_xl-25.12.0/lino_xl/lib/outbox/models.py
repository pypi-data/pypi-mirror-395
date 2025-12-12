# -*- coding: UTF-8 -*-
# Copyright 2011-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from lino.api import dd, _
from lino.mixins import ProjectRelated
from lino.modlib.uploads.mixins import UploadController
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.printing.mixins import Printable

from .choicelists import RecipientTypes
from .ui import *


class Recipient(dd.Model):

    allow_cascaded_delete = ['mail']

    class Meta:
        verbose_name = _("Recipient")
        verbose_name_plural = _("Recipients")

    mail = dd.ForeignKey('outbox.Mail')
    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)
    type = RecipientTypes.field(default='to')
    address = models.EmailField(_("Address"), blank=True)
    name = models.CharField(_("Name"), max_length=200)

    def name_address(self):
        return '%s <%s>' % (self.name, self.address)

    def __str__(self):
        #~ return "[%s]" % unicode(self.name or self.address)
        return str(self.name or self.address)
        #~ return "[%s]" % unicode(self.address)

    def full_clean(self):
        if self.partner:
            if not self.address:
                self.address = self.partner.email
            if not self.name:
                self.name = self.partner.get_full_name(salutation=False)
        super().full_clean()

    def get_row_permission(self, ar, state, ba):
        """
        Recipients of a Mail may not be edited if the Mail is read-only.
        """
        if self.mail_id and not self.mail.get_row_permission(ar, state, ba):
            #~ logger.info("20120920 Recipient.get_row_permission()")
            return False
        return super().get_row_permission(ar, state, ba)


class Mail(UserAuthored, Printable, UploadController, ProjectRelated,
           Controllable):

    class Meta:
        verbose_name = _("Outgoing message")
        verbose_name_plural = _("Outgoing messages")

    send_mail = SendMail()

    date = models.DateField(_("Date"), default=settings.SITE.today)

    subject = models.CharField(_("Subject"), max_length=200, blank=True)
    body = dd.RichTextField(_("Body"), blank=True, format='html')
    sent = models.DateTimeField(null=True, editable=False)

    # def on_create(self, ar):
    #     self.date = settings.SITE.today()
    #     super().on_create(ar)

    def get_print_language(self):
        if self.user is not None:
            return self.user.language
        return super().get_print_language()

    def __str__(self):
        return '%s #%s' % (self._meta.verbose_name, self.pk)

    def get_recipients(self, rr):
        #~ recs = []
        if self.pk is None:
            return ""
        recs = [
            str(r) for r in Recipient.objects.filter(mail=self,
                                                     type=RecipientTypes.to)
        ]
        return ', '.join(recs)

    recipients = dd.VirtualField(dd.HtmlBox(_("Recipients")), get_recipients)

    def get_row_permission(self, ar, state, ba):
        """
        Mails may not be edited after they have been sent.
        """
        if self.sent and not ba.action.readonly:
            #~ logger.info("20120920 Mail.get_row_permission()")
            return False
        return super().get_row_permission(ar, state, ba)


class Attachment(Controllable):

    allow_cascaded_delete = ['mail']

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    mail = dd.ForeignKey('outbox.Mail')

    def __str__(self):
        if self.owner_id:
            return str(self.owner)
        return str(self.id)

    def unused_save(self, *args, **kw):
        # see blog/2012/0929
        if not hasattr(self.owner, 'get_target_url'):
            raise ValidationError(
                "Controller %r has no method `get_target_url`." % self.owner)
        super().save(*args, **kw)

    # def as_summary_row(self, ar, **kw):
    #     url = self.owner.get_target_url()
    #     #~ url = ui.build_url(*parts)
    #     text = url.split('/')[-1]
    #     return ar.renderer.href(url, text)


dd.update_field(Mail, 'user', verbose_name=_("Sender"))

# def send_periodic_report(ar, name, template=None, excerpt_type=None):
#     if excerpt_type is None:
#     if template is None:
#         template = "excerpts/{}.weasy.html".format(name)
#
#     et = rt.models.exceprts.ExcerptType.get(pk=excerpt_type)
#     ex = et.get_or_create_excerpt(ar)
#     ex.do_print.run_from_ui(ar, **kw)
#
#
# @dd.background_task(every_unit='daily', every=1)
# def daily_report(ar):
#     send_periodic_report(ar, "daily")
