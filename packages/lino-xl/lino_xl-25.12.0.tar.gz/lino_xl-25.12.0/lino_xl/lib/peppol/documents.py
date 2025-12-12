# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/peppol.html

# from datetime import datetime
import base64
from importlib import import_module
from dateutil.parser import isoparse
from dateutil import parser as dateparser
from bs4 import BeautifulSoup
from django.utils import timezone
from django.conf import settings
from django.core.management import call_command
from django.db import models
from django.db.models import Q
from lino.api import dd, rt, _
from lino.core import constants
from lino.modlib.linod.models import SystemTasks
from lino.modlib.linod.choicelists import background_task
from lino_xl.lib.accounting.choicelists import VoucherStates, VoucherTypes
from lino_xl.lib.vat.choicelists import VatRegimes
from lino_xl.lib.accounting.mixins import VoucherRelated
from lino_xl.lib.accounting.roles import LedgerStaff
from lino_xl.lib.vat.ui import InvoicesByJournal

try:
    from lino_book import DEMO_DATA
except ImportError:
    DEMO_DATA = None

peppol = dd.plugins.peppol

REMOTE_WORKFLOW_BUTTONS = False


def check_supplier(docinfo):
    return docinfo['relationships']['supplier']['data']['id'] == peppol.supplier_id


def check_doctype(ar, obj, data):
    dt = 'peppolCreditNote' if obj.voucher.is_reversal() else 'peppolInvoice'
    if data['type'] != dt:
        ar.warning("Ibanity response says %s instead of %s in %s",
                   data['type'], dt, data)


def parse_timestamp(s):
    dt = isoparse(s)
    return dt if settings.USE_TZ else timezone.make_naive(dt)


class ResendDocument(dd.Action):
    label = _("Resend this document")
    help_text = _(
        "Resend this document and forget any previous sending attempt")
    select_rows = True
    # button_text = "𝄎"   # "\u1D10E"
    # button_text = "↪"  # 21aa
    button_text = "↯"  # 21af
    #  "𝄊"button_text = “𝄊  (U+1D1A)        # icon_name = 'bell'
    # icon_name = 'lightning'

    "\u128257"

    def run_from_ui(self, ar, **kwargs):
        to_send = []
        to_followup = []
        for obj in ar.selected_rows:
            assert issubclass(obj.__class__, OutboundDocument)
            if obj.outbound_state in {OutboundStates.created, OutboundStates.sending, OutboundStates.sent}:
                to_followup.append(obj)
            else:
                to_send.append(obj)
                obj.created_at = None
                obj.outbound_state = None
                obj.error_message = ''
                obj.full_clean()
                obj.save()
                if obj.voucher_id:
                    mf = obj.voucher.xmlfile
                    # xmlfile = Path(settings.MEDIA_ROOT, *parts)
                    ar.logger.info("Remove %s in order to resend %s.",
                                   mf.path, obj.voucher)
                    mf.path.unlink(missing_ok=True)
                    # obj.voucher.make_xml_file(ar)
        ses = dd.plugins.peppol.get_ibanity_session(ar)
        msg = ""
        if len(to_send):
            send_outbound(ses, to_send)
            msg += ", ".join(map(str, to_send)) + _(" have been resent.")
        if len(to_followup):
            followup_outbound(ses, to_followup)
            msg += ", ".join(map(str, to_followup)) + _(" have been checked.")
        ar.success(refresh=True, message=msg)
        # ar.set_response(refresh=True, message=_(
        #     "XML file has been rebuilt and will be sent with next sync"))

        # make_xml_file() called do_print, which filled open_url, but we
        # don't want it to pop up:
        # ar.response.pop('open_url', None)
        # print(f"20250415 {ar.response}")


class OutboundStates(dd.ChoiceList):
    verbose_name = _("State")
    verbose_name_plural = _("Outbound document states")
    required_roles = dd.login_required(LedgerStaff)


add = OutboundStates.add_item
add('10', _("Created"), 'created')
add('20', _("Sending"), 'sending')
add('30', _("Sent"), 'sent')
add('40', _("Invalid"), 'invalid')
# acknowledged, accepted, rejected and send-error are final technical statuses
# of a document:
add('50', _("Send-Error"), 'send_error')
add('51', _("Acknowledged"), 'acknowledged')
add('52', _("Accepted"), 'accepted')
add('53', _("Rejected"), 'rejected')


# class OutboundErrors(dd.ChoiceList):
#     verbose_name = _("State")
#     verbose_name_plural = _("Outbound document errors")
#     required_roles = dd.login_required(LedgerStaff)
#
#
# add = OutboundErrors.add_item
# add('010', _("Malicious"), 'malicious')
# add('020', _("Invalid format"), 'format')
# add('030', _("Invalid XML"), 'xsd')
# add('040', _("Invalid Schematron"), 'schematron')
# add('050', _("Invalid identifiers"), 'identifiers')
# add('060', _("Invalid size"), 'size')
# add('070', _("Invalid type"), 'invalid_type')
# add('080', _("Customer not registered"), 'customer_not_registered')
# add('090', _("Type not supported"), 'unsupported')
# add('100', _("Access Point issue"), 'access_point')
# add('110', _("Unspecified error"), 'unspecified')


class InboundDocument(dd.Model):
    class Meta:
        app_label = 'peppol'
        verbose_name = _("Inbound document")
        verbose_name_plural = _("Inbound documents")

    allow_cascaded_delete = ['voucher']

    document_id = models.CharField(
        _("DocumentId"), max_length=50, blank=True, editable=False, primary_key=True)
    transmission_id = models.CharField(
        _("Transmission ID"), max_length=50, blank=True, editable=False)
    created_at = models.DateTimeField(
        _("Created at"), editable=False, null=True)
    voucher = dd.ForeignKey(peppol.inbound_model, null=True,
                            blank=True, verbose_name=_("Invoice"))

    def __str__(self):
        return f"{self._meta.verbose_name} #{self.pk}"


EDITABLE = VoucherStates.filter(is_editable=True)
VOUCHER_FILTER = Q(voucher__isnull=True) | Q(voucher__state__in=EDITABLE)


class InboundDetail(dd.DetailLayout):
    main = """
    left center right
    """
    left = """
    document_id
    transmission_id
    created_at
    voucher__entry_date
    """
    center = """
    voucher  voucher__state
    voucher__partner
    voucher__vat_regime
    voucher__source_document
    """
    right = """
    voucher__total_base
    voucher__total_vat
    voucher__total_incl
    """


if REMOTE_WORKFLOW_BUTTONS:

    InboundDetail.left += "voucher__workflow_buttons"


class OutboundDetail(InboundDetail):
    main = """
    created_at document_id transmission_id
    left right
    """


class InboundDocuments(dd.Table):
    model = 'peppol.InboundDocument'
    order_by = ['created_at']
    detail_layout = InboundDetail()
    editable = False
    abstract = True

    if REMOTE_WORKFLOW_BUTTONS:

        workflow_state_field = "voucher__state"

        @classmethod
        def get_row_state(self, obj):
            print(f"20250528 {repr(obj)}")
            if isinstance(obj, peppol.inbound_model):
                return obj.state
            else:
                return obj.voucher.state

    @classmethod
    def override_column_headers(cls, ar, **headers):
        headers['voucher__total_incl'] = _("Amount")
        return super().override_column_headers(ar, **headers)


# dd.inject_field(
#     'accounting.Journal', 'is_outbound', models.BooleanField(
#         _("Peppol outbound"), default=False))
# dd.inject_field(
#     'contacts.Partner', 'send_peppol', models.BooleanField(
#         _("Peppol outbound"), default=False))
# dd.inject_field(
#     'contacts.Partner', 'peppol_id', models.CharField(
#         _("Peppol ID"), max_length=50, blank=True))


class OutboundDocument(VoucherRelated):

    class Meta:
        app_label = 'peppol'
        verbose_name = _("Outbound document")
        verbose_name_plural = _("Outbound documents")

    allow_cascaded_delete = 'voucher'
    resend_document = ResendDocument()

    voucher = dd.OneToOneField(
        peppol.outbound_model, primary_key=True,
        related_name="peppol_outbound", verbose_name=_("Invoice"))
    # voucher = dd.ForeignKey(
    #     peppol.outbound_model, verbose_name=_("Invoice"),
    #     related_name="peppol_outbound")
    document_id = models.CharField(
        _("DocumentId"), max_length=50, blank=True, editable=False)
    created_at = models.DateTimeField(
        _("Created at"), editable=False, null=True)
    outbound_state = OutboundStates.field(editable=False, null=True)
    # outbound_error = OutboundErrors.field(editable=False, null=True)
    transmission_id = models.CharField(
        _("Transmission ID"), max_length=50, blank=True, editable=False)
    error_message = dd.RichTextField(
        _("Error message"), blank=True, editable=False)

    # def disabled_fields(self, ar):
    #     rv = super().disabled_fields(ar)
    #     if self.transmission_id:
    #         rv.add('resend_document')
    #     return rv

    # @dd.displayfield(_("Voucher"))
    # def voucher_info(self, ar):
    #     v = self.voucher
    #     return f"{v.partner} {v.due_date} {v.total_incl}"

    # def __str__(self):
    #     return f"{self._meta.verbose_name} #{self.pk}"

    def __str__(self):
        return f"Sending {self.voucher}"

    @classmethod
    def get_simple_parameters(cls):
        for p in super().get_simple_parameters():
            yield p
        yield "outbound_state"


class OutboundDocuments(dd.Table):
    model = OutboundDocument
    # abstract = True
    editable = False

    detail_layout = """
    voucher_link
    voucher__xml_file

    document_id created_at
    outbound_state #outbound_error
    transmission_id
    error_message

    voucher__partner voucher__vat_regime
    voucher__entry_date
    voucher__total_base
    voucher__total_vat
    """


class Inbox(InboundDocuments):
    label = _("Incoming invoices")
    filter = VOUCHER_FILTER
    column_names = "created_at voucher voucher__partner voucher__total_incl voucher__source_document voucher__state *"
    welcome_message_when_count = 0


class Archive(InboundDocuments):
    label = _("Received invoices")
    model = 'peppol.InboundDocument'
    exclude = VOUCHER_FILTER
    column_names = "voucher voucher__partner voucher__vat_regime voucher__source_document voucher__state voucher__entry_date voucher__total_incl *"


class Outbox(OutboundDocuments):
    # label = _("Invoices to send")
    label = _("Outgoing invoices")
    # filter = models.Q(created_at__isnull=True)
    column_names = "voucher voucher__partner #voucher__vat_regime voucher__entry_date voucher__total_incl outbound_state created_at transmission_id *"
    # welcome_message_when_count = 0


# class Sent(OutboundDocuments):
#     label = _("Sent")
#     filter = models.Q(created_at__isnull=False)
#     column_names = "voucher voucher__partner created_at outbound_state transmission_id *"


class ReceivedInvoiceDetail(dd.DetailLayout):
    main = "general more"

    general = dd.Panel("""
    general1 general2 general3
    vat.ItemsByInvoice
    """, label=_("General"))

    general1 = """
    number partner
    entry_date
    """

    general2 = """
    source_document
    due_date
    """

    general3 = """
    workflow_buttons
    total_incl
    """

    more = dd.Panel("""
    more1 more2
    vat.MovementsByVoucher
    """, label=_("More"))

    more1 = """
    accounting_period your_ref:20 vat_regime:20
    match journal user
    payment_term
    narration id
    total_base
    total_vat
    """

    more2 = """
    uploads.UploadsByController:60
    """


class ReceivedInvoicesByJournal(InvoicesByJournal):
    detail_layout = ReceivedInvoiceDetail()


VoucherTypes.add_item_lazy(ReceivedInvoicesByJournal)


def collect_outbound(ar):
    # ar.debug("20250215 sync_peppol %s", peppol.outbound_model)
    ar.info("Collect outbound invoices into outbox")
    if peppol.outbound_model is None:
        ar.debug("No outbox on this site.")
        return
    qs = rt.models.accounting.Journal.objects.filter(is_outbound=True)
    if (count := qs.count()) == 0:
        ar.debug("No outbound journals configured")
        return
    ar.debug("Scan %d outbound journal(s): %s", count, [jnl.ref for jnl in qs])
    for jnl in qs:
        docs = peppol.outbound_model.objects.filter(journal=jnl)
        docs = docs.filter(partner__send_peppol=True)
        peppol_regimes = VatRegimes.filter(send_peppol=True)
        docs = docs.filter(vat_regime__in=peppol_regimes)
        docs = docs.filter(state=VoucherStates.registered)
        onboarding_date = peppol.onboarding_date
        if onboarding_date is not None:
            docs = docs.filter(entry_date__gte=onboarding_date.isoformat())
        if jnl.last_sending is not None:
            docs = docs.filter(entry_date__gte=jnl.last_sending)
        # qs = qs.filter(outbounddocument__isnull=True)
        docs = docs.exclude(id__in=OutboundDocument.objects.all())
        if (count := docs.count()) == 0:
            ar.info("No new new invoices for %s", jnl.ref)
            return
        ar.debug("Collect %d new invoices from %s into outbox", count, jnl.ref)
        for obj in docs.order_by('id'):
            OutboundDocument.objects.create(voucher=obj)
            if jnl.last_sending is None or obj.entry_date > jnl.last_sending:
                jnl.last_sending = obj.entry_date
                jnl.full_clean()
                jnl.save()


def send_outbound(ses, docs=None):
    ar = ses.ar
    ar.info("Send outbound documents")
    # if not settings.SITE.site_config.site_company:
    site_owner = settings.SITE.get_plugin_setting('contacts', 'site_owner', None)
    if not site_owner:
        ar.warning("You have no site owner configured.")
        return
    if docs is None:
        qs = OutboundDocument.objects.filter(created_at__isnull=True)
        if qs.count() == 0:
            ar.info("Outbox is empty")
            return
        docs = qs.order_by('voucher_id')

    for obj in docs:
        xmlfile = obj.voucher.make_xml_file(ar)
        if not ar.response.get('success', False):
            raise Exception(f"make_xml_file() failed for {obj}")
        ar.response.pop('open_url', None)
        # objects_to_save = [obj, voucher]
        ar.debug("Send %s", xmlfile.path)
        res = ses.create_outbound_document(peppol.supplier_id, xmlfile.path)
        ar.debug("Ibanity response %s", res['data'])
        data = res['data']
        if not check_supplier(data):
            ar.warning("Oops wrong supplier in %s", data)
        obj.document_id = data['id']
        obj.outbound_state = OutboundStates.get_by_name(
            data['attributes']['technicalStatus'].replace("-", "_"))
        # obj.outbound_error = OutboundErrors.get_by_name(
        #     data['attributes']['technicalState'])
        obj.created_at = parse_timestamp(data['attributes']['createdAt'])
        check_doctype(ar, obj, data)
        # voucher.state = VoucherStates.sent
        obj.full_clean()
        obj.save()
        # for obj in objects_to_save:
        #     obj.full_clean()
        # for obj in objects_to_save:
        #     obj.save()


def followup_outbound(ses, docs=None):
    ar = ses.ar
    ar.info("Follow up status of outbound documents")
    if docs is None:
        qs = OutboundDocument.objects.filter(created_at__isnull=False)
        qs = qs.exclude(outbound_state__in={
                        OutboundStates.sent, OutboundStates.invalid})
        if qs.count() == 0:
            ar.info("No outbound documents to follow up.")
            return
        docs = qs.order_by('created_at')
    for obj in docs:
        res = ses.get_outbound_document(peppol.supplier_id, obj.document_id)
        data = res['data']
        attrs = data['attributes']
        transmission_id = attrs.get('transmissionId', None)
        if transmission_id:
            obj.transmission_id = transmission_id
        else:
            ar.debug("No transmissionId in %s", res)
        if not check_supplier(data):
            ar.warning("Oops wrong supplier in %s", data)
        if (errors := attrs.get('errors', None)) is None:
            obj.error_message = ""
        else:
            obj.error_message = str(errors)
        new_state = OutboundStates.get_by_name(attrs['status'].replace("-", "_"))
        if obj.outbound_state != new_state:
            ar.info("%s (%s) state %s becomes %s",
                    obj.voucher, obj.transmission_id, obj.outbound_state.name,
                    new_state.name)
            obj.outbound_state = new_state
        check_doctype(ar, obj, data)
        obj.full_clean()
        obj.save()


def check_inbox(ses):
    ar = ses.ar
    ar.info("Check for new inbound documents")
    res = ses.list_inbound_documents(peppol.supplier_id)
    for docinfo in res['data']:
        # [{'attributes': {'createdAt': '...',
        #                  'transmissionId': 'c038dbdc1-26ed-41bf-9ebf-37g3c4ceaa58'},
        #   'id': '431cb851-5bb2-4526-8149-5655d648292f',
        #   'relationships': {'supplier': {'data': {'id': 'de142988-373c-4829-8181-92bdaf8ef26d',
        #                                           'type': 'supplier'}}},
        #   'type': 'peppolInboundDocument'}]
        document_id = docinfo['id']
        if not check_supplier(docinfo):
            # if not peppol.use_sandbox:
            ar.warning("Ignore document %s for other Peppol end user", document_id)
            continue
        qs = InboundDocument.objects.filter(document_id=document_id)
        if qs.count() == 0:
            ar.info("Receive document %s", document_id)
            InboundDocument.objects.create(
                document_id=document_id,
                transmission_id=docinfo['attributes']['transmissionId'],
                created_at=parse_timestamp(docinfo['attributes']['createdAt']))
        else:
            ar.warning("Document %s is still there", document_id)


def download_inbound(ses):
    ar = ses.ar
    ar.info("Download inbound documents")
    peppol.inbox_dir.mkdir(exist_ok=True)
    qs = InboundDocument.objects.filter(voucher__isnull=True)
    count = qs.count()
    if count == 0:
        ar.info("No inbound documents to download.")
        return
    ar.info("Found %s inbound documents to download", count)
    for obj in qs:
        ar.debug("Download %s", obj.document_id)
        xmlfile = peppol.inbox_dir / f"{obj.document_id}.xml"
        if xmlfile.exists():
            ar.debug("Reuse previously downloaded %s", xmlfile)
            res = xmlfile.read_text()
        else:
            # if peppol.use_sandbox:
            #     pth = DEMO_DATA / f"peppol/{obj.document_id}.xml"
            #     if not pth.exists():
            #         ar.warning("Oops, %s does not exist", pth)
            #         continue
            #     res = pth.read_text()
            # else:
            res = ses.get_inbound_document_xml(obj.document_id)
            ar.debug("Import %d bytes into %s", len(res), xmlfile)
            xmlfile.write_text(res)

        if not peppol.inbound_journal:
            ar.debug("This site has no inbound journal")
            continue
        jnl = rt.models.accounting.Journal.get_by_ref(peppol.inbound_journal, None)
        if jnl is None:
            ar.warning("Oops inbound_journal %s doesn't exist", peppol.inbound_journal)
            continue
        voucher = create_from_ubl(ar, jnl, res)
        if voucher is None:
            ar.info("Failed to create %s from %s",
                    jnl.voucher_type.text, obj.document_id)
        else:
            ar.info("Created %s from %s", voucher, obj.document_id)
            obj.voucher = voucher
            obj.full_clean()
            obj.save()


def create_from_ubl(ar, jnl, xml):
    soup = BeautifulSoup(xml, "xml")
    if (main := soup.find("Invoice")):
        ar.debug("It's an invoice")
    elif (main := soup.find("CreditNote")):
        ar.debug("It's a credit note")
    else:
        ar.warning(f"Invalid XML content {list(soup.children)}")
        return

    assert main.find("cbc:DocumentCurrencyCode").text == "EUR"
    kw = dict()
    if (e := main.find("cbc:IssueDate")) is not None:
        kw.update(entry_date=dateparser.parse(e.text))
    if (e := main.find("cbc:DueDate")) is not None:
        kw.update(due_date=dateparser.parse(e.text))
    if (e := main.find("cbc:BuyerReference")) is not None:
        kw.update(your_ref=e.text)
    if (tot := main.find("cac:LegalMonetaryTotal")) is None:
        ar.warning("No total amount")
        return
    if (e := tot.find("cbc:PayableAmount")) is not None:
        kw.update(total_incl=e.text)

    # print(main.find("cbc:IssueDate").prettify())
    # print(main.find("cbc:DueDate").prettify())
    Partner = rt.models.contacts.Partner
    p = main.find("cac:AccountingSupplierParty")
    p = p.find("cac:Party")
    endpoint = p.find("cbc:EndpointID")
    peppol_id = f"{endpoint['schemeID']}:{endpoint.text}"
    name = p.find("cac:PartyName").find("cbc:Name").string
    partner = None
    qs = Partner.objects.filter(peppol_id=peppol_id)
    if qs.count() == 1:
        partner = qs.first()
        if partner.name != name:
            ar.warning("Partner %s name %r != %r",
                       peppol_id, partner.name, name)
    elif qs.count() == 0:
        ar.debug("Unknown Peppol ID %s", peppol_id)
        qs = Partner.objects.filter(name=name)
        if qs.count() == 0:
            ar.info("Create partner %s with Peppol ID %s)",
                    name, peppol_id)
            partner = rt.models.contacts.Company(
                name=name, peppol_id=peppol_id)
            partner.full_clean()
            partner.save()
        elif qs.count() > 1:
            ar.debug("Multiple partners with name %s", name)
        else:
            ar.debug(
                "Assign %s to partner %s because name matches", peppol_id, name)
            partner = qs.first()
            partner.peppol_id = peppol_id
            partner.full_clean()
            partner.save()
    else:
        ar.debug("Multiple partners with Peppol ID %s", peppol_id)
    if partner is None:
        return
    ar.debug("Supplier %s is %s", peppol_id, partner)
    kw.update(partner=partner)
    # p = main.find("cac:AccountingCustomerParty")
    # p = p.find("cac:Party")
    # p = p.find("cbc:EndpointID")
    # print("I am the customer", p)
    # print(main.find("cac:AccountingCustomerParty").prettify())
    # print(str(kw))
    obj = jnl.create_voucher(**kw)
    obj.full_clean()
    obj.save()
    for line in main.find_all("cac:InvoiceLine"):
        # qty = line.find("cbc:InvoicedQuantity").text
        # account_text = line.find("cbc:AccountingCost").text
        # tax_cat = line.find("cac:ClassifiedTaxCategory").ID.text
        if e := line.find("cac:Item"):
            desc = e.find("cbc:Name").text
        if e := line.find("cbc:PriceAmount"):
            total_base = e.text
        ar.debug("Lino ignores information in %s %s", desc, total_base)
    obj.after_ui_save(ar, None)
    for adoc in main.find_all("cac:AdditionalDocumentReference"):
        if e := adoc.find("cbc:ID"):
            ar.debug("Lino ignores information in %s", e)
        if e := adoc.find("cbc:DocumentDescription"):
            desc = e.string
        if att := adoc.find("cac:Attachment"):
            if e := att.find("cac:ExternalReference"):
                ar.debug("Lino ignores information in %s", e)
            if bo := att.find("cbc:EmbeddedDocumentBinaryObject"):
                ar.debug("Store embedded file (%s) %s",
                         desc, bo['filename'])
                imgdata = base64.b64decode(bo.string)
                obj.store_attached_file(
                   ar, imgdata, bo['mimeCode'], bo['filename'], desc)
    return obj


def expand(obj):
    if obj is None:
        pass  # ignore None values
    elif isinstance(obj, models.Model):
        yield obj
    elif hasattr(obj, "__iter__"):
        for o in obj:
            for so in expand(o):
                yield so


# @dd.background_task(every_unit="daily", every=1)
# @background_task(every_unit="never")
@background_task(every_unit="hourly", every=1)
def sync_peppol(ar):
    if dd.is_installed('tim2lino') and settings.SITE.legacy_data_path:
        ar.info("Load latest data from TIM")
        # call_command('loaddata', 'tim2lino')
        mod = import_module(settings.SITE.plugins.tim2lino.timloader_module)
        tim = mod.TimLoader(settings.SITE.legacy_data_path, logger=ar.logger)
        count = 0
        for obj in expand(tim.objects()):
            obj.full_clean()
            obj.save()
            count += 1
        tim.finalize()
        ar.logger.info("Loaded %d database rows from TIM", count)

    if not peppol.supplier_id:
        ar.info("This site is not a Peppol end user")
        return
    collect_outbound(ar)
    ses = peppol.get_ibanity_session(ar)
    if ses is None:
        ar.info("No Ibanity credentials")
        return
    send_outbound(ses)
    followup_outbound(ses)
    check_inbox(ses)
    download_inbound(ses)


class SyncPeppol(SystemTasks):
    label = _("Synchronize Peppol")
    help_text = _("Send and receive documents via the Peppol network.")
    required_roles = dd.login_required(LedgerStaff)
    editable = False
    default_record_id = "row"
    default_display_modes = {None: constants.DISPLAY_MODE_DETAIL}
    live_panel_update = True
    detail_layout = """
    requested_at last_start_time last_end_time status
    message
    """

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        p = rt.models.linod.Procedures.find(func=sync_peppol)
        return rt.models.linod.SystemTask.objects.get(procedure=p)
